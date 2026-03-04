# AI Video Clipper

Transform long-form **YouTube videos** or **local video files** into viral-ready short clips for Instagram Reels and TikTok using AI-powered analysis.

---

## Quick Start (Choose One)

### Option 1: Use with an AI Assistant (Easiest)
Give the skill file to your AI assistant (Claude Code, Codex, etc.):

```
"Install this skill: universal-video-clipper.skill"
```

Then simply ask:
> "Create viral clips from this YouTube video: https://www.youtube.com/watch?v=VIDEO_ID"

### Option 2: Use with Claude Code / Codex
Tell your AI assistant to install this project:

```
"Install this project into your skill catalog"
```

The AI will automatically use the skill when you ask for video clips.

### Option 3: Run Directly (No AI)
```bash
python ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
python ai_clip_generator.py "/path/to/video.mp4"
```

---

## How to Use This Tool

Once installed (or running directly), use natural language:

### For YouTube Videos
> "Create viral clips from this YouTube video: https://www.youtube.com/watch?v=VIDEO_ID"

> "Turn this YouTube video into Instagram Reels: [URL]"

> "Create viral clips from this YouTube video with animated captions: [URL]"

> "Extract the best highlights from this tutorial for TikTok"

### For Local/Uploaded Videos
> "Create short clips from this video file: /path/to/video.mp4"

> "Make Reels from my uploaded video"

> "Make Reels from my uploaded video with scaling caption style"

### With Additional Options
> "Create 5 viral clips from this video with animated captions"

> "Extract highlights from this YouTube video, skip downloading since I already have it"

---

## What This Tool Does

1. **Analyzes your video** - Downloads (YouTube) or ingests (local files) the source video
2. **Transcribes audio** - Uses Whisper to create timestamped text transcripts
3. **Finds viral moments** - AI analyzes the content for engaging clips (hooks, value bombs, demos)
4. **Generates clips** - Creates 15-60 second clips optimized for social media
5. **Formats for platforms** - Outputs both standard and 9:16 vertical versions

---

## What You Get

For each video processed, you'll receive:

- **Standard clips** - Original aspect ratio versions
- **Instagram versions** - 9:16 vertical format (1080x1920) with padding
- **Captioned variants** - Optional animated word-by-word captions (CapCut-style)
- **Summary report** - Suggested captions, hashtags, virality scores

### Sample Output
```
downloads/{video_id}/
├── original.mp4                    # Source video
├── original.json                   # Transcript with timestamps
├── metadata.json                   # Video info
├── analysis_request.md             # AI analysis prompt
├── clip_recommendations.json       # AI-generated clip suggestions
├── SUMMARY.md                      # Final report with captions & hashtags
└── clips/
    ├── clip_001_hook.mp4           # Standard clip
    ├── clip_001_hook_instagram.mp4 # 9:16 vertical
    ├── clip_001_hook_captioned.mp4 # With animated captions
    └── ...
```

---

## Quick Example

### YouTube Input
**Input:** `https://www.youtube.com/watch?v=VIDEO_ID`

**Output:** 3-5 ready-to-post clips with:
- Virality scores (1-10)
- Suggested captions with emojis
- Hashtag recommendations
- Standard + Instagram versions

### Local File Input
**Input:** `/Users/you/Videos/my_recording.mp4`

**Output:** Same as above - works with any MP4, MOV, or video file on your computer

---

## Prerequisites

Before first use, ensure these are installed:

| Tool | Purpose | Install Command |
|------|---------|-----------------|
| Python 3.8+ | Runtime | (usually pre-installed) |
| ffmpeg | Video processing | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| yt-dlp | YouTube downloads | `pip install yt-dlp` |
| whisper | Audio transcription | `pip install openai-whisper` |
| remotion (optional, captions) | Animated caption rendering | `cd remotion-captions && npm install` |

Verify installation:
```bash
ffmpeg -version
yt-dlp --version
whisper --help
cd remotion-captions && npx remotion --help
```

