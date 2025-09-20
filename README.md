# Whisper Voice Transcription

A Python-based audio transcription tool (STT) using OpenAI's Whisper model with configurable output formats and automated file organization.

## 🎯 Project Overview

This project provides a streamlined interface for transcribing audio files using OpenAI's Whisper speech recognition model. It features a **unified entry point** that supports both CLI automation and web interface modes, with multiple output formats, automatic file organization with timestamps, environment-based configuration, and NVIDIA CUDA acceleration for faster processing.

### ✨ Features

- **🌐 Web Interface**: User-friendly Gradio web UI for easy drag-and-drop transcription
- **💻 Command Line Interface**: Full CLI support for automation and scripting
- **Multiple Output Formats**: SRT, TXT, JSON, VTT, TSV
- **CUDA GPU Acceleration**: Automatic NVIDIA GPU detection for faster transcription
- **Automatic File Organization**: Timestamped output folders
- **Environment Configuration**: `.env` file support for default settings
- **Input/Output Folder Structure**: Organized file management
- **Language Detection**: Auto-detect or specify language
- **Model Selection**: Choose from different Whisper model sizes
- **Task Types**: Transcription or translation

### Prerequisites

- `uv` package manager (AIO pkg, env, runtime manager)
- FFmpeg (for audio processing)
- NVIDIA GPU with CUDA (optional, for acceleration)

<details>
<summary><strong>✋🏽 Only if you don't have it already</strong> (click to expand)</summary>

