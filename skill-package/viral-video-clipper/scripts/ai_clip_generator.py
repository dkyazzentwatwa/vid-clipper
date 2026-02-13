#!/usr/bin/env python3
"""
AI-Powered Video Clipper
Automatically identifies and creates viral-worthy clips from YouTube videos using Claude AI.

Usage:
    python ai_clip_generator.py <youtube_url>

Example:
    python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
"""

import subprocess
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import argparse


def parse_youtube_url(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def download_video(url, video_id, output_dir):
    """Download video using yt-dlp with cookie fallbacks"""
    print("\n📥 Downloading video...")
    print(f"   Video ID: {video_id}")

    video_path = output_dir / "original.mp4"
    metadata_path = output_dir / "metadata.json"

    # Try multiple download methods
    download_methods = [
        {
            "name": "Chrome cookies",
            "cmd": [
                "yt-dlp",
                "--cookies-from-browser", "chrome",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--write-info-json",
                "-o", str(video_path),
                url
            ]
        },
        {
            "name": "Firefox cookies",
            "cmd": [
                "yt-dlp",
                "--cookies-from-browser", "firefox",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--write-info-json",
                "-o", str(video_path),
                url
            ]
        },
        {
            "name": "No cookies",
            "cmd": [
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--write-info-json",
                "-o", str(video_path),
                url
            ]
        }
    ]

    for method in download_methods:
        print(f"\n   Trying: {method['name']}...")
        try:
            result = subprocess.run(
                method['cmd'],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"   ✓ Download successful!")

            # Read metadata
            info_json_path = output_dir / "original.info.json"
            if info_json_path.exists():
                with open(info_json_path, 'r') as f:
                    metadata = json.load(f)

                # Extract relevant metadata
                clean_metadata = {
                    "video_id": video_id,
                    "title": metadata.get("title", "Unknown"),
                    "duration": metadata.get("duration", 0),
                    "uploader": metadata.get("uploader", "Unknown"),
                    "upload_date": metadata.get("upload_date", "Unknown"),
                    "view_count": metadata.get("view_count", 0),
                    "description": metadata.get("description", "")[:500]  # First 500 chars
                }

                with open(metadata_path, 'w') as f:
                    json.dump(clean_metadata, f, indent=2)

                print(f"   Title: {clean_metadata['title']}")
                print(f"   Duration: {clean_metadata['duration']}s")

                return video_path, clean_metadata

            return video_path, {"video_id": video_id}

        except subprocess.CalledProcessError as e:
            print(f"   ✗ Failed: {e.stderr[:200]}")
            continue
        except FileNotFoundError:
            print(f"   ✗ yt-dlp not found. Install with: pip install yt-dlp")
            sys.exit(1)

    print("\n❌ All download methods failed!")
    print("\nManual download instructions:")
    print(f"1. Visit: {url}")
    print(f"2. Download the video manually")
    print(f"3. Save as: {video_path}")
    print(f"4. Run this script again")
    sys.exit(1)


def transcribe_video(video_path, output_dir):
    """Transcribe video using Whisper"""
    print("\n🎙️  Transcribing video...")

    transcript_json = output_dir / "original.json"

    # Check if transcription already exists
    if transcript_json.exists():
        print("   ✓ Found existing transcription")
        with open(transcript_json, 'r') as f:
            return json.load(f)

    # Check if whisper is available
    try:
        subprocess.run(["whisper", "--help"], capture_output=True, check=True)
    except FileNotFoundError:
        print("   ✗ Whisper not found. Install with: pip install openai-whisper")
        sys.exit(1)

    # Try base model first, fallback to tiny if it fails
    models = ["base", "tiny"]

    for model in models:
        print(f"   Trying Whisper model: {model}...")
        try:
            cmd = [
                "whisper",
                str(video_path),
                "--model", model,
                "--output_format", "json",
                "--output_dir", str(output_dir)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=str(output_dir)
            )

            print(f"   ✓ Transcription complete with {model} model")

            # Load and return the transcript
            if transcript_json.exists():
                with open(transcript_json, 'r') as f:
                    return json.load(f)
            else:
                print(f"   ✗ Warning: Transcript file not created")
                if model == models[-1]:
                    print(f"\n❌ Transcription failed: Output file not found")
                    sys.exit(1)
                continue

        except subprocess.CalledProcessError as e:
            print(f"   ✗ Failed with {model} model")
            if model == models[-1]:  # Last model
                print(f"\n❌ Transcription failed: {e.stderr[:200]}")
                sys.exit(1)
            continue


def format_transcript_for_claude(transcript_data):
    """Format Whisper transcript with timestamps for Claude analysis"""
    formatted_lines = []

    for segment in transcript_data.get("segments", []):
        timestamp = segment.get("start", 0)
        text = segment.get("text", "").strip()

        # Format as [MM:SS] text
        mins = int(timestamp // 60)
        secs = int(timestamp % 60)
        formatted_lines.append(f"[{mins:02d}:{secs:02d}] {text}")

    return "\n".join(formatted_lines)


def generate_analysis_prompt(transcript_data, metadata, output_dir):
    """Generate Claude analysis prompt from template"""
    print("\n📝 Generating Claude analysis prompt...")

    template_path = Path(__file__).parent / "prompt_templates" / "clip_analysis_prompt.md"

    if not template_path.exists():
        print(f"   ✗ Template not found: {template_path}")
        sys.exit(1)

    with open(template_path, 'r') as f:
        template = f.read()

    # Format metadata
    metadata_str = f"""
- **Title**: {metadata.get('title', 'Unknown')}
- **Duration**: {metadata.get('duration', 0)} seconds
- **Uploader**: {metadata.get('uploader', 'Unknown')}
- **Video ID**: {metadata.get('video_id', 'Unknown')}
"""

    # Format transcript
    transcript_str = format_transcript_for_claude(transcript_data)

    # Replace placeholders
    prompt = template.replace("{metadata}", metadata_str.strip())
    prompt = prompt.replace("{transcript}", transcript_str)

    # Save prompt
    prompt_path = output_dir / "analysis_request.md"
    with open(prompt_path, 'w') as f:
        f.write(prompt)

    print(f"   ✓ Prompt saved to: {prompt_path}")
    return prompt_path


def invoke_claude_analysis(prompt_path, output_path):
    """Invoke Claude Code for analysis (interactive mode)"""
    # Check if recommendations already exist
    if output_path.exists():
        print("\n✓ Found existing clip recommendations")
        return

    print("\n🤖 Claude AI Analysis Required")
    print("=" * 60)
    print("\nNext steps:")
    print(f"1. Review the analysis prompt at:")
    print(f"   {prompt_path}")
    print(f"\n2. Run Claude Code on this prompt to generate clip recommendations")
    print(f"\n3. Save Claude's JSON output to:")
    print(f"   {output_path}")
    print(f"\n4. Press Enter when the JSON file is ready...")
    print("=" * 60)

    input("\nPress Enter to continue...")

    # Validate output exists
    if not output_path.exists():
        print(f"\n❌ Output file not found: {output_path}")
        print("Please create the file and run again.")
        sys.exit(1)

    print("   ✓ Found clip recommendations file")


def validate_clip_recommendations(json_path, video_duration):
    """Validate Claude's clip recommendations"""
    print("\n✅ Validating clip recommendations...")

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"   ✗ Invalid JSON: {e}")
        sys.exit(1)

    if "clips" not in data:
        print("   ✗ Missing 'clips' field in JSON")
        sys.exit(1)

    clips = data["clips"]

    if not clips or len(clips) == 0:
        print("   ✗ No clips found in recommendations")
        sys.exit(1)

    print(f"   Found {len(clips)} clips")

    # Validate each clip
    for i, clip in enumerate(clips, 1):
        required_fields = ["start_time", "end_time", "title", "description"]

        for field in required_fields:
            if field not in clip:
                print(f"   ✗ Clip {i} missing required field: {field}")
                sys.exit(1)

        start = clip["start_time"]
        end = clip["end_time"]

        # Validate timestamps
        if start >= end:
            print(f"   ✗ Clip {i}: start_time ({start}) >= end_time ({end})")
            sys.exit(1)

        duration = end - start

        if duration < 15 or duration > 60:
            print(f"   ⚠️  Clip {i}: duration {duration:.1f}s outside 15-60s range")

        if end > video_duration:
            print(f"   ✗ Clip {i}: end_time ({end}) exceeds video duration ({video_duration})")
            sys.exit(1)

    print("   ✓ All clips validated successfully")
    return data


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
        print(f"   ✗ Error: {e.stderr[:200]}")
        return False


def generate_clips(video_path, recommendations, output_dir):
    """Generate video clips based on recommendations"""
    print("\n✂️  Generating clips...")

    clips_dir = output_dir / "clips"
    clips_dir.mkdir(exist_ok=True)

    clips = recommendations["clips"]
    success_count = 0
    generated_files = []

    for clip in clips:
        clip_num = clip.get("clip_number", 0)
        title = clip.get("title", f"clip_{clip_num}")
        start_time = clip.get("start_time", 0)
        end_time = clip.get("end_time", 0)

        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"clip_{clip_num:03d}_{safe_title[:30]}"

        print(f"\n   📹 Creating clip {clip_num}: {title}")
        print(f"      Time: {format_time(start_time)} - {format_time(end_time)}")

        output_path = clips_dir / f"{filename}.mp4"
        instagram_path = clips_dir / f"{filename}_instagram.mp4"

        # Create standard clip
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c:v", "libx264", "-c:a", "aac",
            "-preset", "fast", "-crf", "23",
            "-y", str(output_path)
        ]

        if not run_ffmpeg(cmd, f"Creating clip {clip_num}"):
            continue

        print(f"      ✓ Created {filename}.mp4")
        generated_files.append(output_path)

        # Create Instagram vertical version (9:16 aspect ratio)
        cmd_instagram = [
            "ffmpeg", "-i", str(output_path),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
            "-c:v", "libx264", "-c:a", "aac",
            "-preset", "fast", "-crf", "23",
            "-y", str(instagram_path)
        ]

        if run_ffmpeg(cmd_instagram, f"Creating Instagram version {clip_num}"):
            print(f"      ✓ Created {filename}_instagram.mp4 (9:16)")
            generated_files.append(instagram_path)
            success_count += 1

    print(f"\n   ✅ Successfully created {success_count}/{len(clips)} clips")
    return generated_files


