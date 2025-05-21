# src/streamweaver/streamer.py

import os
import subprocess
import time
from typing import Optional

# Get the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to thirdparty/mediamtx relative to this file
MEDIA_MTX_PATH = os.path.join(BASE_DIR, "thirdparty", "mediamtx", "mediamtx")
MEDIA_MTX_CONFIG = os.path.join(BASE_DIR, "thirdparty", "mediamtx", "mediamtx.yml")
RTSP_URL = "rtsp://localhost:8554/stream"


def start_mediamtx():
    if not os.path.exists(MEDIA_MTX_PATH):
        raise FileNotFoundError(f"MediaMTX binary not found at: {MEDIA_MTX_PATH}")
    if not os.path.exists(MEDIA_MTX_CONFIG):
        raise FileNotFoundError(f"MediaMTX config not found at: {MEDIA_MTX_CONFIG}")

    return subprocess.Popen([MEDIA_MTX_PATH, MEDIA_MTX_CONFIG])


def build_ffmpeg_command(
    video_path: str, fps: Optional[int], codec: Optional[str], resolution: Optional[str]
) -> list:
    cmd = ["ffmpeg", "-re", "-stream_loop", "-1", "-i", video_path]

    if fps:
        cmd += ["-r", str(fps)]
    if codec:
        cmd += ["-c:v", codec]
    if resolution:
        cmd += ["-vf", f"scale=-2:{resolution}"]  # width auto, height fixed (e.g., 720)

    # Always RTSP output
    cmd += ["-f", "rtsp", RTSP_URL]
    return cmd


def stream_video(
    video_path: str,
    fps: Optional[int] = None,
    codec: Optional[str] = None,
    resolution: Optional[str] = None,
):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist: {video_path}")

    print(f"[🎛️] Starting MediaMTX with config: {MEDIA_MTX_CONFIG}")
    mediamtx_proc = start_mediamtx()
    time.sleep(2)  # Allow MediaMTX to bind port

    ffmpeg_cmd = build_ffmpeg_command(video_path, fps, codec, resolution)
    print(f"[🎞️] Starting FFmpeg with command:\n{' '.join(ffmpeg_cmd)}")

    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd)

    try:
        ffmpeg_proc.wait()
    except KeyboardInterrupt:
        print("[🛑] Caught Ctrl+C, terminating...")
        ffmpeg_proc.terminate()
        mediamtx_proc.terminate()
