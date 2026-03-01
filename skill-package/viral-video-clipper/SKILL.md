---
name: viral-video-clipper
description: Automatically create viral-worthy short clips from YouTube videos using AI analysis. Use when the user wants to create Instagram Reels, TikTok clips, or social media shorts from long-form video content. Triggers include requests to "create clips," "extract highlights," "make reels," "find viral moments," or "turn video into shorts." Also use when the user provides a YouTube URL and wants optimized clips for social media.
---

# Viral Video Clipper

Transform long-form YouTube videos into viral-worthy short clips optimized for Instagram Reels and TikTok using AI-powered analysis.

## Quick Start

```bash
python3 scripts/ai_clip_generator.py "<youtube-url>"
```

The script will:
1. Download the YouTube video
2. Transcribe audio with timestamps using Whisper
3. Generate an AI analysis prompt
4. **[Pause for user]** Run Claude on the analysis prompt
5. Generate clips (standard + Instagram 9:16 versions)
6. Create summary report with captions and hashtags

## Prerequisites

Verify dependencies are installed:

```bash
# Check installations
yt-dlp --version        # YouTube downloader
whisper --help          # Audio transcription
ffmpeg -version         # Video processing
node --version          # Node.js 18+ (required for captions)
```

If missing, install them:

```bash
# Install Python dependencies
pip install -r assets/requirements.txt

# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Linux)
sudo apt install ffmpeg

# Install Node.js (required for captions)
brew install node       # macOS
# Or use nvm: nvm install 18

# Install Remotion dependencies (for captions)
cd remotion-captions && npm install
```

## Workflow

### Step 1: Download and Transcribe

Run the main script with a YouTube URL:

```bash
python3 scripts/ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script will:
- Extract video ID from URL
- Download video using yt-dlp (tries Chrome cookies → Firefox cookies → no cookies)
- Transcribe audio with Whisper (base model, fallback to tiny)
- Save files to `downloads/{video_id}/`

**Output files:**
- `original.mp4` - Downloaded video
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
- `clips/clip_001_*_captioned.mp4` - With animated captions (if `--add-captions`)
- `clips/clip_001_*_instagram_captioned.mp4` - Instagram with captions (if `--add-captions`)
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
python3 scripts/ai_clip_generator.py <url> --skip-download

# Skip transcription if already done
python3 scripts/ai_clip_generator.py <url> --skip-transcription

# Skip both (useful for re-generating clips with different recommendations)
python3 scripts/ai_clip_generator.py <url> --skip-download --skip-transcription
```

### Animated Captions (Phase 2)

Generate CapCut-style animated captions using Remotion:

```bash
# Add captions with default style (background)
python3 scripts/ai_clip_generator.py <url> --add-captions

# Choose specific caption style
python3 scripts/ai_clip_generator.py <url> --add-captions --caption-style scaling

# Custom accent color (default: yellow #FFFF00)
python3 scripts/ai_clip_generator.py <url> --add-captions --caption-color "#FF6600"
```

**Available Caption Styles:**

| Style | Description | Best For |
|-------|-------------|----------|
| `background` | Animated highlight box behind words (default) | CapCut-style, modern IG look |
| `scaling` | Words scale up with spring animation | Energetic, punchy content |
| `colored` | Active word highlighted in accent color | Clean, professional look |

**Prerequisites for Captions:**
- Node.js 18+ required
- First run: `cd remotion-captions && npm install`

Captioned clips will be saved with `_captioned` suffix alongside standard clips.

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

- `parse_youtube_url(url)` - Extract video ID
- `download_video(url, video_id, output_dir)` - Download with cookie fallbacks
- `transcribe_video(video_path, output_dir)` - Whisper transcription
- `generate_analysis_prompt(transcript, metadata, output_dir)` - Create Claude prompt
- `validate_clip_recommendations(json_path, duration)` - Validate AI output
- `generate_clips(video_path, recommendations, output_dir)` - FFmpeg clip generation
- `generate_captions_for_clip(...)` - Remotion caption generation
- `convert_whisper_to_captions(...)` - Whisper JSON to Remotion format
- `generate_summary_report(...)` - Create final report

## Design Decisions

1. **File-based Claude integration** - Simple, no API costs, easy debugging
2. **Interactive analysis step** - User reviews prompt and AI output before generation
3. **Cookie-based downloads** - Handles age-restricted and private videos
4. **Whisper base model** - Balance of speed and accuracy
5. **Dual clip formats** - Standard landscape + Instagram 9:16 vertical
6. **Remotion for captions** - React-based rendering for animated word-by-word captions
7. **Caption positioning** - Captions positioned within video content (not black bars) for 9:16 letterboxed videos

## Next Steps After Clip Generation

1. **Review clips** - Check quality and content
2. **Add captions** - Use `--add-captions` flag or video editing software
3. **Add music** - Use trending audio in Instagram/TikTok editor
4. **Post with optimized captions** - Use suggestions from SUMMARY.md
5. **Track performance** - Monitor which clips perform best
