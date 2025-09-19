import whisper
import os
import torch
import subprocess
import platform
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

def get_device(preferred_device=None):
    """Detect and return the best available device for inference."""
    if preferred_device and preferred_device.lower() != "auto":
        if preferred_device.lower() == "cuda" and torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"🚀 Using CUDA GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        elif preferred_device.lower() == "cpu":
            device = "cpu"
            print(f"💻 Using CPU (forced)")
        else:
            print(f"⚠️  Requested device '{preferred_device}' not available, falling back to CPU")
            device = "cpu"
            print(f"💻 Using CPU")
    else:
        # Auto-detection - only CUDA or CPU
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"🚀 CUDA GPU detected: {gpu_name} ({gpu_memory:.1f}GB)")
        else:
            device = "cpu"
            print(f"💻 Using CPU (no CUDA GPU detected)")
    return device

def check_ffmpeg_availability():
    """Check if FFmpeg is available and provide helpful error messages for Windows."""
    import subprocess
    import platform
    
    try:
        # Try to run ffmpeg to check if it's available
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=10)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        system = platform.system()
        if system == "Windows":
            error_msg = (
                "❌ FFmpeg not found. This is required for audio processing.\n\n"
                "🔧 Windows Installation Options:\n"
                "1. Download FFmpeg from: https://ffmpeg.org/download.html\n"
                "2. Extract and add to PATH, or\n"
                "3. Use Chocolatey: choco install ffmpeg\n"
                "4. Use Winget: winget install FFmpeg\n\n"
                "After installation, restart your terminal/command prompt."
            )
        elif system == "Darwin":  # macOS
            error_msg = (
                "❌ FFmpeg not found. Install with: brew install ffmpeg"
            )
        else:  # Linux
            error_msg = (
                "❌ FFmpeg not found. Install with: sudo apt install ffmpeg"
            )
        
        raise RuntimeError(error_msg)
    except Exception as e:
        # Other unexpected errors
        raise RuntimeError(f"❌ Error checking FFmpeg: {str(e)}")

def transcribe_audio_core(audio_path, model_name=None, language=None, task=None, formats=None, device=None):
    """
    Core transcription function that can be used by both CLI and Gradio.
    
    Args:
        audio_path: Path to audio file
        model_name: Whisper model size
        language: Language code or None for auto-detect
        task: 'transcribe' or 'translate'
        formats: List of output formats
        device: 'auto', 'cuda', or 'cpu'
    
    Returns:
        dict: Contains output_dir, files, and metadata
    """
    # Check FFmpeg availability first
    try:
        check_ffmpeg_availability()
    except RuntimeError as e:
        raise RuntimeError(str(e))
    
    # Use defaults from environment if not specified
    model_name = model_name or os.getenv("WHISPER_MODEL", "small.en")
    language = language or os.getenv("WHISPER_LANGUAGE")
    task = task or os.getenv("WHISPER_TASK", "transcribe")
    formats = formats or os.getenv("WHISPER_FORMATS", "txt").split(",")
    device = device or os.getenv("WHISPER_DEVICE", "auto")
    
    # Handle language auto-detection
    if language in [None, "", "auto", "Auto Detect"]:
        language = None
    
    # Ensure formats is a list and filter valid ones
    if isinstance(formats, str):
        formats = [f.strip() for f in formats.split(",")]
    formats = [f.strip() for f in formats if f.strip() in SUPPORTED_FORMATS]
    
    if not formats:
        raise ValueError("No valid formats selected. Supported: " + ", ".join(SUPPORTED_FORMATS))
    
    # Check if the audio file exists
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file '{audio_path}' not found.")

    # Detect best available device
    device = get_device(device)
    
    # Load model with fallback
    print(f"Loading model '{model_name}' on {device}...")
    try:
        model = whisper.load_model(model_name, device=device)
    except Exception as e:
        if device == "cuda":
            print(f"⚠️  Failed to load model on CUDA: {str(e)[:100]}...")
            print(f"🔄 Falling back to CPU...")
            device = "cpu"
            model = whisper.load_model(model_name, device=device)
        else:
            raise e
    
    # Transcribe audio with better error handling
    print(f"Starting transcription...")
    try:
        result = model.transcribe(audio_path, language=language, task=task)
    except Exception as e:
        # Check if this looks like an FFmpeg error
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in ['ffmpeg', 'file specified', 'winerror 2', 'cannot find']):
            raise RuntimeError(
                "❌ Audio processing failed. This is usually caused by missing FFmpeg.\n\n"
                "🔧 Windows users: Install FFmpeg from https://ffmpeg.org/download.html\n"
                "Make sure FFmpeg is added to your system PATH.\n\n"
                f"Original error: {str(e)}"
            )
        else:
            # Re-raise the original error if it's not FFmpeg-related
            raise e
    segments = result["segments"]
    
    # Create outputs directory with date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the base filename (without extension) from the audio file
    audio_filename = os.path.basename(audio_path)
    base = os.path.splitext(audio_filename)[0]
    
    # Save files in requested formats
    output_files = []
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
        
        output_files.append(out_path)
        print(f"Saved {fmt} to {out_path}")
    
    return {
        "output_dir": output_dir,
        "files": output_files,
        "segments": segments,
        "language": result.get("language"),
        "model": model_name,
        "device": device
    }
