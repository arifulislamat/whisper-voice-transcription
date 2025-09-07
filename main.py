import argparse
import os
import shutil
from datetime import datetime
from transcription_core import transcribe_audio_core, SUPPORTED_FORMATS

def get_language_mapping():
    """Load language mapping from environment variables."""
    # Get languages from environment variable
    languages_str = os.getenv("WHISPER_LANGUAGES", "")
    
    if not languages_str:
        raise ValueError("WHISPER_LANGUAGES not found in .env file. Please check your .env configuration.")
    
    # Parse the string into a dictionary
    language_mapping = {}
    for pair in languages_str.split(','):
        if ':' in pair:
            display_name, code = pair.split(':', 1)
            language_mapping[display_name.strip()] = code.strip()
    
    if not language_mapping:
        raise ValueError("No valid language mappings found in WHISPER_LANGUAGES. Please check your .env configuration.")
    
    return language_mapping

def get_language_code(display_name):
    """Convert display language name to Whisper language code."""
    language_mapping = get_language_mapping()
    return language_mapping.get(display_name, "auto")

def save_audio_to_inputs(audio_file):
    """Save uploaded audio file to inputs folder."""
    if audio_file is None:
        return "❌ No audio file provided."
    
    try:
        # Ensure inputs directory exists
        os.makedirs("inputs", exist_ok=True)
        
        # Get the original filename from the audio file path
        from pathlib import Path
        
        source_path = Path(audio_file)
        filename = source_path.name
        
        # If the filename doesn't have an extension, add .wav
        if not filename.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.aac')):
            filename += '.wav'
        
        destination_path = os.path.join("inputs", filename)
        
        # Handle duplicate filenames
        counter = 1
        base_name = Path(filename).stem
        extension = Path(filename).suffix
        while os.path.exists(destination_path):
            new_filename = f"{base_name}_{counter}{extension}"
            destination_path = os.path.join("inputs", new_filename)
            counter += 1
        
        # Copy the file
        shutil.copy2(audio_file, destination_path)
        
        return f"✅ Saved audio as: {Path(destination_path).name}"
    
    except Exception as e:
        return f"❌ Error saving audio: {str(e)}"

def save_audio_and_update_dropdown(audio_file):
    """Save uploaded audio file and return updated dropdown with new file selected."""
    import gradio as gr
    
    # Save the audio file
    status = save_audio_to_inputs(audio_file)
    
    # Get updated choices
    updated_choices = get_audio_files_list()
    
    # Extract the saved filename from status message
    selected_filename = None
    if status.startswith("✅ Saved audio as:"):
        saved_filename = status.split(": ")[1]
        # Find the corresponding choice that contains this filename
        for choice in updated_choices:
            if choice.startswith(saved_filename):
                selected_filename = choice
                break
    
    return status, gr.Dropdown(choices=updated_choices, value=selected_filename)

def get_audio_files_list():
    """Get list of audio files from inputs folder with file info."""
    if not os.path.exists("inputs"):
        os.makedirs("inputs")
    
    files = []
    for file in os.listdir("inputs"):
        if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.aac')):
            file_path = os.path.join("inputs", file)
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)
            files.append(f"{file} ({size_mb:.1f} MB)")
    
    if not files:
        return ["No audio files found - upload or record something first"]
    return files

def display_audio_files():
    """Return a formatted string showing all available audio files."""
    files = get_audio_files_list()
    if files == ["No audio files found - upload or record something first"]:
        return "No audio files found in the inputs folder.\nUpload or record some audio to get started!"
    
    file_list_text = "Available audio files:\n"
    for i, file in enumerate(files, 1):
        file_list_text += f"{i}. {file}\n"
    file_list_text += f"\nTotal files: {len(files)}"
    return file_list_text

