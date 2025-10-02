# BalitAI

An AI summarizer that gives you the news from a video source.

## Installation

BalitAI requires a HuggingFace access tokent to perform speaker diarization. Set is an environment variable:

**Linux / Mac OS**

```bash
export HUGGINGFACE_TOKEN=your_token_here
```

**Windows (PowerShell)**

```powershell
$env:HUGGINGFACE_TOKEN="your_token_here"
```

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/balitai.git
cd balitai
pip install -e .
```

Make sure you have `ffmpeg` installed:

### Ubuntu / Debian

```bash
sudo apt update && sudo apt install ffmpeg -y
```

### Mac (Homebrew)

```bash
brew install ffmpeg
```

## Usage

### Convert Video to Audio

Extract audio from a video file:

```bash
balitai video-to-audio input.mp4 output.wav
```

### Transcribe and Diarize

Transcribe audio and annotate who said what:

```bash
balitai transcribe output.wav --output transcript.json
```

The tool will automatically pick up the token from `HUGGINGFACE_TOKEN` environment variable.

Example JSON output:

```json
{
  "meta": {
    "filename": "output.wav",
    "duration": 123.45,
    "model": "whisper-base"
  },
  "speakers": [
    "SPEAKER_0",
    "SPEAKER_1"
  ],
  "segments": [
    {
      "speaker": "SPEAKER_0",
      "start": 0.0,
      "end": 5.2,
      "text": "Welcome to our video news summary."
    },
    {
      "speaker": "SPEAKER_1",
      "start": 5.3,
      "end": 9.1,
      "text": "Today we will discuss the latest updates."
    }
  ]
}
```
