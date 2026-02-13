#!/usr/bin/env python3
"""
YouTube Video Clipping Script for Instagram Reels
Video: "I Made an Apple Shortcuts MCP" by littlehakr
Duration: 6:51

Usage:
1. Download the video first (use yt-dlp, browser extension, or online tool)
2. Save as 'apple_shortcuts_mcp_original.mp4' in the same directory
3. Run: python create_instagram_clips.py
"""

import subprocess
import os
import sys
from pathlib import Path

# Configuration
VIDEO_URL = "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
OUTPUT_DIR = Path("./instagram_clips")
INPUT_FILE = "apple_shortcuts_mcp_original.mp4"

# Clip definitions: (start_seconds, end_seconds, name, description)
CLIPS = [
    (0, 30, "clip1_hook", "THE HOOK - Introduction to MCP + Apple Shortcuts"),
    (60, 105, "clip2_demo", "THE DEMO - AI Creating Shortcuts in Real-Time"),
    (150, 195, "clip3_gemini", "GEMINI CLI - Cross-Platform AI Demo"),
    (240, 285, "clip4_usecase", "USE CASE - Practical Time-Saving Demo"),
    (330, 380, "clip5_future", "FUTURE - AI Automation Possibilities"),
]

def format_time(seconds):
    """Convert seconds to MM:SS format"""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins}:{secs:02d}"

def run_ffmpeg(cmd, description="Running ffmpeg"):
    """Run an ffmpeg command with error handling"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def create_clip(input_file, start, end, output_name, description):
    """Create a single clip from the video"""
    print(f"\n📹 Creating {output_name}")
    print(f"   Description: {description}")
    print(f"   Time: {format_time(start)} - {format_time(end)}")
    
    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    instagram_path = OUTPUT_DIR / f"{output_name}_instagram.mp4"
    
    # Create standard clip
    cmd = [
        "ffmpeg", "-i", input_file,
        "-ss", format_time(start),
        "-to", format_time(end),
        "-c:v", "libx264", "-c:a", "aac",
        "-preset", "fast", "-crf", "23",
        "-y", str(output_path)
    ]
    
    if not run_ffmpeg(cmd):
        return False
    
    print(f"   ✓ Created {output_name}.mp4")
    
    # Create Instagram vertical version (9:16 aspect ratio)
    cmd_instagram = [
        "ffmpeg", "-i", str(output_path),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
        "-c:v", "libx264", "-c:a", "aac",
        "-preset", "fast", "-crf", "23",
        "-y", str(instagram_path)
    ]
    
    if run_ffmpeg(cmd_instagram):
        print(f"   ✓ Created {output_name}_instagram.mp4 (9:16 vertical)")
    
    return True

def main():
    print("=" * 50)
    print("  YouTube Video Clipping Script")
    print("  Video: I Made an Apple Shortcuts MCP")
    print("=" * 50)
    
    # Check for ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ffmpeg not found. Please install ffmpeg first.")
        sys.exit(1)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"\n⚠️  Input file '{INPUT_FILE}' not found!")
        print("\nTo download the video, use one of these methods:")
        print("\n1. yt-dlp (recommended):")
        print(f"   pip install yt-dlp")
        print(f"   yt-dlp -o {INPUT_FILE} '{VIDEO_URL}'")
        print("\n2. Browser extension:")
        print("   Install 'Video DownloadHelper' and download from YouTube")
        print("\n3. Online tool:")
        print("   Visit y2mate.com or savefrom.net")
        print("\nSave the downloaded file as: " + INPUT_FILE)
        print("\nThen run this script again.")
        sys.exit(1)
    
    print(f"\n✅ Found input file: {INPUT_FILE}")
    print(f"\n🎬 Creating {len(CLIPS)} clips...")
    
    success_count = 0
    for start, end, name, desc in CLIPS:
        if create_clip(INPUT_FILE, start, end, name, desc):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"  ✅ Created {success_count}/{len(CLIPS)} clips successfully!")
    print("=" * 50)
    
    # List output files
    print(f"\n📁 Output files in {OUTPUT_DIR}:")
    for f in sorted(OUTPUT_DIR.glob("*.mp4")):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"   {f.name}: {size_mb:.1f} MB")
    
    print("\n🎯 Next Steps:")
    print("1. Review each clip")
    print("2. Add text overlays in Instagram or editing app")
    print("3. Add trending audio/music")
    print("4. Post with optimized hashtags!")
    
    print("\n📝 Suggested Captions:")
    print("\nClip 1 (Hook):")
    print('   "🤯 I made AI create Apple Shortcuts from scratch!"')
    print("\nClip 2 (Demo):")
    print('   "Watch AI build a shortcut in SECONDS! 💪"')
    print("\nClip 3 (Gemini):")
    print('   "Using Gemini CLI to control Apple Shortcuts 🧙‍♂️"')
    print("\nClip 4 (Use Case):")
    print('   "This would take HOURS manually... AI did it in seconds! 🚀"')
    print("\nClip 5 (Future):")
    print('   "The future of AI automation is HERE! 🔮"')

if __name__ == "__main__":
    main()
