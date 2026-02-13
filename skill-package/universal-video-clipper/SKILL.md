---
name: universal-video-clipper
description: Use when the user wants viral short clips from either a YouTube URL or an uploaded/local video file for Instagram Reels or TikTok.
---

# Universal Video Clipper

Transform long-form videos into viral-worthy short clips optimized for Instagram Reels and TikTok using AI-powered analysis.

## Quick Start

```bash
python3 scripts/ai_clip_generator.py "<youtube-url-or-local-video-path>"
```

The script will:
1. Accept either a YouTube URL or a local uploaded video file
2. Download/copy video into the working folder
3. Transcribe audio with timestamps using Whisper
4. Generate an AI analysis prompt
5. **[Pause for user]** Run Claude on the analysis prompt
6. Generate clips (standard + Instagram 9:16 versions)
7. Create summary report with captions and hashtags

## Prerequisites

Verify dependencies are installed:

```bash
# Check installations
yt-dlp --version        # YouTube downloader (only needed for YouTube URLs)
whisper --help          # Audio transcription
ffmpeg -version         # Video processing
```

If missing, install them:

```bash
# Install Python dependencies
pip install -r assets/requirements.txt

# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Linux)
sudo apt install ffmpeg
```

## Workflow

### Step 1: Download and Transcribe

Run the main script with either input type:

```bash
# YouTube input
python3 scripts/ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Local/uploaded file input
python3 scripts/ai_clip_generator.py "/absolute/path/to/uploaded_video.mp4"
```

The script will:
- Detect source type automatically
- For YouTube: extract video ID and download via yt-dlp
- For local input: copy your file into the run folder
- Transcribe audio with Whisper (base model, fallback to tiny)
- Save files to `downloads/{video_id}/`

**Output files:**
- `original.*` - Downloaded or copied source video
- `original.json` - Whisper transcript with timestamps
- `metadata.json` - Video title, duration, uploader
- `analysis_request.md` - Generated Claude prompt

### Step 2: AI Analysis (Interactive)

The script pauses and displays:

```
🤖 Claude AI Analysis Required
============================================================
Next steps:
1. Review the analysis prompt at:
   downloads/{video_id}/analysis_request.md

2. Run Claude Code on this prompt to generate clip recommendations

3. Save Claude's JSON output to:
   downloads/{video_id}/clip_recommendations.json

4. Press Enter when the JSON file is ready...
============================================================
```

**What to do:**
1. Read the generated `analysis_request.md` file
2. The file contains the full transcript with timestamps and detailed instructions
3. Run Claude (in a separate session) on this prompt
4. Claude will analyze the video and return JSON with 3-7 clip recommendations
5. Save Claude's JSON response to `clip_recommendations.json`
6. Return to the script and press Enter

**Important:** The JSON must contain valid clip recommendations. See `references/clip_analysis_prompt.md` for the required format.

### Step 3: Generate Clips

After you provide the JSON file, the script automatically:
- Validates clip recommendations (timestamps, required fields)
- Generates each clip using FFmpeg
- Creates Instagram 9:16 vertical versions
- Generates a summary report

**Output:**
- `clips/clip_001_*.mp4` - Standard clips (landscape)
- `clips/clip_001_*_instagram.mp4` - Instagram versions (9:16 vertical)
- `SUMMARY.md` - Report with captions, hashtags, virality scores

## Clip Selection Criteria

The AI analysis identifies viral-worthy moments based on:

1. **Strong Hooks** (0-3 seconds) - Bold claims, surprising statements, visual demonstrations
2. **Value Bombs** - Actionable tips, "aha!" moments, problem-solution demos
3. **Emotional Peaks** - Excitement, surprise, humor, impressive demonstrations
4. **Story Arcs** - Complete narratives with setup → demonstration → payoff

**Constraints:**
- Duration: 15-60 seconds (optimal: 20-45 seconds)
- Self-contained: Each clip makes sense independently
- Natural boundaries: No mid-sentence cuts
- Platform: Optimized for Instagram Reels and TikTok (9:16 mobile vertical)

## JSON Output Format

The AI analysis must return JSON in this format:

```json
{
  "clips": [
    {
      "clip_number": 1,
      "start_time": 5.2,
      "end_time": 32.8,
      "duration": 27.6,
      "title": "Hook: AI Creates Apple Shortcuts",
      "description": "Opens with bold claim and immediate demonstration",
      "virality_score": 9,
      "virality_factors": ["strong_hook", "visual_demo", "trending_topic"],
      "suggested_caption": "🤯 I made AI create Apple Shortcuts!",
      "content_type": "hook",
      "target_audience": "iOS users, automation enthusiasts",
      "key_moments": ["0:05 - Bold claim", "0:15 - First demo"]
    }
  ],
  "video_summary": "Brief summary of video content",
  "overall_theme": "AI Automation",
  "target_audience": "Tech enthusiasts, developers",
  "hashtag_suggestions": ["#AI", "#automation", "#tech"]
}
```

See `references/clip_analysis_prompt.md` for the complete prompt template.

## Advanced Usage

### Skip Flags

```bash
# Skip download if video already exists
python3 scripts/ai_clip_generator.py <source> --skip-download

# Skip transcription if already done
python3 scripts/ai_clip_generator.py <source> --skip-transcription

# Skip both (useful for re-generating clips with different recommendations)
python3 scripts/ai_clip_generator.py <source> --skip-download --skip-transcription
```

### Working Directory Structure

```
downloads/
└── {video_id}/
    ├── original.mp4               # Downloaded video
    ├── original.json              # Whisper transcript
    ├── metadata.json              # Video info
    ├── analysis_request.md        # Claude prompt
    ├── clip_recommendations.json  # AI analysis output
    ├── SUMMARY.md                 # Final report
    └── clips/
        ├── clip_001_hook.mp4
        ├── clip_001_hook_instagram.mp4
        └── ...
```

## Troubleshooting

See `references/troubleshooting.md` for detailed solutions.

**Quick fixes:**

**Download fails:**
```bash
brew upgrade yt-dlp
```

**Transcription fails:**
```bash
pip install openai-whisper
```

**FFmpeg not found:**
```bash
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

**Invalid JSON from Claude:**
- Remove markdown code blocks (```json)
- Ensure all required fields are present
- Validate timestamps are within video duration

## Key Functions

In `scripts/ai_clip_generator.py`:

- `is_youtube_url(input)` - Detect source type
- `parse_youtube_url(url)` - Extract video ID
- `prepare_local_video(path, video_id, output_dir)` - Ingest local file input
- `download_video(url, video_id, output_dir)` - Download with cookie fallbacks
- `transcribe_video(video_path, output_dir)` - Whisper transcription
- `generate_analysis_prompt(transcript, metadata, output_dir)` - Create Claude prompt
- `validate_clip_recommendations(json_path, duration)` - Validate AI output
- `generate_clips(video_path, recommendations, output_dir)` - FFmpeg clip generation
- `generate_summary_report(...)` - Create final report

## Design Decisions

1. **File-based Claude integration** - Simple, no API costs, easy debugging
2. **Interactive analysis step** - User reviews prompt and AI output before generation
3. **Dual input support** - Handles both YouTube and local uploads
4. **Whisper base model** - Balance of speed and accuracy
5. **Dual clip formats** - Standard landscape + Instagram 9:16 vertical

## Next Steps After Clip Generation

1. **Review clips** - Check quality and content
2. **Add captions** - Use video editing software
3. **Add music** - Use trending audio in Instagram/TikTok editor
4. **Post with optimized captions** - Use suggestions from SUMMARY.md
5. **Track performance** - Monitor which clips perform best
