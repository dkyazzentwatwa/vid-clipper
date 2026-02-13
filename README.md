# AI Video Clipper

Automatically identify and create viral-worthy clips from YouTube videos using AI-powered analysis. This tool uses Claude AI to analyze video transcripts and intelligently extract the most engaging moments for Instagram Reels and TikTok.

## Overview

The AI Video Clipper is a two-phase automation tool that transforms long-form YouTube videos into short, engaging social media clips:

**Phase 1 (Current):** AI-powered clip identification and generation
- Downloads YouTube videos
- Transcribes audio using Whisper
- Analyzes content with Claude AI
- Generates optimized clips for Instagram/TikTok

**Phase 2 (Roadmap):** Automated caption generation
- Dynamic caption overlays using Remotion
- Customizable text styles and animations
- Auto-synced captions with speech timing

## Features

- **Smart Clip Detection**: Uses Claude AI to identify viral-worthy moments based on:
  - Strong hooks and attention-grabbing openings
  - Value bombs (quick, actionable insights)
  - Emotional peaks and exciting demonstrations
  - Complete story arcs with setup-payoff structure

- **Automated Workflow**: End-to-end automation from URL to final clips
  - YouTube video downloading with cookie support
  - Audio transcription with timestamp precision
  - AI-powered content analysis
  - FFmpeg-based video processing

- **Social Media Optimization**: Generates clips ready for posting
  - 15-60 second duration (optimal for Reels/TikTok)
  - 9:16 vertical format for mobile viewing
  - Suggested captions and hashtags
  - Virality scoring for each clip

- **Comprehensive Reporting**: Detailed analysis output
  - Clip recommendations with timestamps
  - Virality scores and success factors
  - Target audience insights
  - Ready-to-use social media captions

## Installation

### Prerequisites

- Python 3.8 or higher
- ffmpeg (for video processing)
- macOS, Linux, or Windows with WSL

### Step 1: Install System Dependencies

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Step 2: Install Python Dependencies

```bash
# Clone or download this repository
cd vid-clipper

# Install Python packages
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `yt-dlp` - YouTube video downloader
- `openai-whisper` - Audio transcription

### Step 3: Verify Installation

```bash
# Check ffmpeg
ffmpeg -version

# Check yt-dlp
yt-dlp --version

# Check whisper
whisper --help
```

## Usage

### Basic Usage

```bash
python ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Full Example

```bash
# Example with the sample video
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

### Advanced Options

```bash
# Skip download if video already exists
python ai_clip_generator.py "https://youtube.com/watch?v=ID" --skip-download

# Skip transcription if it already exists
python ai_clip_generator.py "https://youtube.com/watch?v=ID" --skip-transcription

