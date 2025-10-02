import argparse
from balitai import video_to_audio

def main():
    parser = argparse.ArgumentParser(
        prog="balitai",
        description="BalitAI CLI Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # video to audio
    v2a = subparsers.add_parser("video-to-audio", help="Extract audio from video")
    v2a.add_argument("input", help="Input video file")
    v2a.add_argument("output", help="Output audio file (wav/mp3)")
    v2a.add_argument("--sr", type=int, default=16000, help="Sample rate (default 16000 Hz)")
    v2a.add_argument("--ch", type=int, default=1, help="Number of channels (default mono)")

    args = parser.parse_args()

    if args.command == "video-to-audio":
        video_to_audio.extract_audio(args.input, args.output, args.sr, args.ch)
    else:
        parser.print_help()
