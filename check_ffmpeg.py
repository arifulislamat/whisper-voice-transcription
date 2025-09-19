#!/usr/bin/env python3
"""
FFmpeg availability checker for Whisper Voice Transcription
Run this script to diagnose FFmpeg installation issues on Windows.
"""

import subprocess
import platform
import sys
import os

def check_ffmpeg():
    """Check if FFmpeg is available and provide detailed diagnostics."""
    print("🔍 Checking FFmpeg availability...")
    print(f"🖥️  Operating System: {platform.system()} {platform.release()}")
    print(f"🐍 Python Version: {sys.version}")
    print()
    
    try:
        # Try to run ffmpeg
        print("⏳ Testing FFmpeg command...")
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg is working correctly!")
            
            # Extract version info
            lines = result.stdout.split('\n')
            version_line = lines[0] if lines else "Unknown version"
            print(f"📦 {version_line}")
            
            # Check configuration
            config_line = None
            for line in lines:
                if 'configuration:' in line:
                    config_line = line
                    break
            
            if config_line:
                print("🔧 Configuration found (audio codecs should be available)")
            
            print("\n🎉 Your system is ready for audio transcription!")
            return True
            
        else:
            print(f"❌ FFmpeg command failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg not found in system PATH")
        print_ffmpeg_installation_help()
        return False
        
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def print_ffmpeg_installation_help():
    """Print platform-specific installation instructions."""
    system = platform.system()
    print("\n🔧 FFmpeg Installation Guide:")
    
    if system == "Windows":
        print("""
📥 Windows Installation Options:

Option 1 - Direct Download (Recommended):
1. Go to: https://www.gyan.dev/ffmpeg/builds/
2. Download the latest 'release' build (ZIP file)
3. Extract to C:\\ffmpeg (or any folder you prefer)
4. Add C:\\ffmpeg\\bin to your Windows PATH:
   • Press Win + R, type 'sysdm.cpl', press Enter
   • Click 'Environment Variables'
   • Under 'System Variables', find 'Path', click 'Edit'
   • Click 'New' and add 'C:\\ffmpeg\\bin'
   • Click OK to close all dialogs
5. Restart your Command Prompt/Terminal
6. Test by running: ffmpeg -version

Option 2 - Package Managers:
• Chocolatey: choco install ffmpeg
• Winget: winget install FFmpeg

⚠️  After installation, you MUST restart your terminal!
""")
    
    elif system == "Darwin":  # macOS
        print("""
📥 macOS Installation:
• Using Homebrew: brew install ffmpeg
• Using MacPorts: sudo port install ffmpeg
""")
    
    else:  # Linux
        print("""
📥 Linux Installation:
• Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg
• CentOS/RHEL: sudo yum install ffmpeg
• Arch Linux: sudo pacman -S ffmpeg
• Fedora: sudo dnf install ffmpeg
""")

def check_path_environment():
    """Check PATH environment variable for common issues."""
    print("\n🔍 Checking PATH environment...")
    
    path_var = os.environ.get('PATH', '')
    path_dirs = path_var.split(os.pathsep)
    
    print(f"📁 PATH contains {len(path_dirs)} directories")
    
    # Look for common FFmpeg installation paths
    common_ffmpeg_paths = [
        'C:\\ffmpeg\\bin',
        'C:\\Program Files\\ffmpeg\\bin',
        '/usr/bin',
        '/usr/local/bin',
        '/opt/homebrew/bin'
    ]
    
    found_paths = []
    for path in common_ffmpeg_paths:
        if path in path_dirs:
            found_paths.append(path)
    
    if found_paths:
        print(f"✅ Found potential FFmpeg paths in PATH: {', '.join(found_paths)}")
    else:
        print("⚠️  No common FFmpeg paths found in PATH")
        
        # Check if FFmpeg exists in common locations
        for path in common_ffmpeg_paths:
            ffmpeg_exe = os.path.join(path, 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg')
            if os.path.exists(ffmpeg_exe):
                print(f"💡 Found FFmpeg at {ffmpeg_exe} but it's not in PATH!")
                print(f"   Add {path} to your PATH environment variable.")

def main():
    """Main diagnostic routine."""
    print("🎤 Whisper Voice Transcription - FFmpeg Checker")
    print("=" * 50)
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Check PATH environment
    check_path_environment()
    
    print("\n" + "=" * 50)
    
    if ffmpeg_ok:
        print("🎉 All checks passed! You're ready to use Whisper transcription.")
        print("\n🚀 Next steps:")
        print("   • Run: python main.py --web (for web interface)")
        print("   • Or: python main.py --audio your_file.mp3 (for CLI)")
    else:
        print("❌ FFmpeg issues detected. Please install FFmpeg and try again.")
        print("\n🔄 After installing FFmpeg:")
        print("   • Restart your terminal/command prompt")
        print("   • Run this checker again: python check_ffmpeg.py")
    
    return 0 if ffmpeg_ok else 1

if __name__ == "__main__":
    exit(main())
