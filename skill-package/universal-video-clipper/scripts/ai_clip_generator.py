#!/usr/bin/env python3
"""
AI-Powered Video Clipper
Automatically identifies and creates viral-worthy clips from YouTube videos or local files using Claude AI.

Usage:
    python ai_clip_generator.py <youtube_url_or_local_file>

Example:
    python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
    python ai_clip_generator.py "/path/to/video.mp4"
    python ai_clip_generator.py <url> --add-captions --caption-style background
"""

import subprocess
import os
import sys
import json
import re
import shutil
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


def is_youtube_url(value):
    """Check if input looks like a YouTube URL"""
    return bool(re.search(r"(youtube\.com|youtu\.be)", str(value)))


def slugify(value):
    """Create filesystem-safe slug"""
    safe = re.sub(r"[^\w\s-]", "", value).strip().lower()
    safe = re.sub(r"[-\s]+", "_", safe)
    return safe or "video"


def get_local_video_metadata(video_path, source_id):
    """Extract metadata from local video using ffprobe"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-of", "json",
        str(video_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
    except Exception:
        info = {}

    duration = 0
    fmt = info.get("format", {})
    if fmt.get("duration"):
        try:
            duration = int(float(fmt["duration"]))
        except Exception:
            duration = 0

    return {
        "video_id": source_id,
        "title": video_path.stem,
        "duration": duration,
        "uploader": "Local Upload",
        "upload_date": datetime.now().strftime("%Y%m%d"),
        "view_count": 0,
        "description": f"Local video file: {video_path.name}",
        "source_type": "local",
        "source_path": str(video_path.resolve())
    }


def has_audio_stream(video_path):
    """Return True if ffprobe detects at least one audio stream."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "json",
        str(video_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout or "{}")
        return len(data.get("streams", [])) > 0
    except Exception:
        return False