def delete_audio_file(filename):
    """Delete selected audio file from inputs folder."""
    if not filename or filename.startswith("No audio files found"):
        return "❌ No file selected for deletion."
    
    # Extract just the filename (remove size info)
    if '(' in filename and ')' in filename:
        actual_filename = filename.split(' (')[0]
    else:
        actual_filename = filename.strip()
    
    file_path = os.path.join("inputs", actual_filename)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"✅ Deleted: {actual_filename}"
        else:
            return f"❌ File not found: {actual_filename}"
    except Exception as e:
        return f"❌ Error deleting file: {str(e)}"

def delete_audio_file_and_refresh(filename):
    """Delete selected audio file and return updated dropdown, status, and clear audio input."""
    import gradio as gr
    status = delete_audio_file(filename)
    updated_choices = get_audio_files_list()
    
    # Clear audio input as well since the file might be loaded there
    cleared_audio = None
    
    return gr.Dropdown(choices=updated_choices, value=None), status, cleared_audio

def load_selected_file_to_audio_input(filename):
    """Load selected file from dropdown into audio input component."""
    if not filename or filename.startswith("No audio files found"):
        return None
    
    # Extract just the filename (remove size info)
    if '(' in filename and ')' in filename:
        actual_filename = filename.split(' (')[0]
    else:
        actual_filename = filename.strip()
    
    file_path = os.path.join("inputs", actual_filename)
    
    if os.path.exists(file_path):
        return file_path
    else:
        return None

def get_activity_logs():
    """Get list of all previous transcription jobs from outputs folder."""
    if not os.path.exists("outputs"):
        return []
    
    activities = []
    for folder in sorted(os.listdir("outputs"), reverse=True):  # Most recent first
        folder_path = os.path.join("outputs", folder)
        if os.path.isdir(folder_path):
            # Parse timestamp from folder name (YYYYMMDD_HHMMSS)
            try:
                from datetime import datetime
                timestamp = datetime.strptime(folder, "%Y%m%d_%H%M%S")
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # Get files in this output folder
                files = []
                audio_file = ""
                for file in os.listdir(folder_path):
                    if not file.endswith('.zip'):
                        files.append(file)
                        # Try to determine the original audio file name
                        if not audio_file:
                            base_name = os.path.splitext(file)[0]
                            audio_file = base_name
                
                if files:  # Only include folders with files
                    activity_info = f"{formatted_time} | {audio_file} | {len(files)} files | {folder}"
                    activities.append(activity_info)
            except ValueError:
                # Skip folders that don't match the timestamp format
                continue
    
    if not activities:
        return ["No previous transcription jobs found"]
    return activities

def load_activity_job(selected_activity):
    """Load selected transcription job into preview components."""
    if not selected_activity or selected_activity.startswith("No previous"):
        return "", "", "", "", "", "No job selected"
    
    # Extract folder name from activity info (last part after |)
    try:
        folder_name = selected_activity.split(" | ")[-1]
        folder_path = os.path.join("outputs", folder_name)
        
        if not os.path.exists(folder_path):
            return "", "", "", "", "", f"❌ Job folder not found: {folder_name}"
        
        # Read all output files
        txt_content = ""
        srt_content = ""
        vtt_content = ""
        tsv_content = ""
        json_content = ""
        
        for file in os.listdir(folder_path):
            if file.endswith('.zip'):
                continue
                
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if file.endswith('.txt'):
                        txt_content = content
                    elif file.endswith('.srt'):
                        srt_content = content
                    elif file.endswith('.vtt'):
                        vtt_content = content
                    elif file.endswith('.tsv'):
                        tsv_content = content
                    elif file.endswith('.json'):
                        json_content = content
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        return txt_content, srt_content, vtt_content, tsv_content, json_content, f"✅ Loaded job: {folder_name}"
    
    except Exception as e:
        return "", "", "", "", "", f"❌ Error loading job: {str(e)}"

