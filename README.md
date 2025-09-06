# Whisper Voice Transcription

A Python-based audio transcription tool (STT) using OpenAI's Whisper model with configurable output formats and automated file organization.

## 🎯 Project Overview

This projects provides a streamlined interface for transcribing audio files using OpenAI's Whisper speech recognition model. It supports multiple output formats, automatic file organization with timestamps, environment-based configuration, and NVIDIA CUDA acceleration for faster processing.

### ✨ Features

- **Multiple Output Formats**: SRT, TXT, JSON, VTT, TSV
- **CUDA GPU Acceleration**: Automatic NVIDIA GPU detection for faster transcription
- **Automatic File Organization**: Timestamped output folders
- **Environment Configuration**: `.env` file support for default settings
- **Input/Output Folder Structure**: Organized file management
- **Language Detection**: Auto-detect or specify language
- **Model Selection**: Choose from different Whisper model sizes
- **Task Types**: Transcription or translation

## 🚀 Quick Start

### Prerequisites

- `uv` package manager (If not installed)
- FFmpeg (for audio processing)
- NVIDIA GPU with CUDA (optional, for acceleration)

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
    Download from [FFmpeg official website](https://ffmpeg.org/download.html)

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

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/arifulislamat/whisper-voice-transcription.git
   cd whisper-voice-transcription
   ```

2. **Install dependencies using uv (recommended):**
   ```bash
   uv sync
   ```

### Project Structure

```
whisper-voice-transcription/
├── main.py              # Main transcription script
├── .env                 # Environment configuration
├── inputs/              # Place audio files here
├── outputs/             # Transcription outputs (auto-created)
│   └── YYYYMMDD_HHMMSS/ # Timestamped folders
├── pyproject.toml       # Project dependencies
└── README.md           # This file
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

### Available Options

| Parameter          | Description        | Options                                             | Default      |
| ------------------ | ------------------ | --------------------------------------------------- | ------------ |
| `WHISPER_MODEL`    | Whisper model size | `tiny`, `base`, `small`, `medium`, `small.en` `...` |              |
| `WHISPER_LANGUAGE` | Language code      | `en`, `es`, `fr`, `de`, `bn`, etc.                  | auto-detect  |
| `WHISPER_TASK`     | Processing task    | `transcribe`, `translate`                           | `transcribe` |
| `WHISPER_FORMATS`  | Output formats     | `srt`, `txt`, `json`, `vtt`, `tsv`                  | `txt`        |

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

## 📁 Usage

### 1. Prepare Audio Files

Place your audio files in the `inputs/` folder:

```bash
cp english-voice-example.mp3 inputs/
```

### 2. Basic Usage

**Using .env defaults (simplest):**

```bash
uv run python main.py --audio english-voice-example.mp3
```

**Using Python directly:**

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

### 3. Advanced Usage

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

### 4. Command Line Arguments

```bash
python main.py [OPTIONS]

Options:
  --audio FILEPATH     Path to audio file (required)
  --model MODEL        Whisper model size (default from .env)
  --language CODE      Language code (default from .env or auto-detect)
  --task TASK          transcribe or translate (default from .env)
  --formats FORMATS    Comma-separated formats (default from .env)
  --device DEVICE      auto, cuda, or cpu (default from .env)
```

## � GPU Acceleration

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

## �📄 Output Formats

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

## 🔧 Development

### Dependencies

The project uses these main dependencies:

- `openai-whisper` - Core Whisper functionality
- `python-dotenv` - Environment variable loading
- `torch` - PyTorch (installed with Whisper)
- `ffmpeg-python` - Audio processing

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**"Audio file not found" error:**

- Check the file path is correct
- Ensure the file exists and is accessible

**FFmpeg errors:**

- Install FFmpeg using the instructions above
- Ensure FFmpeg is in your system PATH

**Out of memory errors:**

- Use a smaller model (`tiny`, `base`, `small`)
- Close other applications to free up RAM/VRAM
- Use CPU mode: `--device cpu`

**Slow transcription:**

- Use GPU if available: ensure CUDA is properly installed
- Choose a smaller model for faster processing
- Check if other processes are using GPU resources

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

If you encounter any issues or have questions, please:

1. Search existing issues
2. Create a new issue if not exist with detailed information

---

**Happy transcribing! 🎤✨**