1. **Install FFmpeg (if not already installed):**

   macOS:

   ```bash
   brew install ffmpeg
   ```

   Ubuntu/Debian:

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   Windows:
   Download from [FFmpeg official website](https://ffmpeg.org/download.html)

2. **Install UV (if not already installed):**

   macOS:

   ```bash
   brew install uv
   ```

   OR

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Ubuntu/Debian:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

</details>

### ⚡ Super Quick Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/arifulislamat/whisper-voice-transcription.git
   cd whisper-voice-transcription
   ```

2. **Install dependencies using uv:**

   For CPU only mode (Default):

   ```bash
   uv sync
   ```

   For Linux/Windows with NVIDIA GPU (CUDA 12.8):

   ```bash
   uv sync --extra cu128
   ```

   > **Note**: To use above commend, first you will need to uncomment line number `29 to 46` in `pyproject.toml` file.

## 📁 Usage

You can use this tool in two ways: **Web Interface** (easiest) or **Command Line** (for automation).

### 🌐 Option 1: Web Interface (Recommended for beginners)

This project now includes a user-friendly web interface powered by Gradio, perfect for non-technical users or quick transcriptions.

#### Launch Web Interface

```bash
uv run python main.py --web
```

This will start a web server (usually at `http://127.0.0.1:7860`) where you can:

- **Upload audio files** via drag-and-drop or file picker
- **Select Whisper model** from dropdown (tiny.en, base.en, small.en, medium.en, large, turbo)
- **Choose language** (auto-detect or specific language)
- **Pick output formats** (multiple selection: SRT, TXT, JSON, VTT, TSV)
- **Set device preference** (auto, CUDA, CPU)
- **Start Transcription** directly from the browser

### ⌨️ Option 2: CLI - Command Line Interface

#### Prepare Audio Files

Place your audio files in the `inputs/` folder:

```bash
mkdir inputs
cp english-voice-example.mp3 inputs/
```

#### Basic CLI Usage

Using uv (simplest):

```bash
uv run main.py --audio english-voice-example.mp3
```

#### Advanced CLI Usage

Override specific settings:

```bash
uv run main.py --audio english-voice-example.mp3 --model large --language es
```

Multiple output formats:

```bash
uv run main.py --audio english-voice-example.mp3 --formats srt,txt,json,vtt
```

Translation task:

```bash
uv run main.py --audio spanish-audio.mp3 --task translate --language es
```

Force GPU/CPU usage:

```bash
uv run main.py --audio audio.mp3 --device cuda  # Force CUDA
uv run main.py --audio audio.mp3 --device cpu   # Force CPU
```

Complete configuration override:

```bash
uv run python main.py --audio audio-file.wav \
--model medium \
--language bn \
--task transcribe \
--formats srt,txt \
--device auto
```

#### CLI Command Line Arguments

```text
python main.py [OPTIONS]

Options:
--web                 Launch web interface instead of CLI mode
--audio FILEPATH      Path to audio file (required for CLI mode)
--model MODEL         Whisper model size (default from .env)
--language CODE       Language code (default from .env or auto-detect)
--task TASK           transcribe or translate (default from .env)
--formats FORMATS     Comma-separated formats (default from .env)
--device DEVICE       auto, cuda, or cpu (default from .env)
```

### Dual Interface Benefits

| Feature              | CLI                           | Web Interface         |
| -------------------- | ----------------------------- | --------------------- |
| **Automation**       | ✅ Perfect for scripts        | ❌ Manual only        |
| **Ease of use**      | ❌ Requires command knowledge | ✅ Point and click    |
| **Batch processing** | ✅ Easy with shell scripts    | ❌ One file at a time |
| **User-friendly**    | ❌ Technical users only       | ✅ Anyone can use     |
| **Remote access**    | ❌ Local only                 | ✅ Can be hosted      |
| **Mobile Support**   | ❌ No                         | ✅ Yes                |
| **File Management**  | ❌ Manual                     | ✅ Automatic download |

### Project Structure

```text
whisper-voice-transcription/   # Repo Directory
├── main.py                    # Unified CLI & Web interface
├── transcription_core.py      # Shared transcription logic
├── .env                       # Environment configuration
├── inputs/                    # Place audio files here (optional)
├── outputs/                   # Transcription outputs (auto-created)
│   └── YYYYMMDD_HHMMSS/       # Timestamped folders per run
├── pyproject.toml             # Project dependencies
├── uv.lock                    # uv package lock file
├── bangla-voice-example.mp3   # Sample audio (Bangla)
├── english-voice-example.mp3  # Sample audio (English)
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables (.env)

Create or modify the `.env` file to set default values:

```env
WHISPER_MODEL=small.en
WHISPER_LANGUAGE=en
WHISPER_TASK=transcribe
WHISPER_FORMATS=srt,txt,json
WHISPER_DEVICE=auto
GRADIO_SHARE=false
```

## 🎵 Whisper Models

### Model Sizes & Performance

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
| :----: | :--------: | :----------------: | :----------------: | :-----------: | :------------: |
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~10x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~7x       |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~4x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
| turbo  |   809 M    |        N/A         |      `turbo`       |     ~6 GB     |      ~8x       |

### Recommendations

- **English audio**: Use `.en` models for better performance
- **Limited VRAM**: Start with `tiny` or `base`
- **Best quality**: Use `large` or `turbo`
- **Balanced**: `small.en` for English, `small` for multilingual

## 🗃️ Output Formats

### SRT (SubRip)

```srt
1
00:00:00,000 --> 00:00:04,000
Hello, this is a sample transcription.

2
00:00:04,000 --> 00:00:08,000
The text appears with timestamps.
```

### TXT (Plain Text)

```txt
Hello, this is a sample transcription.
The text appears with timestamps.
```

### JSON (Detailed)

```json
[
  {
    "start": 0.0,
    "end": 4.0,
    "text": "Hello, this is a sample transcription."
  }
]
```

### VTT (WebVTT)

```vtt
WEBVTT

00:00:00.000 --> 00:00:04.000
Hello, this is a sample transcription.
```

### TSV (Tab-Separated)

```tsv
start	end	speaker	text
0.0	4.0		Hello, this is a sample transcription.
```

## 🐛 Troubleshooting

### Common Issues

"Audio file not found" error:

- Check the file path is correct
- Ensure the file exists and is accessible

FFmpeg errors:

- Install FFmpeg using the instructions above
- Ensure FFmpeg is in your system PATH

Web interface won't start:

```bash
# Check if port 7860 is available
lsof -i :7860

# Kill process using the port if needed
pkill -f "python main.py --web"
```

Web upload fails:

- Check file format is supported (MP3, WAV, M4A, FLAC, etc.)
- Ensure file size is reasonable (<500MB recommended)
- Verify browser supports file uploads

Out of memory errors:

- Use a smaller model (`tiny`, `base`, `small`)
- Close other applications to free up RAM/VRAM
- Use CPU mode: `--device cpu`

Slow transcription:

- Use GPU if available: ensure CUDA is properly installed
- Choose a smaller model for faster processing
- Check if other processes are using GPU resources

### GPU Troubleshooting

CUDA not detected:

```bash
# Check CUDA installation
nvidia-smi
```

```python
# Check PyTorch CUDA support
python -c "import torch; print(torch.cuda.is_available())"
```

### Using Python directly

Ubuntu/Debian (Mac/Linux):

```bash
source .venv/bin/activate
```

Windows (CMD):

```cmd
.venv\Scripts\activate.bat
```

Start STT:

```bash
python main.py --audio english-voice-example.mp3
```

CUDA out of memory:

- Use smaller models (`tiny`, `base`, `small`)
- Reduce batch size by processing shorter audio clips
- Close other GPU-intensive applications

## 📝 License

This project is open source under MIT License. Please check the license file for details.

## 🤝 How to contribute

We welcome contributions. A minimal workflow:

1. Fork the repository.
2. Create a branch for your change: `git checkout -b feat/your-feature`.
3. Make changes and add tests where applicable.
4. Run any project linters/tests and ensure they pass.
5. Commit with clear messages and push your branch: `git push origin feat/your-feature`.
6. Open a Pull Request against the `main` branch, describe the change, and reference any related issues.
7. Address any feedback and iterate as needed.

## 📞 Support

If you encounter any issues or have questions, please:

1. Search existing issues
2. Create a new issue if not exist with detailed information

---

**Happy transcribing! 🎤✨**
