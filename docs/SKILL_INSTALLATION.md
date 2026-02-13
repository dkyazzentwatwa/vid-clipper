# Viral Video Clipper Skill - Installation Guide

## What Is This?

The **Viral Video Clipper** skill is a packaged, reusable Claude Code skill that transforms any long-form YouTube video into viral-worthy short clips optimized for Instagram Reels and TikTok.

## Installation

### Option 1: Import the Skill (Recommended)

1. Locate the skill file: `viral-video-clipper.skill` (13KB)
2. Import into Claude Code using the skills manager
3. The skill will be available in all future Claude Code sessions

### Option 2: Manual Installation

```bash
# Extract the skill package
unzip viral-video-clipper.skill -d ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/viral-video-clipper/
```

## What's Included

The skill package contains:

```
viral-video-clipper/
├── SKILL.md                           # Main skill instructions (7.9KB)
├── scripts/
│   └── ai_clip_generator.py          # Main orchestrator (18KB)
├── references/
│   ├── clip_analysis_prompt.md       # Claude AI prompt template (4.8KB)
│   └── troubleshooting.md            # Common issues & solutions (2.8KB)
└── assets/
    └── requirements.txt              # Python dependencies (90B)
```

**Total size:** 13KB (compressed), 34KB (uncompressed)

## Prerequisites

Before using the skill, install these dependencies:

```bash
# Install Python packages
pip install yt-dlp openai-whisper

# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Linux)
sudo apt install ffmpeg
```

## How to Use

Once installed, simply ask Claude Code:

- "Create viral clips from this YouTube video: [URL]"
- "Turn my video into Instagram reels"
- "Extract the best moments from this tutorial"
- "Make TikTok clips from my product demo"

Claude will automatically use the skill to:

1. Download the YouTube video
2. Transcribe audio with timestamps
3. Analyze the content for viral moments
4. Generate optimized clips (standard + Instagram 9:16)
5. Provide ready-to-use captions and hashtags

## Example Usage

```
User: Create viral clips from https://www.youtube.com/watch?v=yKeWqGkCaRQ

Claude: [Automatically invokes viral-video-clipper skill]

        ✅ Downloaded video: "I Made Claude Into A Cybersecurity Agent"
        ✅ Transcribed with Whisper
        ✅ Generated AI analysis prompt

        🤖 Please run Claude on the analysis prompt at:
           downloads/yKeWqGkCaRQ/analysis_request.md

        [After you provide the JSON analysis]

        ✅ Generated 5 viral-worthy clips
        ✅ Created Instagram 9:16 versions
        ✅ Summary report with captions ready!
```

## Workflow Overview

```
YouTube URL
    ↓
Download video (yt-dlp with cookie support)
    ↓
Transcribe audio (Whisper with timestamps)
    ↓
Generate Claude analysis prompt
    ↓
[YOU: Run Claude on the prompt] ← Interactive step
    ↓
Generate clips (FFmpeg)
    ↓
✨ Viral-ready clips + captions + hashtags
```

## Output Structure

For each video, you'll get:

```
downloads/{video_id}/
├── original.mp4                     # Downloaded video
├── original.json                    # Whisper transcript
├── metadata.json                    # Video info
├── analysis_request.md              # Claude prompt
├── clip_recommendations.json        # AI analysis
├── SUMMARY.md                       # Final report
└── clips/
    ├── clip_001_hook.mp4           # Standard clip
    ├── clip_001_hook_instagram.mp4 # Instagram 9:16
    ├── clip_002_demo.mp4
    ├── clip_002_demo_instagram.mp4
    └── ...
```

## What Makes This Skill Powerful

### AI-Powered Clip Selection

The skill uses Claude to analyze videos for:

- **Strong Hooks** (0-3 sec attention grabbers)
- **Value Bombs** (actionable tips, "aha!" moments)
- **Emotional Peaks** (excitement, surprise, humor)
- **Story Arcs** (complete narratives with payoff)

### Optimized for Social Media

