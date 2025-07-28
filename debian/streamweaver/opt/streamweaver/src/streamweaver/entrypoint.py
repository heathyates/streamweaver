#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Stream MP4 as RTSP using ffmpeg and MediaMTX"
    )
    parser.add_argument(
        "--path", type=str, help="Path to MP4 file (default: use a prebaked one)"
    )
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--width", type=int, default=1280, help="Video width")
    parser.add_argument("--height", type=int, default=720, help="Video height")
    parser.add_argument(
        "--rtsp-url", type=str, default="rtsp://127.0.0.1:8554/ai-sim", help="RTSP URL"
    )
    args = parser.parse_args()

    # Find MP4
    mp4_path = args.path
    if not mp4_path:
        # Use first prebaked MP4 in /opt/streamweaver/video
        video_dir = Path("/opt/streamweaver/video")
        mp4s = list(video_dir.glob("*.mp4"))
        if not mp4s:
            print("No prebaked MP4s found in /opt/streamweaver/video")
            sys.exit(1)
        mp4_path = str(mp4s[0])

    # Start MediaMTX if not running
    mediamtx_bin = "/opt/streamweaver/mediamtx"
    if not any("mediamtx" in p for p in os.popen("ps ax -o command").readlines()):
        print("Starting MediaMTX...")
        subprocess.Popen(
            [mediamtx_bin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    # Run ffmpeg to stream to RTSP
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-stream_loop",
        "-1",
        "-i",
        mp4_path,
        "-vf",
        f"fps={args.fps},scale={args.width}:{args.height}",
        "-c:v",
        "libx264",
        "-f",
        "rtsp",
        args.rtsp_url,
    ]
    print("Running:", " ".join(ffmpeg_cmd))
    subprocess.run(ffmpeg_cmd)


if __name__ == "__main__":
    main()
