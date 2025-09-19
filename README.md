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

1.  **Install FFmpeg (if not already installed):**

    **macOS:**

    ```bash
    brew install ffmpeg
    ```

    **Ubuntu/Debian:**

    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

    **Windows:**

    **⚠️ IMPORTANT: FFmpeg is required for audio processing and commonly missing on Windows!**

    **Option 1 - Direct Download (Recommended):**

    1. Download from [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)
    2. Extract the ZIP file (e.g., to `C:\ffmpeg`)
    3. Add `C:\ffmpeg\bin` to your Windows PATH:
       - Press `Win + R`, type `sysdm.cpl`, press Enter
       - Click "Environment Variables"
       - Under "System Variables", find and select "Path", click "Edit"
       - Click "New" and add `C:\ffmpeg\bin`
       - Click "OK" to close all dialogs
    4. Restart your terminal/command prompt

    **Option 2 - Package Managers:**

    ```bash
    # Using Chocolatey
    choco install ffmpeg

    # Using Winget
    winget install FFmpeg
    ```

    **⚠️ Common Windows Issues:**

    - If you get `[WinError 2] The system cannot find the file specified`, FFmpeg is not properly installed
    - Make sure to restart your terminal after adding FFmpeg to PATH
    - Test installation by running `ffmpeg -version` in Command Prompt

2.  **Install UV (if not already installed):**

    **macOS:**

    ```bash
    brew install uv
    ```

    **OR**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    **Ubuntu/Debian:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    **Windows:**

    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

</details>

### ⚡ Super Quick Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/arifulislamat/whisper-voice-transcription.git
   cd whisper-voice-transcription
   ```

2. **Install dependencies using uv (recommended):**

   ```bash
   uv sync
   ```

3. **🔧 Test your installation (especially Windows users):**

   ```bash
   # Check if FFmpeg is properly installed
   uv run python check_ffmpeg.py
   ```

   If you see ✅ messages, you're ready to go! If you see ❌ errors, follow the FFmpeg installation guide above.

## 📁 Usage

You can use this tool in two ways: **Web Interface** (easiest) or **Command Line** (for automation).

### 🌐 Option 1: Web Interface (Recommended for beginners)

This project now includes a user-friendly web interface powered by Gradio, perfect for non-technical users or quick transcriptions.

### Launch Web Interface

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

### Web Interface Features

- **Drag & Drop Audio Upload**: Upload audio files directly in your browser
- **Live Configuration**: Adjust settings with dropdowns and checkboxes
- **Real-time Feedback**: See transcription progress and results instantly
- **Multi-format Download**: Get results in ZIP files for multiple formats
- **Mobile-friendly**: Responsive design works on phones and tablets
- **Same Configuration**: Uses your `.env` settings as defaults
- **No installation needed** for end users - just share the web link

### Interface Sections

#### Audio Input Section

- **Upload Area**: Supports MP3, WAV, M4A, FLAC, and more
- **Sample Files**: Use provided english-voice-example.mp3 or bangla-voice-example.mp3 ( need to copy them into inputs dir)

#### Configuration Panel

- **Whisper Model Size**: Choose from tiny.en (fast) to large (most accurate)
- **Language**: Auto-detect or select from 15+ languages
- **Task**: Transcribe in original language or translate to English
- **Output Formats**: Select multiple formats (packaged in ZIP)
- **Processing Device**: Auto-detect GPU or force CPU

#### Results Section

- **Status Display**: Real-time progress and configuration summary
- **Output Location**: All files saved in timestamped `outputs/` folders

### Advanced Web Interface Usage

#### Public Access

To share the interface out of your home network:

`Set GRADIO_SHARE=true in .env`

> **Note:** Use `--web` flag to launch the intuitive web interface - no other arguments needed!

### ⌨️ Option 2: CLI - Command Line Interface

1. Prepare Audio Files

   Place your audio files in the `inputs/` folder:

   ```bash
   mkdir inputs
   cp english-voice-example.mp3 inputs/
   ```

2. Basic CLI Usage

   **Using uv (simplest):**

   ```bash
   uv run python main.py --audio english-voice-example.mp3
   ```

3. Advanced CLI Usage

   **Override specific settings:**

   ```bash
   uv run python main.py --audio english-voice-example.mp3 --model large --language es
   ```

   **Multiple output formats:**

   ```bash
   uv run python main.py --audio english-voice-example.mp3 --formats srt,txt,json,vtt
   ```

   **Translation task:**

   ```bash
   uv run python main.py --audio spanish-audio.mp3 --task translate --language es
   ```

   **Force GPU/CPU usage:**

   ```bash
   uv run python main.py --audio audio.mp3 --device cuda  # Force CUDA
   uv run python main.py --audio audio.mp3 --device cpu   # Force CPU
   ```

   **Complete configuration override:**

   ```bash
   uv run python main.py --audio audio-file.wav \
   --model medium \
   --language bn \
   --task transcribe \
   --formats srt,txt \
   --device auto
   ```

4. CLI Command Line Arguments

   ```bash
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