- **Duration:** 15-60 seconds (optimal for Reels/TikTok)
- **Format:** Dual output (landscape + 9:16 vertical)
- **Quality:** Professional FFmpeg encoding
- **Captions:** Ready-to-use captions with emojis
- **Hashtags:** AI-generated hashtag suggestions

### Automation Features

- **Cookie-based downloads** - Handles private/age-restricted videos
- **Whisper transcription** - Timestamp-accurate audio-to-text
- **Fallback mechanisms** - Multiple download/transcription methods
- **Comprehensive validation** - Ensures AI output is valid
- **Batch-friendly** - Skip flags for efficient re-processing

## Advanced Features

### Skip Flags

```bash
# Skip download if video already exists
python3 scripts/ai_clip_generator.py <url> --skip-download

# Skip transcription if already done
python3 scripts/ai_clip_generator.py <url> --skip-transcription

# Both (for testing different clip selections)
python3 scripts/ai_clip_generator.py <url> --skip-download --skip-transcription
```

### Custom Clip Selection

You can manually edit the `clip_recommendations.json` file to:

- Adjust timestamps
- Change clip titles
- Modify suggested captions
- Add/remove clips

Then re-run with `--skip-download --skip-transcription` to regenerate only the clips.

## Troubleshooting

The skill includes a comprehensive troubleshooting guide at `references/troubleshooting.md` covering:

- Download failures (403 errors, cookies, updates)
- Transcription issues (memory, speed, model selection)
- FFmpeg problems (audio sync, encoding)
- JSON validation errors
- Performance optimization

**Quick fixes:**

```bash
# Update yt-dlp
brew upgrade yt-dlp

# Install Whisper
pip install openai-whisper

# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

## Real-World Example

**Input:** 3-minute cybersecurity demo video

**Output:**
- 5 viral-worthy clips (21s, 43s, 33s, 27s, 43s)
- 10 total files (standard + Instagram versions)
- Virality scores: 8/10, 9/10, 8/10, 9/10, 8/10
- Ready-to-use captions with emojis
- Hashtags: #cybersecurity #AI #infosec #pentest #opensource

**Time saved:** Manual editing (1-2 hours) → AI workflow (10-15 minutes)

## Design Philosophy

The skill balances **automation** with **human oversight**:

- ✅ **Automated:** Download, transcription, clip generation, formatting
- 🤝 **Interactive:** AI analysis step (you review the prompt and output)
- ✅ **Validated:** Comprehensive checks ensure quality output
- 🎯 **Optimized:** Built on proven patterns from viral content

This approach ensures:
- **Quality control** - You see what Claude recommends before generating
- **No API costs** - File-based analysis (no Anthropic API charges)
- **Easy debugging** - All intermediate files are saved
- **Flexibility** - Edit recommendations before final generation

## What's Next

After generating clips:

1. **Review** - Check quality and content
2. **Edit** - Add captions (automated captions coming in Phase 2)
3. **Enhance** - Add trending music in Instagram/TikTok editor
4. **Post** - Use suggested captions and hashtags
5. **Track** - Monitor performance and iterate

## Future Enhancements (Roadmap)

Phase 2 features planned:
- ✨ Automated caption generation with Remotion
- ✨ Direct Claude API integration (no manual step)
- ✨ Web UI for clip review and editing
- ✨ Batch processing multiple videos
- ✨ Social media posting integration
- ✨ Background music addition
- ✨ Thumbnail extraction and optimization

## Support

The skill includes:

- **SKILL.md** - Complete usage documentation
- **references/troubleshooting.md** - Common issues and solutions
- **references/clip_analysis_prompt.md** - AI prompt template
- **scripts/ai_clip_generator.py** - Well-documented Python code

All files are included in the skill package and available in context when using the skill.

## License

Open source - feel free to fork, modify, and share!

---

**Skill Package:** `viral-video-clipper.skill` (13KB)
**Version:** 1.0.0
**Created:** February 2026
**Compatibility:** Claude Code, macOS/Linux
