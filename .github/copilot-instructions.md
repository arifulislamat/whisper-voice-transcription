# Copilot Instructions for Whisper Voice Transcription

## Project Architecture

This is a **single-script audio transcription tool** using OpenAI's Whisper model. The architecture is deliberately simple:

- **`main.py`**: Core transcription logic with CLI interface
- **`.env`**: Configuration defaults (overridable via CLI)
- **`inputs/`**: Audio file staging area (optional - can transcribe from anywhere)
- **`outputs/YYYYMMDD_HHMMSS/`**: Timestamped output folders with multiple formats

## Key Development Patterns

### Environment-First Configuration

All CLI arguments have `.env` defaults. The pattern is:

```python
parser.add_argument("--model", default=os.getenv("WHISPER_MODEL", "small.en"))
```

This allows users to set preferences in `.env` but override per-run. Always maintain this dual-source pattern.

### Device Detection & Fallback Strategy

The `get_device()` function implements smart GPU/CPU selection:

- `auto`: CUDA → CPU fallback
- `cuda`: Force GPU with CPU fallback on failure
- `cpu`: Force CPU only

**Critical**: Always wrap model loading in try/catch for CUDA fallback:

```python
try:
    model = whisper.load_model(args.model, device=device)
except Exception as e:
    if device == "cuda":
        # Fallback to CPU logic
```

### Output Format Architecture

Each format (SRT, TXT, JSON, VTT, TSV) has its own `save_*()` function. When adding formats:

1. Add to `SUPPORTED_FORMATS` list
2. Create `save_FORMAT()` function
3. Add elif branch in main loop
4. Update README format examples

### Timestamped Output Organization

Outputs use `YYYYMMDD_HHMMSS` folders to prevent overwrites. Pattern:

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join("outputs", timestamp)
```

## Development Workflows

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