5. Using Python directly

   **Ubuntu/Debian (Mac/Linux):**

   ```bash
   source .venv/bin/activate

   ```

   **WIndows (CMD):**

   ```bash
   .venv\Scripts\activate.bat
   ```

   **Start STT:**

   ```bash
   python main.py --audio english-voice-example.mp3
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

```
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

## 🏞️ GPU Acceleration

### NVIDIA CUDA Support

For faster transcription with NVIDIA GPUs:

1. **Install CUDA-enabled PyTorch:**

   ```bash
   uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

2. **The tool will automatically detect and use your GPU:**
   ```bash
   🚀 CUDA GPU detected: GeForce RTX 4090 (24.0GB)
   ```

### Device Selection

| Device | Usage                                | Performance    |
| ------ | ------------------------------------ | -------------- |
| `auto` | Automatic detection (CUDA → CPU)     | Best available |
| `cuda` | Force NVIDIA GPU (falls back to CPU) | Fastest        |
| `cpu`  | Force CPU only                       | Reliable       |

### Performance Comparison

| Model   | CPU (M2 Max)  | RTX 4090     | Speedup |
| ------- | ------------- | ------------ | ------- |
| `tiny`  | 2x realtime   | 15x realtime | 7.5x    |
| `small` | 1x realtime   | 8x realtime  | 8x      |
| `large` | 0.3x realtime | 3x realtime  | 10x     |

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

**"Audio file not found" error:**

- Check the file path is correct
- Ensure the file exists and is accessible

**FFmpeg errors:**

- Install FFmpeg using the instructions above
- Ensure FFmpeg is in your system PATH

**Web interface won't start:**

```bash
# Check if port 7860 is available
lsof -i :7860

# Kill process using the port if needed
pkill -f "python main.py --web"
```

**Web upload fails:**

- Check file format is supported (MP3, WAV, M4A, FLAC, etc.)
- Ensure file size is reasonable (<500MB recommended)
- Verify browser supports file uploads

**Out of memory errors:**

- Use a smaller model (`tiny`, `base`, `small`)
- Close other applications to free up RAM/VRAM
- Use CPU mode: `--device cpu`

**Slow transcription:**

- Use GPU if available: ensure CUDA is properly installed
- Choose a smaller model for faster processing
- Check if other processes are using GPU resources

### Windows-Specific Issues

**❌ `[WinError 2] The system cannot find the file specified`:**

This is the most common Windows error and means FFmpeg is not installed or not in PATH.

**Solutions:**

1. Install FFmpeg following the Windows instructions above
2. Verify installation: open Command Prompt and run `ffmpeg -version`
3. If still failing, restart your computer after PATH changes
4. Check Windows Defender isn't blocking FFmpeg execution

**❌ Permission denied errors:**

- Run Command Prompt as Administrator
- Check Windows Defender/antivirus isn't blocking the application
- Ensure the `inputs` and `outputs` folders are writable

**❌ Audio file upload issues in Web Interface:**

- Try different audio formats (MP3, WAV, M4A)
- Ensure file isn't corrupted
- Check file size (very large files may timeout)
- Use shorter audio clips for testing

**💡 Windows Tips:**

- Use Windows Terminal or PowerShell instead of old Command Prompt
- Place audio files in the `inputs` folder to avoid path issues
- Avoid special characters in file names

### GPU Troubleshooting

**CUDA not detected:**

```bash
# Check CUDA installation
nvidia-smi

# Check PyTorch CUDA support
python -c "import torch; print(torch.cuda.is_available())"
```

**CUDA out of memory:**

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