def launch_gradio_interface():
    """Launch the Gradio web interface."""
    try:
        import gradio as gr
        from pathlib import Path
    except ImportError:
        print("❌ Error: Gradio is not installed. Please run: uv add gradio")
        return 1

    def gradio_transcribe(audio_file, selected_file, model, language, task, formats, device):
        """Gradio interface function for audio transcription."""
        try:
            # Determine which audio source to use
            audio_path = None
            
            if selected_file and selected_file.strip() and not selected_file.startswith("No audio files found"):
                # Use selected file from inputs folder
                # Check if it's just a filename or has size info
                if '(' in selected_file and ')' in selected_file:
                    # Extract filename from "filename (size)" format
                    actual_filename = selected_file.split(' (')[0]
                else:
                    # It's just the filename
                    actual_filename = selected_file.strip()
                
                audio_path = os.path.join("inputs", actual_filename)
                if not os.path.exists(audio_path):
                    return f"❌ Selected file not found: {actual_filename}", "", "", "", "", ""
            elif audio_file is not None:
                # Save uploaded/recorded audio and use it
                saved_result = save_audio_to_inputs(audio_file)
                if saved_result.startswith("✅"):
                    # Extract filename from the success message
                    filename = saved_result.split(": ")[1]
                    audio_path = os.path.join("inputs", filename)
                else:
                    return saved_result, "", "", "", "", ""
            else:
                return "❌ Please upload an audio file, record audio, or select an existing file.", "", "", "", "", ""
            
            if not formats:
                return "❌ Please select at least one output format.", "", "", "", "", ""
            
            # Convert display language name to language code
            language_code = get_language_code(language)
            
            # Use the transcription core
            result = transcribe_audio_core(audio_path, model, language_code, task, formats, device)
            
            # transcribe_audio_core returns a dict with output_dir, files, etc.
            # No need to check for "success" key since function raises exceptions on error
            output_path = result["output_dir"]
            
            # Read preview files
            txt_content = ""
            srt_content = ""
            vtt_content = ""
            tsv_content = ""
            json_content = ""
            
            # Look for output files
            for file in os.listdir(output_path):
                file_path = os.path.join(output_path, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if file.endswith('.txt'):
                            txt_content = content
                        elif file.endswith('.srt'):
                            srt_content = content
                        elif file.endswith('.vtt'):
                            vtt_content = content
                        elif file.endswith('.tsv'):
                            tsv_content = content
                        elif file.endswith('.json'):
                            json_content = content
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            return (
                f"✅ Transcription completed! Output saved to: {output_path}",
                txt_content,
                srt_content,
                vtt_content,
                tsv_content,
                json_content
            )
                
        except Exception as e:
            return f"❌ Error during transcription: {str(e)}", "", "", "", "", ""

    # Create the Gradio interface
    with gr.Blocks(title="🎤 Whisper Voice Transcription") as interface:
        gr.Markdown("# 🎤 Whisper Voice Transcription")
        gr.Markdown("Upload audio files or record directly to get accurate transcriptions using OpenAI's Whisper model.")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🎵 Audio Input")
                
                # Audio input with proper sources configuration
                audio_input = gr.Audio(
                    label="🎤 Upload or Record Audio",
                    sources=["upload", "microphone"],
                    type="filepath"
                )
                
                gr.Markdown("---")
                gr.Markdown("### 📁 Audio File Manager")
                
                # File management components
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Refresh List", size="sm")
                    delete_btn = gr.Button("🗑️ Delete Selected", size="sm", variant="secondary")
                
                # File selector as dropdown
                selected_file_input = gr.Dropdown(
                    label="📝 Selected File",
                    choices=get_audio_files_list(),
                    value=None,
                    info="Select a file from inputs folder or leave empty to use uploaded/recorded audio above"
                )
                
                file_status = gr.Textbox(
                    label="🙈 File Status", 
                    placeholder="File operations will be shown here...",
                    lines=2,
                    max_lines=3,
                    interactive=False
                )
                
                gr.Markdown("---")
                gr.Markdown("### 🏃🏻 Activity Logs")
                
                with gr.Row():
                    refresh_logs_btn = gr.Button("🔄 Refresh Logs", size="sm")
                
                # Activity list
                activity_list = gr.Dropdown(
                    label="📅 Job History",
                    choices=get_activity_logs(),
                    value=None,
                    info="Select a previous job to automatically load its results"
                )
                
                activity_status = gr.Textbox(
                    label="🙈 Load Status",
                    placeholder="Select a job from the dropdown to automatically view results...",
                    lines=2,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 👂 Whisper Model Setup")
                
                model_input = gr.Dropdown(
                    choices=["tiny.en", "base.en", "small.en", "medium.en", "tiny", "base", "small", "medium" "large", "turbo"],
                    value=os.getenv("WHISPER_MODEL", "small.en"),
                    label="🏋️‍♂️ Model Sizes"
                )
                
                # Determine default language for dropdown
                language_mapping = get_language_mapping()
                env_language_code = os.getenv("WHISPER_LANGUAGE", "auto")
                # Find display name for env_language_code
                default_language_display = None
                for display, code in language_mapping.items():
                    if code == env_language_code:
                        default_language_display = display
                        break
                if not default_language_display:
                    default_language_display = "Auto Detect"
                language_input = gr.Dropdown(
                    choices=list(language_mapping.keys()),
                    value=default_language_display,
                    label="🌍 Language"
                )
                task_input = gr.Radio(
                    choices=["transcribe", "translate"],
                    value=os.getenv("WHISPER_TASK", "transcribe"),
                    label="📝 Task",
                    info="Transcribe: Convert speech to text in original language | Translate: Convert speech to English text (from any language)"
                )
                
                formats_input = gr.CheckboxGroup(
                    choices=SUPPORTED_FORMATS,
                    value=os.getenv("WHISPER_FORMATS", "srt,txt,json").split(","),
                    label="📄 Output Formats"
                )
                
                device_input = gr.Radio(
                    choices=["auto", "cuda", "cpu"],
                    value=os.getenv("WHISPER_DEVICE", "auto"),
                    label="⚙️ Processing Device"
                )
                
                transcribe_btn = gr.Button("✍️ Start Transcription", variant="primary", size="lg")
                
                status_output = gr.Textbox(
                    label="🙈 Transcription Status",
                    placeholder="Ready to transcribe...",
                    lines=2,
                    interactive=False
                )

                gr.Markdown("---")
                
                with gr.Tabs():
                    with gr.Tab("📄 TXT"):
                        txt_preview = gr.Textbox(
                            label="Plain Text Output",
                            lines=10,
                            max_lines=20,
                            interactive=False,
                            placeholder="Transcribed text will appear here..."
                        )
                    
                    with gr.Tab("🎬 SRT"):
                        srt_preview = gr.Textbox(
                            label="SRT Subtitle Output",
                            lines=10,
                            max_lines=20,
                            interactive=False,
                            placeholder="SRT subtitle format will appear here..."
                        )
                    
                    with gr.Tab("🌐 VTT"):
                        vtt_preview = gr.Textbox(
                            label="VTT Subtitle Output",
                            lines=10,
                            max_lines=20,
                            interactive=False,
                            placeholder="WebVTT format will appear here..."
                        )
                    
                    with gr.Tab("📊 TSV"):
                        tsv_preview = gr.Textbox(
                            label="TSV Data Output",
                            lines=10,
                            max_lines=20,
                            interactive=False,
                            placeholder="Tab-separated values will appear here..."
                        )
                    
                    with gr.Tab("🔧 JSON"):
                        json_preview = gr.Textbox(
                            label="JSON Output",
                            lines=10,
                            max_lines=20,
                            interactive=False,
                            placeholder="JSON format will appear here..."
                        )
        
        # Connect the transcribe button to the function
        transcribe_btn.click(
            fn=gradio_transcribe,
            inputs=[audio_input, selected_file_input, model_input, language_input, task_input, formats_input, device_input],
            outputs=[status_output, txt_preview, srt_preview, vtt_preview, tsv_preview, json_preview]
        ).then(
            # Refresh activity logs after transcription
            fn=lambda: gr.Dropdown(choices=get_activity_logs()),
            outputs=activity_list
        )
        
        # Connect file management buttons
        refresh_btn.click(
            fn=lambda: gr.Dropdown(choices=get_audio_files_list()),
            outputs=selected_file_input
        )
        
        delete_btn.click(
            fn=delete_audio_file_and_refresh,
            inputs=selected_file_input,
            outputs=[selected_file_input, file_status, audio_input]
        )
        
        # Auto-save uploaded audio and refresh file list
        audio_input.upload(
            fn=save_audio_and_update_dropdown,
            inputs=audio_input,
            outputs=[file_status, selected_file_input]
        )
        
        # Load selected file into audio input when dropdown selection changes
        selected_file_input.change(
            fn=load_selected_file_to_audio_input,
            inputs=selected_file_input,
            outputs=audio_input
        )
        
        # Activity logs event handlers
        refresh_logs_btn.click(
            fn=lambda: gr.Dropdown(choices=get_activity_logs()),
            outputs=activity_list
        )
        
        # Auto-load job when selected from dropdown
        activity_list.change(
            fn=load_activity_job,
            inputs=activity_list,
            outputs=[txt_preview, srt_preview, vtt_preview, tsv_preview, json_preview, activity_status]
        )
        
        gr.Markdown("---")
        gr.Markdown("### 💡 Tips:")
        gr.Markdown("• **English audio**: Use `.en` models for better performance")
        gr.Markdown("• **Limited GPU memory**: Start with `tiny` or `base` models")
        gr.Markdown("• **Best quality**: Use `large` or `turbo` models")
        gr.Markdown("• **Multiple formats**: Select multiple checkboxes to get a zip file")

    print("🌐 Starting Gradio web interface...")
    print("📱 The interface will be available in your browser")
    
    # Get share setting from environment variable
    share_enabled = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=share_enabled,
        inbrowser=True
    )
    return 0

def run_cli_mode(args):
    """Run transcription in CLI mode."""
    print("🎤 Starting Whisper Voice Transcription (CLI Mode)")
    print(f"📁 Audio file: {args.audio}")
    print(f"🤖 Model: {args.model}")
    print(f"🌍 Language: {args.language}")
    print(f"📝 Task: {args.task}")
    # Handle formats display - it could be a string or list
    if isinstance(args.formats, str):
        print(f"📄 Formats: {args.formats}")
    else:
        print(f"📄 Formats: {', '.join(args.formats)}")
    print(f"⚙️ Device: {args.device}")
    print("-" * 50)
    
    # Check if audio file exists
    if not os.path.exists(args.audio):
        print(f"❌ Error: Audio file '{args.audio}' not found.")
        return 1
    
    # Use the transcription core
    try:
        result = transcribe_audio_core(args.audio, args.model, args.language, args.task, args.formats, args.device)
        print(f"✅ Transcription completed successfully!")
        print(f"📁 Output directory: {result['output_dir']}")
        return 0
    except Exception as e:
        print(f"❌ Transcription failed: {str(e)}")
        return 1

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="🎤 Whisper Voice Transcription Tool")
    
    # Web interface flag
    parser.add_argument("--web", action="store_true", help="Launch web interface instead of CLI")
    
    # CLI arguments
    parser.add_argument("--audio", default=os.getenv("WHISPER_AUDIO", ""), help="Path to audio file")
    parser.add_argument("--model", default=os.getenv("WHISPER_MODEL", "small.en"), help="Whisper model to use")
    parser.add_argument("--language", default=os.getenv("WHISPER_LANGUAGE", "auto"), help="Audio language")
    parser.add_argument("--task", default=os.getenv("WHISPER_TASK", "transcribe"), choices=["transcribe", "translate"], help="Task type")
    parser.add_argument("--formats", default=os.getenv("WHISPER_FORMATS", "srt,txt,json"), help="Output formats (comma-separated)")
    parser.add_argument("--device", default=os.getenv("WHISPER_DEVICE", "auto"), help="Processing device")
    
    args = parser.parse_args()
    
    if args.web:
        return launch_gradio_interface()
    else:
        if not args.audio:
            print("❌ Error: --audio argument is required for CLI mode")
            print("💡 Use --web flag to launch the web interface instead")
            return 1
        return run_cli_mode(args)

if __name__ == "__main__":
    exit(main())