---

## Technical Reference

### CLI Command (Alternative to Natural Language)

If you prefer direct script execution:

```bash
# YouTube video
python ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Local video file (MP4, MOV, etc.)
python ai_clip_generator.py "/path/to/video.mp4"
python ai_clip_generator.py "~/Movies/my_recording.mov"

# With options
python ai_clip_generator.py "URL" --add-captions
python ai_clip_generator.py "/path/to/video.mp4" --add-captions
python ai_clip_generator.py "URL" --skip-download
```

### Caption Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `background` | CapCut-style animated box behind active word | Most content (default) |
| `scaling` | Word pops/bounces when spoken | Energetic, punchy videos |
| `colored` | Active word highlighted in accent color | Professional, clean look |

### Skip Flags

```bash
# Re-run with existing files
python ai_clip_generator.py "URL" --skip-download
python ai_clip_generator.py "URL" --skip-download --skip-transcription
```

---

## Workflow Details

### Step 1: Video Ingest
- **YouTube URLs:** Downloads via yt-dlp (tries Chrome cookies → Firefox → no cookies)
- **Local files:** Copies to working directory (supports MP4, MOV, MKV, and most video formats)

### Step 2: Transcription
- Uses OpenAI Whisper for speech-to-text
- Generates timestamps for each segment
- Falls back from "base" to "tiny" model if needed

### Step 3: AI Analysis
The script pauses and waits for AI analysis:
1. Review `analysis_request.md` (contains transcript + instructions)
2. Run AI on this prompt to generate clip recommendations
3. Save results as `clip_recommendations.json`
4. Press Enter to continue

### Step 4: Clip Generation
- Validates clip timestamps
- Uses FFmpeg to extract segments
- Creates dual formats: standard + Instagram 9:16

### Step 5: Summary Report
- Generates `SUMMARY.md` with captions, hashtags, virality scores

---

## JSON Recommendation Format

When AI analyzes the transcript, it should return JSON like:

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
      "content_type": "hook"
    }
  ],
  "video_summary": "Brief summary of video content",
  "overall_theme": "AI Automation",
  "hashtag_suggestions": ["#AI", "#automation", "#tech"]
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Download fails | `brew upgrade yt-dlp` or use browser cookies |
| Whisper not found | `pip install openai-whisper` |
| FFmpeg missing | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| Invalid JSON from AI | Remove markdown code blocks (`json`), validate required fields |

---

## Understanding the Output

### Virality Score (1-10)
- **8-10:** Highly recommended, strong viral potential
- **6-7:** Good, worth posting
- **Below 6:** Consider adjusting timestamps or skipping

### Content Types
- **hook** - Attention-grabbing opening (0-3 seconds)
- **value_bomb** - Actionable tips, "aha!" moments
- **demo** - Technical demonstrations
- **story** - Complete narrative with payoff

---

## Project Overview

This tool is designed for two types of users:

1. **AI Agents** - Use natural language prompts shown in the "How to Use This Tool" section above
2. **Direct users** - Run CLI commands shown in "Technical Reference" section

### Features
- Smart clip detection based on viral content patterns
- Automated workflow from URL to final clips
- Social media optimization (15-60 second duration, 9:16 format)
- Comprehensive reporting with captions and hashtags

### Phase 2 Features (Implemented)
- Animated caption generation using Remotion
- Word-by-word sync with Whisper timestamps
- Three customizable caption styles

---

## AI Assistant Integration (Optional)

If you use an AI assistant (like Claude Code), you can import the packaged skill:

**`universal-video-clipper.skill`** - A packaged skill file (ZIP archive) containing:
- SKILL.md with instructions for the AI
- Reference documentation
- Helper scripts

To use it, import `universal-video-clipper.skill` into your AI assistant's skill manager.

---

## License

Open source - feel free to use, modify, and distribute.

---

**Ready?** Try: "Create viral clips from this YouTube video: https://www.youtube.com/watch?v=QE_Nt5dMLHI"
