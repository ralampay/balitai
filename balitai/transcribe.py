import whisper
import json
import os
import wave
from pyannote.audio import Pipeline

def get_audio_duration(file_path: str) -> float:
    """Return audio duration in seconds."""
    with wave.open(file_path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

def run_transcription(audio_file: str, output_file: str):
    """
    Transcribe and diarize audio, then save structured JSON.
    
    Args:
        audio_file (str): Path to audio file (.wav, .mp3, etc.)
        output_file (str): Path to output JSON
    """
    # Load Whisper model
    model_name = "base"
    print(f"Loading whisper model {model_name}")
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_file)

    # Load Hugging Face token
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")
    if not hf_token:
        raise RuntimeError("HuggingFace token required.")

    # Run pyannote diarization
    print("Running diarization...")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", 
        token=hf_token,
        revision="main"
    )

    diarization = pipeline(audio_file)

    print(type(diarization))
    print(dir(diarization))

    # Collect speaker segments
    print("Collecting speaker segments...")
    annotation = diarization.speaker_diarization  # this is a pyannote.core.Annotation

    speaker_segments = []
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        speaker_segments.append({
            "speaker": str(speaker),
            "start": float(segment.start),
            "end": float(segment.end)
        })



    # Unique speaker list
    print("Extracting unique speakers...")
    speakers = sorted(list({seg["speaker"] for seg in speaker_segments}))

    # Merge Whisper + diarization
    print("Merging data...")
    diarized_output = []
    for seg in result["segments"]:
        seg_start, seg_end, text = seg["start"], seg["end"], seg["text"]

        speaker = "UNKNOWN"
        for spk in speaker_segments:
            if spk["start"] <= seg_start < spk["end"] or spk["start"] < seg_end <= spk["end"]:
                speaker = spk["speaker"]
                break

        diarized_output.append({
            "speaker": speaker,
            "start": seg_start,
            "end": seg_end,
            "text": text.strip()
        })

    # Final JSON structure
    output_json = {
        "meta": {
            "filename": os.path.basename(audio_file),
            "duration": round(get_audio_duration(audio_file), 2),
            "model": f"whisper-{model_name}"
        },
        "speakers": speakers,
        "segments": diarized_output
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)

    print(f"Diarized transcript saved to {output_file}")