def generate_summary_report(output_dir, recommendations, generated_files, metadata):
    """Generate a summary report"""
    print("\n📊 Generating summary report...")

    report_path = output_dir / "SUMMARY.md"

    report = f"""# Video Clipping Summary Report

## Video Information
- **Title**: {metadata.get('title', 'Unknown')}
- **Video ID**: {metadata.get('video_id', 'Unknown')}
- **Duration**: {metadata.get('duration', 0)} seconds
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Analysis Results
- **Total Clips Recommended**: {len(recommendations.get('clips', []))}
- **Overall Theme**: {recommendations.get('overall_theme', 'N/A')}
- **Target Audience**: {recommendations.get('target_audience', 'N/A')}
- **Hashtags**: {', '.join(recommendations.get('hashtag_suggestions', []))}

## Generated Clips

"""

    for i, clip in enumerate(recommendations.get('clips', []), 1):
        report += f"""### Clip {i}: {clip.get('title', 'Untitled')}
- **Time**: {format_time(clip.get('start_time', 0))} - {format_time(clip.get('end_time', 0))}
- **Duration**: {clip.get('duration', 0):.1f}s
- **Virality Score**: {clip.get('virality_score', 0)}/10
- **Description**: {clip.get('description', 'N/A')}
- **Suggested Caption**: {clip.get('suggested_caption', 'N/A')}
- **Content Type**: {clip.get('content_type', 'N/A')}

"""

    report += f"""## Output Files

Generated {len(generated_files)} files in `clips/` directory:

"""

    for filepath in sorted(generated_files):
        size_mb = filepath.stat().st_size / (1024 * 1024)
        report += f"- `{filepath.name}` ({size_mb:.1f} MB)\n"

    report += """
## Next Steps

1. **Review each clip** for quality and content
2. **Add captions** using Remotion or editing software (Phase 2)
3. **Add trending audio/music** in Instagram/TikTok editor
4. **Post with optimized captions** and hashtags from recommendations
5. **Track performance** and iterate on successful patterns

---
Generated by AI Video Clipper
"""

    with open(report_path, 'w') as f:
        f.write(report)

    print(f"   ✓ Report saved to: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Video Clipper - Automatically create viral clips from YouTube videos"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--skip-download", action="store_true", help="Skip download if video already exists")
    parser.add_argument("--skip-transcription", action="store_true", help="Skip transcription if it already exists")

    args = parser.parse_args()

    print("=" * 60)
    print("  AI-Powered Video Clipper")
    print("  Automated Viral Clip Generation")
    print("=" * 60)

    # Check for ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ ffmpeg not found. Install with: brew install ffmpeg")
        sys.exit(1)

    try:
        # Parse URL
        video_id = parse_youtube_url(args.url)
        print(f"\n✓ Video ID: {video_id}")

        # Setup directories
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)

        output_dir = downloads_dir / video_id
        output_dir.mkdir(exist_ok=True)

        print(f"✓ Output directory: {output_dir}")

        # Download video
        video_path = output_dir / "original.mp4"
        if args.skip_download and video_path.exists():
            print(f"\n✓ Using existing video: {video_path}")
            metadata_path = output_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {"video_id": video_id}
        else:
            video_path, metadata = download_video(args.url, video_id, output_dir)

        # Transcribe video
        transcript_json = output_dir / "original.json"
        if args.skip_transcription and transcript_json.exists():
            print(f"\n✓ Using existing transcription")
            with open(transcript_json, 'r') as f:
                transcript_data = json.load(f)
        else:
            transcript_data = transcribe_video(video_path, output_dir)

        # Generate Claude prompt
        prompt_path = generate_analysis_prompt(transcript_data, metadata, output_dir)

        # Invoke Claude analysis (interactive)
        recommendations_path = output_dir / "clip_recommendations.json"
        invoke_claude_analysis(prompt_path, recommendations_path)

        # Validate recommendations
        recommendations = validate_clip_recommendations(recommendations_path, metadata.get("duration", 999999))

        # Generate clips
        generated_files = generate_clips(video_path, recommendations, output_dir)

        # Generate summary report
        report_path = generate_summary_report(output_dir, recommendations, generated_files, metadata)

        print("\n" + "=" * 60)
        print("  ✅ Video Clipping Complete!")
        print("=" * 60)
        print(f"\n📁 All files saved to: {output_dir}")
        print(f"📊 Summary report: {report_path}")
        print(f"🎬 Generated {len(generated_files)} clip files")

        print("\n🎯 Next Steps:")
        print("1. Review clips in the clips/ directory")
        print("2. Use suggested captions from SUMMARY.md")
        print("3. Add captions (Phase 2 feature coming soon)")
        print("4. Post to Instagram/TikTok with recommended hashtags")

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
