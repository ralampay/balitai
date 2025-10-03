import argparse
from balitai import video_to_audio
from balitai import transcribe
from balitai import summarize

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

    # transcribe
    tr = subparsers.add_parser("transcribe", help="Transcribe + diarize audio")
    tr.add_argument("audio", help="Input audio file")
    tr.add_argument("--output", default="transcript.json", help="Output JSON file")

    # summarize
    sum_parser = subparsers.add_parser("summarize", help="Summarize diarized JSON into a news script")
    sum_parser.add_argument("input", help="Input diarized JSON file")
    sum_parser.add_argument("--output", default="summary.json", help="Output JSON file")
    sum_parser.add_argument("--model", required=True, help="Path to local GGUF model")

    args = parser.parse_args()

    if args.command == "video-to-audio":
        video_to_audio.extract_audio(args.input, args.output, args.sr, args.ch)
    elif args.command == "transcribe":
        transcribe.run_transcription(args.audio, args.output)
    elif args.command == "summarize":
        summarize.run_summarization(args.input, args.output, args.model)
    else:
        parser.print_help()
