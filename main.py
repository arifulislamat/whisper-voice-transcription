import argparse
import whisper
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supported output formats
SUPPORTED_FORMATS = ["srt", "tsv", "txt", "vtt", "json"]

def save_srt(segments, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")

def save_tsv(segments, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("start\tend\tspeaker\ttext\n")
        for seg in segments:
            f.write(f"{seg['start']}\t{seg['end']}\t\t{seg['text'].strip()}\n")

def save_txt(segments, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg['text'].strip() + "\n")

def save_vtt(segments, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in segments:
            start = format_timestamp(seg["start"], vtt=True)
            end = format_timestamp(seg["end"], vtt=True)
            f.write(f"{start} --> {end}\n{seg['text'].strip()}\n\n")

def save_json(segments, out_path):
    import json
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

def format_timestamp(seconds, vtt=False):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    if vtt:
        return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"
    else:
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def main():
    parser = argparse.ArgumentParser(description="Whisper transcription with selectable output formats.")
    parser.add_argument("--audio", required=True, help="Audio filename (will look in inputs folder).")
    parser.add_argument("--model", default=os.getenv("WHISPER_MODEL", "small.en"), help="Whisper model size (default from .env or small.en)")
    parser.add_argument("--language", default=os.getenv("WHISPER_LANGUAGE"), help="Language code (e.g. 'en', 'bn') - default from .env or auto-detect.")
    parser.add_argument("--task", default=os.getenv("WHISPER_TASK", "transcribe"), choices=["transcribe", "translate"], help="Task type (default from .env or transcribe).")
    parser.add_argument("--formats", default=os.getenv("WHISPER_FORMATS", "txt"), help="Comma-separated output formats: srt,tsv,txt,vtt,json (default from .env or txt)")
    args = parser.parse_args()

    # Construct full path to audio file in inputs folder
    audio_path = os.path.join("inputs", args.audio)
    
    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print(f"Error: Audio file '{audio_path}' not found.")
        return

    # Display configuration
    print(f"Configuration:")
    print(f"  Audio file: {audio_path}")
    print(f"  Model: {args.model}")
    print(f"  Language: {args.language or 'auto-detect'}")
    print(f"  Task: {args.task}")
    print(f"  Formats: {args.formats}")
    print()

    model = whisper.load_model(args.model)
    result = model.transcribe(audio_path, language=args.language, task=args.task)
    segments = result["segments"]
    
    # Create outputs directory with date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the base filename (without extension) from the audio file
    audio_filename = os.path.basename(args.audio)
    base = os.path.splitext(audio_filename)[0]
    
    formats = [f.strip() for f in args.formats.split(",") if f.strip() in SUPPORTED_FORMATS]
    if not formats:
        print("No valid formats selected. Supported: srt, tsv, txt, vtt")
        return
    for fmt in formats:
        out_path = os.path.join(output_dir, f"{base}.{fmt}")
        if fmt == "srt":
            save_srt(segments, out_path)
        elif fmt == "tsv":
            save_tsv(segments, out_path)
        elif fmt == "txt":
            save_txt(segments, out_path)
        elif fmt == "vtt":
            save_vtt(segments, out_path)
        elif fmt == "json":
            save_json(segments, out_path)
        print(f"Saved {fmt} to {out_path}")

if __name__ == "__main__":
    main()
