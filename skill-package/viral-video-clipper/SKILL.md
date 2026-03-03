---
name: viral-video-clipper
description: Automatically create viral-worthy short clips from YouTube videos using AI analysis. Use when the user wants to create Instagram Reels, TikTok clips, or social media shorts from long-form video content. Triggers include requests to "create clips," "extract highlights," "make reels," "find viral moments," or "turn video into shorts." Also use when the user provides a YouTube URL and wants optimized clips for social media.
---

# Viral Video Clipper

Transform long-form YouTube videos into viral-worthy short clips optimized for Instagram Reels and TikTok using AI-powered analysis.

---

## How to Talk to This Tool

Use natural language to create clips:

> "Create viral clips from this YouTube video: https://www.youtube.com/watch?v=VIDEO_ID"

> "Turn this YouTube video into Instagram Reels"

> "Extract the best highlights from this tutorial for TikTok"

> "Make short clips from this video with animated captions"

---

## What You Get

For each YouTube video processed:

- **3-7 viral-worthy clips** (15-60 seconds each)
- **Dual formats** - Standard (original aspect ratio) + Instagram 9:16 vertical
- **Optional animated captions** - CapCut-style word-by-word highlighting
- **Summary report** with:
  - Virality scores (1-10)
  - Suggested captions with emojis
  - Hashtag recommendations
  - Target audience insights

### Sample Output Structure
```
downloads/{video_id}/
├── original.mp4                    # Downloaded YouTube video
├── original.json                   # Whisper transcript with timestamps
├── metadata.json                   # Video title, duration, uploader
├── analysis_request.md             # AI analysis prompt
├── clip_recommendations.json       # AI-generated clip suggestions
├── SUMMARY.md                      # Final report
└── clips/
    ├── clip_001_hook.mp4           # Standard clip
    ├── clip_001_hook_instagram.mp4 # 9:16 vertical
    ├── clip_001_hook_captioned.mp4 # With animated captions
    └── ...
```

---

## How It Works

### Step 1: Ingest & Transcribe
- Downloads YouTube video via yt-dlp
- Transcribes audio using Whisper with timestamp precision
- Saves to `downloads/{video_id}/`

### Step 2: AI Analysis (Interactive)
The script pauses for AI analysis:
1. Review `analysis_request.md` (contains transcript + instructions)
2. Run AI on this prompt to generate clip recommendations
3. Save results as `clip_recommendations.json`
4. Press Enter to continue

### Step 3: Generate Clips
- Validates clip timestamps
- Creates standard and Instagram 9:16 versions
- Optionally adds animated captions

---

## Prerequisites

Verify these are installed:

```bash
# Check installations
ffmpeg -version                      # Video processing
yt-dlp --version                    # YouTube downloader
whisper --help                      # Audio transcription
```

If missing, install:

```bash
# Install Python dependencies
pip install -r assets/requirements.txt

# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Linux)
sudo apt install ffmpeg

# Install Node.js 18+ (for animated captions)
brew install node
```

---

## Technical Reference

### CLI Command

```bash
# Basic usage
python3 scripts/ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Skip download if video exists
python3 scripts/ai_clip_generator.py <url> --skip-download

# Skip transcription if done
python3 scripts/ai_clip_generator.py <url> --skip-transcription

# With animated captions
python3 scripts/ai_clip_generator.py <url> --add-captions
python3 scripts/ai_clip_generator.py <url> --add-captions --caption-style scaling
python3 scripts/ai_clip_generator.py <url> --add-captions --caption-color "#FF6600"
```

### Caption Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `background` | Animated highlight box behind words (default) | CapCut-style, modern IG look |
| `scaling` | Words scale up with spring animation | Energetic, punchy content |
| `colored` | Active word highlighted in accent color | Clean, professional look |

---

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

---

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

---

## Troubleshooting

### Quick Fixes

| Issue | Solution |
|-------|----------|
| Download fails | `brew upgrade yt-dlp` |
| Transcription fails | `pip install openai-whisper` |
| FFmpeg not found | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| Invalid JSON from AI | Remove markdown code blocks (`json`), ensure all required fields present |

---

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

---

## Design Decisions

1. **File-based AI integration** - Simple, no API costs, easy debugging
2. **Interactive analysis step** - User reviews prompt and AI output before generation
3. **Cookie-based downloads** - Handles age-restricted and private videos
4. **Whisper base model** - Balance of speed and accuracy
5. **Dual clip formats** - Standard landscape + Instagram 9:16 vertical
6. **Remotion for captions** - React-based rendering for animated word-by-word captions
7. **Caption positioning** - Captions positioned within video content (not black bars) for 9:16 letterboxed videos

---

## Next Steps After Clip Generation

1. **Review clips** - Check quality and content
2. **Add captions** - Use `--add-captions` flag or video editing software
3. **Add music** - Use trending audio in Instagram/TikTok editor
4. **Post with optimized captions** - Use suggestions from SUMMARY.md
5. **Track performance** - Monitor which clips perform best
