import subprocess

def extract_audio(input_video, output_audio, sample_rate=16000, channels=1):
    """
    Extract audio from a video file using ffmpeg.

    Args:
        input_video (str): Path to input video file (e.g., mp4, mkv, mov)
        output_audio (str): Path to output audio file (wav, mp3, etc.)
        sample_rate (int): Audio sample rate (default: 16000 Hz, good for Whisper)
        channels (int): Number of audio channels (default: 1 = mono)
    """
    cmd = [
        "ffmpeg",
        "-i", input_video,
        "-ar", str(sample_rate),  # resample
        "-ac", str(channels),     # mono/stereo
        output_audio,
        "-y"  # overwrite without asking
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted audio saved to {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
