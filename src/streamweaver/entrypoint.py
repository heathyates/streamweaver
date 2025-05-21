# src/streamweaver/entrypoint.py

import argparse

from streamweaver import streamer


def main():
    parser = argparse.ArgumentParser(
        description="Stream video to RTSP via MediaMTX + FFmpeg"
    )
    parser.add_argument("video_path", help="Path to the .mp4 video")
    parser.add_argument("--fps", type=int, help="Target FPS (e.g. 30)")
    parser.add_argument("--codec", type=str, help="Video codec (e.g. libx264, copy)")
    parser.add_argument("--res", type=str, help="Vertical resolution (e.g. 720, 1080)")

    args = parser.parse_args()

    streamer.stream_video(
        video_path=args.video_path, fps=args.fps, codec=args.codec, resolution=args.res
    )


if __name__ == "__main__":
    main()