# Combine flags
python ai_clip_generator.py "https://youtube.com/watch?v=ID" --skip-download --skip-transcription
```

## Workflow Explanation

The AI Video Clipper follows a 6-step automated workflow:

### Step 1: Video Download
```
Input: YouTube URL
Output: original.mp4, metadata.json
```

- Extracts video ID from URL
- Downloads highest quality MP4 format
- Attempts multiple methods: Chrome cookies → Firefox cookies → No cookies
- Saves video metadata (title, duration, uploader, etc.)

### Step 2: Audio Transcription
```
Input: original.mp4
Output: original.json (Whisper transcript)
```

- Uses OpenAI Whisper for speech-to-text
- Generates timestamps for each segment
- Tries "base" model first, falls back to "tiny" if needed
- Outputs JSON with precise timing information

### Step 3: Prompt Generation
```
Input: Transcript + Metadata
Output: analysis_request.md
```

- Formats transcript with [MM:SS] timestamps
- Combines with video metadata
- Uses template from `prompt_templates/clip_analysis_prompt.md`
- Creates analysis request for Claude

### Step 4: AI Analysis (Interactive)
```
Input: analysis_request.md
Output: clip_recommendations.json
```

**This step requires manual interaction with Claude:**

1. The script pauses and displays the prompt file location
2. You copy the prompt and submit to Claude (via Claude Code, web, or API)
3. Claude analyzes the transcript and returns JSON with clip recommendations
4. You save the JSON as `clip_recommendations.json`
5. Press Enter to continue

**Why manual?** This allows you to:
- Review Claude's analysis prompt
- Adjust parameters if needed
- Verify recommendations before processing
- Keep costs transparent (API usage)

### Step 5: Clip Generation
```
Input: clip_recommendations.json + original.mp4
Output: clips/*.mp4
```

- Validates all clip timestamps
- Uses FFmpeg to extract video segments
- Generates two versions per clip:
  - Standard format (preserves original aspect ratio)
  - Instagram format (9:16 vertical with padding)
- Creates descriptive filenames based on clip titles

### Step 6: Summary Report
```
Output: SUMMARY.md
```

- Overview of all generated clips
- Virality scores and recommendations
- Suggested captions and hashtags
- File listing with sizes
- Next steps for posting

## Directory Structure

After running, your project will look like this:

```
vid-clipper/
├── ai_clip_generator.py        # Main script
├── requirements.txt            # Python dependencies
├── prompt_templates/
│   └── clip_analysis_prompt.md # Claude analysis template
├── downloads/
│   └── VIDEO_ID/              # Per-video directory
│       ├── original.mp4       # Downloaded video
│       ├── original.json      # Whisper transcript
│       ├── metadata.json      # Video metadata
│       ├── analysis_request.md # Claude prompt
│       ├── clip_recommendations.json # AI analysis results
│       ├── SUMMARY.md         # Final report
│       └── clips/             # Generated clips
│           ├── clip_001_hook.mp4
│           ├── clip_001_hook_instagram.mp4
│           ├── clip_002_demo.mp4
│           ├── clip_002_demo_instagram.mp4
│           └── ...
└── logs/                       # (future use)
```

## Output Files Explained

### Video Files
- **original.mp4**: The full YouTube video
- **clip_XXX_*.mp4**: Standard clips (original aspect ratio)
- **clip_XXX_*_instagram.mp4**: Vertical clips (9:16, 1080x1920)

### Data Files
- **metadata.json**: Video title, duration, uploader, views, etc.
- **original.json**: Full Whisper transcript with timestamps
- **analysis_request.md**: The prompt sent to Claude
- **clip_recommendations.json**: Claude's analysis and clip suggestions
- **SUMMARY.md**: Human-readable report with all recommendations

## Understanding Claude's Recommendations

The `clip_recommendations.json` contains:

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
  "video_summary": "Overall video description",
  "overall_theme": "Main category (e.g., 'AI Automation')",
  "target_audience": "Primary audience",
  "hashtag_suggestions": ["#apple", "#AI", "#automation"]
}
```

**Key Fields:**
- **virality_score**: 1-10 rating (8+ highly recommended)
- **virality_factors**: What makes this clip engaging
- **content_type**: hook, demo, tutorial, value_bomb, story, payoff
- **suggested_caption**: Ready-to-use social media text

## Troubleshooting

### Video Download Fails

**Problem:** "All download methods failed"

**Solutions:**
1. **Try manual download:**
   - Visit the YouTube URL in browser
   - Use browser extension (Video DownloadHelper)
   - Save as `downloads/VIDEO_ID/original.mp4`
   - Run script again with `--skip-download`

2. **Use browser cookies:**
   ```bash
   # Make sure you're logged into YouTube in Chrome/Firefox
   yt-dlp --cookies-from-browser chrome -o downloads/VIDEO_ID/original.mp4 "URL"
   ```

3. **Check for age restrictions or region blocks**

### Transcription Fails

**Problem:** "Whisper not found" or transcription errors

**Solutions:**
1. **Reinstall Whisper:**
   ```bash
   pip uninstall openai-whisper
   pip install openai-whisper
   ```

2. **Try smaller model:**
   - Script automatically tries "base" then "tiny"
   - For very long videos, manually use "tiny" model

3. **Check disk space:**
   - Whisper downloads models (~1-3GB)
   - Ensure sufficient space in `~/.cache/whisper`

### FFmpeg Errors

**Problem:** "ffmpeg not found" or clip generation fails

**Solutions:**
1. **Verify installation:**
   ```bash
   which ffmpeg
   ffmpeg -version
   ```

2. **Reinstall ffmpeg:**
   ```bash
   # macOS
   brew reinstall ffmpeg

   # Linux
   sudo apt install --reinstall ffmpeg
   ```

3. **Check file permissions:**
   ```bash
   chmod +x ai_clip_generator.py
   ```

### Invalid JSON from Claude

**Problem:** "Invalid JSON" error when parsing recommendations

**Solutions:**
1. **Ensure pure JSON output:**
   - Claude sometimes wraps JSON in markdown code blocks
   - Remove ```json and ``` markers
   - File should start with `{` and end with `}`

2. **Validate JSON:**
   ```bash
   python -m json.tool clip_recommendations.json
   ```

3. **Check required fields:**
   - Each clip needs: start_time, end_time, title, description
   - Root object needs: clips (array)

### Clips Are Cut Off or Wrong Timestamps

**Problem:** Clips don't match the described content

**Solutions:**
1. **Verify transcript timestamps:**
   - Check `original.json` for accuracy
   - Whisper sometimes misaligns on poor audio

2. **Review Claude's recommendations:**
   - Check `analysis_request.md` to see what Claude analyzed
   - Timestamps in [MM:SS] format should match video

3. **Manual adjustment:**
   - Edit `clip_recommendations.json` directly
   - Adjust start_time and end_time as needed
   - Re-run with `--skip-download --skip-transcription`

### Memory Issues

**Problem:** Script crashes with memory errors

**Solutions:**
1. **Use smaller Whisper model:**
   - Edit script to force "tiny" model
   - Reduce video quality before transcription

2. **Process shorter videos:**
   - Start with videos under 10 minutes
   - Split longer videos first

3. **Close other applications:**
   - Whisper and FFmpeg are memory-intensive

## Best Practices

### Getting Better Clips

1. **Choose the right content:**
   - Tech demos and tutorials work great
   - Talking head videos may need more manual review
   - High-energy presentations create better clips

2. **Review before posting:**
   - Watch each generated clip
   - Verify audio sync and quality
   - Check for awkward cuts

3. **Customize captions:**
   - Use Claude's suggestions as starting points
   - Add personality and emojis
   - Match your brand voice

### Optimization Tips

1. **Batch processing:**
   - Process multiple videos sequentially
   - Use `--skip-download` to retry failed steps

2. **Disk space management:**
   - Videos can be large (100MB-1GB+)
   - Delete originals after clipping
   - Keep only the Instagram versions

3. **Iterate on prompts:**
   - Adjust `prompt_templates/clip_analysis_prompt.md`
   - Request specific clip types (e.g., "focus on funny moments")
   - Experiment with different selection criteria

## Phase 2 Roadmap: Caption Generation

**Status:** Planned for future release

**Features:**
- Automated caption overlays using Remotion
- Word-level timing from Whisper transcript
- Customizable caption styles:
  - Font, size, color, positioning
  - Highlight current word
  - Background boxes for readability
- Animation presets (fade, slide, pop)
- Export with captions burned into video

**Timeline:** TBD

**Preview workflow:**
```bash
# Phase 2 usage (future)
python ai_clip_generator.py "URL" --add-captions --caption-style "bold"
```

**Why Remotion?**
- Programmatic video editing with React
- Frame-perfect caption timing
- Professional-quality output
- Open-source and customizable

**Get involved:**
If you're interested in contributing to Phase 2, please open an issue or discussion!

## Examples

See [EXAMPLES.md](EXAMPLES.md) for a complete walkthrough using the sample video.

## FAQ

**Q: How much does this cost?**
A: The tool is free, but you may incur costs from:
- Claude API usage (if using programmatically)
- Storage for video files
- Whisper runs locally (free)

**Q: Can I use videos from other platforms?**
A: Currently YouTube-only. Future versions may support direct video files.

**Q: How accurate is the AI analysis?**
A: Very good for tech content. Accuracy depends on:
- Transcript quality (clear audio helps)
- Content structure (well-organized videos work best)
- Claude's understanding of your niche

**Q: Can I edit the clips after generation?**
A: Yes! Use any video editor. The clips are standard MP4 files.

**Q: Do I need a Claude subscription?**
A: You need access to Claude (free tier works). You manually submit the prompt and copy the response.

**Q: What if I want different clip lengths?**
A: Edit the `prompt_templates/clip_analysis_prompt.md` to change the duration constraints (currently 15-60s).

## Contributing

Contributions are welcome! Areas for improvement:
- Automatic caption generation (Phase 2)
- Support for more video platforms
- Better error handling and recovery
- GUI/web interface
- Batch processing multiple videos

## License

This project is open source. Feel free to use, modify, and distribute.

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [Whisper](https://github.com/openai/whisper) - Speech recognition
- [Claude](https://claude.ai) - AI content analysis
- [FFmpeg](https://ffmpeg.org) - Video processing

## Support

Having issues? Check:
1. [Troubleshooting](#troubleshooting) section above
2. [EXAMPLES.md](EXAMPLES.md) for step-by-step guidance
3. Open an issue with:
   - Full error message
   - Your command
   - Video URL (if not private)
   - Operating system

---

**Ready to create viral clips?** Start with the example in [EXAMPLES.md](EXAMPLES.md)!