def prepare_local_video(source_path, source_id, output_dir):
    """Copy local video into output directory and generate metadata"""
    print("\n📥 Preparing local video...")
    local_path = Path(source_path).expanduser().resolve()
    if not local_path.exists() or not local_path.is_file():
        print(f"\n❌ Local video not found: {local_path}")
        sys.exit(1)

    suffix = local_path.suffix if local_path.suffix else ".mp4"
    target_path = output_dir / f"original{suffix}"
    shutil.copy2(local_path, target_path)

    metadata = get_local_video_metadata(target_path, source_id)
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"   ✓ Copied: {local_path.name}")
    print(f"   ✓ Duration: {metadata.get('duration', 0)}s")
    return target_path, metadata


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

    video_path = Path(video_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

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

    # Handle silent videos gracefully (e.g., screen recordings with no audio track)
    if not has_audio_stream(video_path):
        print("   ⚠️  No audio stream detected; creating placeholder transcript")
        fallback = {
            "text": "[No audio track detected]",
            "segments": [
                {
                    "start": 0.0,
                    "end": 0.0,
                    "text": "[No audio track detected in this video. Use visual moments for clip selection.]",
                }
            ],
        }
        with open(transcript_json, "w") as f:
            json.dump(fallback, f, indent=2)
        return fallback

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

            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            print(f"   ✓ Transcription complete with {model} model")

            # Whisper can emit either <stem>.json or "original.json" depending on input path handling.
            stem_transcript_json = output_dir / f"{video_path.stem}.json"
            if not transcript_json.exists() and stem_transcript_json.exists():
                transcript_json = stem_transcript_json

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

    template_candidates = [
        Path(__file__).parent.parent / "references" / "clip_analysis_prompt.md",
        Path(__file__).parent / "prompt_templates" / "clip_analysis_prompt.md",
        Path(__file__).parents[2] / "prompt_templates" / "clip_analysis_prompt.md",
    ]
    template_path = next((p for p in template_candidates if p.exists()), None)

    if not template_path:
        print("   ✗ Template not found in expected locations")
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


def check_remotion_available():
    """Check if Remotion is installed and available"""
    remotion_dir = Path(__file__).parent.parent.parent.parent / "remotion-captions"
    if not remotion_dir.exists():
        # Try alternate location
        remotion_dir = Path(__file__).parent.parent / "remotion-captions"
    if not remotion_dir.exists():
        return False, "Remotion project not found", None

    node_modules = remotion_dir / "node_modules"
    if not node_modules.exists():
        return False, "Remotion dependencies not installed. Run: cd remotion-captions && npm install", None

    return True, None, remotion_dir


def convert_whisper_to_captions(whisper_json_path, start_time, end_time):
    """Convert Whisper JSON to Remotion caption format"""
    with open(whisper_json_path, 'r') as f:
        whisper_data = json.load(f)

    captions = []
    offset_ms = start_time * 1000

    for segment in whisper_data.get("segments", []):
        # Skip segments outside clip range
        if segment.get("end", 0) < start_time or segment.get("start", 0) > end_time:
            continue

        # Use word-level timestamps if available
        words = segment.get("words", [])
        if words:
            for word in words:
                word_start = word.get("start", 0)
                word_end = word.get("end", 0)

                # Skip words outside clip range
                if word_end < start_time or word_start > end_time:
                    continue

                start_ms = max(0, word_start * 1000 - offset_ms)
                end_ms = word_end * 1000 - offset_ms

                captions.append({
                    "text": word.get("word", "").strip(),
                    "startMs": start_ms,
                    "endMs": end_ms,
                    "timestampMs": start_ms,
                    "confidence": word.get("probability")
                })
        else:
            # Fall back to segment-level - distribute timing across words
            text = segment.get("text", "").strip()
            words_list = text.split()
            seg_start = segment.get("start", 0)
            seg_end = segment.get("end", 0)
            seg_duration = (seg_end - seg_start) * 1000

            if words_list:
                word_duration = seg_duration / len(words_list)
                for i, word_text in enumerate(words_list):
                    word_start_ms = seg_start * 1000 + i * word_duration - offset_ms
                    word_end_ms = word_start_ms + word_duration

                    if word_start_ms < 0:
                        continue

                    captions.append({
                        "text": word_text,
                        "startMs": max(0, word_start_ms),
                        "endMs": word_end_ms,
                        "timestampMs": max(0, word_start_ms),
                        "confidence": None
                    })

    return captions


def generate_captions_for_clip(clip_path, whisper_json_path, start_time, end_time, output_path, style="background", accent_color="#FFFF00"):
    """Generate captioned video using Remotion"""
    print(f"      🎬 Generating captions with style: {style}...")

    # Check if Remotion is available
    available, error, remotion_dir = check_remotion_available()
    if not available:
        print(f"      ⚠️  {error}")
        return False

    # Convert Whisper JSON to captions
    captions = convert_whisper_to_captions(whisper_json_path, start_time, end_time)
    if not captions:
        print(f"      ⚠️  No captions found for this time range")
        return False

    # Calculate duration in frames
    fps = 30
    duration_frames = int((end_time - start_time) * fps)

    # Copy clip to Remotion public folder for serving
    public_dir = remotion_dir / "public"
    public_dir.mkdir(exist_ok=True)
    temp_video_name = f"temp_clip_{Path(clip_path).stem}.mp4"
    temp_video_path = public_dir / temp_video_name
    shutil.copy2(clip_path, temp_video_path)

    # Create props JSON for Remotion - use staticFile path
    props = {
        "videoSrc": temp_video_name,  # Remotion will serve from public/
        "captions": captions,
        "style": style,
        "accentColor": accent_color,
        "fontFamily": "Inter, system-ui, sans-serif",
        "durationInFrames": duration_frames
    }

    # Write props to temp file
    props_file = Path(output_path).parent / f".caption_props_{Path(output_path).stem}.json"
    with open(props_file, 'w') as f:
        json.dump(props, f)

    # Build the render command using Remotion CLI
    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        "CaptionedClip",
        str(Path(output_path).resolve()),
        "--props", str(props_file.resolve()),
        "--overwrite"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(remotion_dir),
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        # Clean up temp files
        if props_file.exists():
            props_file.unlink()
        if temp_video_path.exists():
            temp_video_path.unlink()

        if result.returncode != 0:
            print(f"      ✗ Caption render failed: {result.stderr[:300]}")
            return False

        print(f"      ✓ Captions generated!")
        return True

    except subprocess.TimeoutExpired:
        print(f"      ✗ Caption render timed out")
        if props_file.exists():
            props_file.unlink()
        if temp_video_path.exists():
            temp_video_path.unlink()
        return False
    except FileNotFoundError:
        print(f"      ✗ Node.js/npx not found. Install Node.js 18+")
        if props_file.exists():
            props_file.unlink()
        if temp_video_path.exists():
            temp_video_path.unlink()
        return False


def generate_clips(video_path, recommendations, output_dir, add_captions=False, caption_style="background", caption_color="#FFFF00", whisper_json_path=None):
    """Generate video clips based on recommendations"""
    print("\n✂️  Generating clips...")

    clips_dir = output_dir / "clips"
    clips_dir.mkdir(exist_ok=True)

    clips = recommendations["clips"]
    success_count = 0
    generated_files = []

    # Check Remotion availability if captions requested
    if add_captions:
        available, error, _ = check_remotion_available()
        if not available:
            print(f"\n   ⚠️  Captions disabled: {error}")
            add_captions = False

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

        # Generate captioned versions if requested
        if add_captions and whisper_json_path:
            captioned_path = clips_dir / f"{filename}_captioned.mp4"
            captioned_instagram_path = clips_dir / f"{filename}_instagram_captioned.mp4"

            # Generate captioned standard version
            if generate_captions_for_clip(
                output_path, whisper_json_path,
                start_time, end_time,
                captioned_path, caption_style, caption_color
            ):
                generated_files.append(captioned_path)

                # Generate captioned Instagram version
                cmd_captioned_ig = [
                    "ffmpeg", "-i", str(captioned_path),
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
                    "-c:v", "libx264", "-c:a", "aac",
                    "-preset", "fast", "-crf", "23",
                    "-y", str(captioned_instagram_path)
                ]

                if run_ffmpeg(cmd_captioned_ig, f"Creating captioned Instagram version {clip_num}"):
                    print(f"      ✓ Created {filename}_instagram_captioned.mp4")
                    generated_files.append(captioned_instagram_path)

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
2. **Add captions** using --add-captions flag or editing software
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
        description="AI-Powered Video Clipper - Create viral clips from YouTube URLs or local video files"
    )
    parser.add_argument("source", help="YouTube URL or local video file path")
    parser.add_argument("--skip-download", action="store_true", help="Skip download if video already exists")
    parser.add_argument("--skip-transcription", action="store_true", help="Skip transcription if it already exists")
    parser.add_argument("--add-captions", action="store_true", help="Generate animated captions using Remotion")
    parser.add_argument("--caption-style", choices=["background", "scaling", "colored"], default="background",
                        help="Caption animation style (default: background)")
    parser.add_argument("--caption-color", default="#FFFF00", help="Accent color for captions (default: #FFFF00)")

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
        source = args.source
        source_type = "youtube" if is_youtube_url(source) else "local"
        if source_type == "youtube":
            video_id = parse_youtube_url(source)
        else:
            local_path = Path(source).expanduser().resolve()
            if not local_path.exists():
                print(f"\n❌ Local file not found: {local_path}")
                sys.exit(1)
            video_id = f"local_{slugify(local_path.stem)}_{int(local_path.stat().st_mtime)}"

        print(f"\n✓ Source type: {source_type}")
        print(f"✓ Video ID: {video_id}")

        # Setup directories
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)

        output_dir = downloads_dir / video_id
        output_dir.mkdir(exist_ok=True)

        print(f"✓ Output directory: {output_dir}")

        # Download video
        existing_video = next((p for p in output_dir.glob("original.*") if p.is_file()), None)

        if source_type == "youtube":
            video_path = output_dir / "original.mp4"
            if args.skip_download and existing_video:
                video_path = existing_video
                print(f"\n✓ Using existing video: {video_path}")
                metadata_path = output_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                else:
                    metadata = {"video_id": video_id, "source_type": "youtube"}
            else:
                video_path, metadata = download_video(source, video_id, output_dir)
                metadata["source_type"] = "youtube"
        else:
            if args.skip_download and existing_video:
                video_path = existing_video
                print(f"\n✓ Using existing local video: {video_path}")
                metadata_path = output_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                else:
                    metadata = {"video_id": video_id, "source_type": "local"}
            else:
                video_path, metadata = prepare_local_video(source, video_id, output_dir)

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
        generated_files = generate_clips(
            video_path, recommendations, output_dir,
            add_captions=args.add_captions,
            caption_style=args.caption_style,
            caption_color=args.caption_color,
            whisper_json_path=transcript_json
        )

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
        if not args.add_captions:
            print("3. Generate captions with: --add-captions --caption-style [background|scaling|colored]")
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
