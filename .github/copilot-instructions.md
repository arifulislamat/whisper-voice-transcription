# Copilot Instructions for Whisper Voice Transcription

## Project Architecture & Data Flow

This project is a **single-script, environment-driven audio transcription tool** using OpenAI's Whisper model. It is designed for simplicity, reliability, and ease of extension:

- **`main.py`**: Unified CLI and Gradio web interface. Handles all user interaction, argument parsing, and workflow orchestration.
- **`transcription_core.py`**: Core transcription logic, device selection, and output format handling. All format-specific logic is here.
- **`.env`**: Central config for all defaults (model, language, device, formats, etc). CLI args always override `.env`.
- **`inputs/`**: Audio file staging (optional, not required for CLI).
- **`outputs/YYYYMMDD_HHMMSS/`**: Timestamped output folders, one per run, containing all requested formats.

**Data flow:**

1. User provides audio (via CLI, web upload, or file picker)
2. `main.py` parses config, launches transcription via `transcription_core.py`
3. Output files are written to a new timestamped folder in `outputs/`
4. Web UI and CLI both use the same core logic and output conventions

## Critical Development Patterns

### Environment-First, CLI-Override Configuration

All CLI arguments default to `.env` values. Always use:

```python
parser.add_argument("--model", default=os.getenv("WHISPER_MODEL", "small.en"))
```

Never hardcode config defaults elsewhere.

### Device Detection & Fallback

Use `get_device()` from `transcription_core.py`:

- `auto`: Prefer CUDA, fallback to CPU
- `cuda`: Force GPU, fallback to CPU on error
- `cpu`: Force CPU only
  **Always** wrap model loading in try/except for CUDA fallback:

```python
try:
    model = whisper.load_model(model_name, device=device)
except Exception as e:
    if device == "cuda":
        # Fallback to CPU
```

### Output Format Extension

To add a new output format:

1. Add to `SUPPORTED_FORMATS` in `transcription_core.py`
2. Implement `save_FORMAT()` in `transcription_core.py`
3. Add to output logic in `transcribe_audio_core()`
4. Update README with format example

### Timestamped Output Folders

All outputs go to `outputs/YYYYMMDD_HHMMSS/` to avoid overwrites. Use:

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join("outputs", timestamp)
```

### Web & CLI Parity

Both interfaces use the same core logic and config. Web UI (Gradio) is in `main.py` and mirrors CLI options.

## Developer Workflows

### Install & Run

- Install dependencies: `uv sync` (CPU) or `uv sync --extra cu128` (CUDA, after editing `pyproject.toml`)
- Run CLI: `uv run python main.py --audio file.mp3`
- Run Web UI: `uv run python main.py --web`

### Audio File Handling

- Audio can be anywhere for CLI (`--audio /path/to/file.mp3`)
- Web UI saves uploads to `inputs/` and manages duplicates

### Adding Languages

- Update `WHISPER_LANGUAGES` in `.env` for dropdowns
- Use `get_language_mapping()` in `main.py` for mapping

### Error Handling

- Device fallback is permissive (GPU errors → CPU)
- File and format validation is strict: invalid files or formats are skipped with clear errors

## Project-Specific Conventions

- All config is `.env`-driven, never hardcoded
- Output filenames match input: `audio.mp3` → `audio.srt`, `audio.txt`, etc.
- All new formats must have a `save_FORMAT()`
- Timestamps always use `YYYYMMDD_HHMMSS`
- No global state: all logic is function-based

## Integration Points

- **Whisper**: Always load with explicit device
- **PyTorch**: Used for CUDA detection, installed via Whisper
- **FFmpeg**: Required for audio, must be installed system-wide
- **Gradio**: Web UI only, not required for CLI

## Example: Add a New Output Format

1. Add to `SUPPORTED_FORMATS` in `transcription_core.py`
2. Implement `save_newformat()`
3. Add to output logic in `transcribe_audio_core()`
4. Update README with example

---

For more, see `README.md` for usage, troubleshooting, and advanced examples.

### Package Management (uv-based)

```bash
# Install dependencies
uv sync

# Run transcription
uv run python main.py --audio file.mp3

# Add new dependency
uv add package-name
```

### Testing GPU/CPU Modes

```bash
# Test GPU detection
uv run python main.py --audio test.mp3 --device auto

# Force CPU (for debugging)
uv run python main.py --audio test.mp3 --device cpu

# Test CUDA with fallback
uv run python main.py --audio test.mp3 --device cuda
```

### Audio File Placement

Audio files can be:

- Placed in `inputs/` (convention, not required)
- Referenced from anywhere with `--audio /full/path/file.mp3`
- Root directory has sample files: `english-voice-example.mp3`, `bangla-voice-example.mp3`

## Critical Dependencies

- **`openai-whisper>=20250625`**: Core transcription engine
- **`python-dotenv>=1.1.1`**: Environment variable loading
- **PyTorch**: Auto-installed with Whisper, handles CUDA detection
- **FFmpeg**: External dependency for audio processing (not in pyproject.toml)

## Project-Specific Conventions

### Error Handling Philosophy

- **Permissive device fallback**: GPU errors fall back to CPU
- **File validation**: Check audio file existence before processing
- **Format validation**: Filter invalid formats, continue with valid ones

### Configuration Hierarchy

1. CLI arguments (highest priority)
2. `.env` values
3. Code defaults (lowest priority)

### Naming Patterns

- Output files use original filename: `audio.mp3` → `audio.srt`, `audio.txt`, etc.
- Functions follow `save_FORMAT()` naming
- Timestamps follow `YYYYMMDD_HHMMSS` format

## Integration Points

### Whisper Model Loading

```python
# Always specify device explicitly
model = whisper.load_model(model_name, device=device)
```

### FFmpeg Integration

- Required for audio preprocessing
- Handled transparently by Whisper
- Installation varies by OS (documented in README)

### CUDA Detection

```python
torch.cuda.is_available()  # Check availability
torch.cuda.get_device_name(0)  # Get GPU name
torch.cuda.get_device_properties(0).total_memory  # Get VRAM
```

This codebase prioritizes **simplicity and reliability** over complex architecture. When extending, maintain the single-script approach and environment-configurable defaults pattern.
