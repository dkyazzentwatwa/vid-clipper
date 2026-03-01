# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Video Clipper** is a Python-based tool that automatically identifies and creates viral-worthy clips from YouTube videos using AI-powered analysis. It's a two-phase project:
- **Phase 1 (Complete):** AI-powered clip identification and generation
- **Phase 2 (Complete):** Animated caption generation with Remotion

## Core Architecture

### Workflow Pipeline

The system follows a 6-step automated workflow orchestrated by `ai_clip_generator.py`:

1. **Video Download** → Downloads YouTube video using yt-dlp with cookie fallbacks
2. **Audio Transcription** → Uses OpenAI Whisper to generate timestamped transcripts
3. **Prompt Generation** → Formats transcript using template from `prompt_templates/clip_analysis_prompt.md`
4. **AI Analysis** → Interactive: User submits prompt to Claude and saves JSON response
5. **Clip Generation** → Uses FFmpeg to extract clips and create 9:16 Instagram versions
6. **Summary Report** → Generates SUMMARY.md with clip details and posting recommendations

### Key Design Decisions

- **Interactive Claude integration:** Phase 1 uses file-based interaction (not API) to keep costs transparent and allow prompt review
- **Cookie-based YouTube downloads:** Tries Chrome cookies → Firefox cookies → No cookies to handle age-restricted content
- **Whisper model fallback:** Tries "base" model first, falls back to "tiny" if it fails
- **Dual output formats:** Standard clips preserve aspect ratio, Instagram clips use 9:16 vertical with black padding
- **Validation-first:** All Claude JSON outputs are validated against schema before clip generation

## Development Commands

### Running the Main Script

```bash
# Full workflow
python3 ai_clip_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Skip download (if video exists)
python3 ai_clip_generator.py "URL" --skip-download

# Skip transcription (if transcript exists)
python3 ai_clip_generator.py "URL" --skip-transcription

# Skip both (for testing clip generation only)
python3 ai_clip_generator.py "URL" --skip-download --skip-transcription

# With animated captions (Phase 2)
python3 ai_clip_generator.py "URL" --add-captions

# Choose caption style: background (default), scaling, colored
python3 ai_clip_generator.py "URL" --add-captions --caption-style scaling

# Custom accent color for captions
python3 ai_clip_generator.py "URL" --add-captions --caption-color "#FF5500"
```

### Dependency Verification

```bash
# Check ffmpeg
ffmpeg -version

# Check yt-dlp
yt-dlp --version

# Check whisper
whisper --help

# Install dependencies
pip install -r requirements.txt
brew install ffmpeg  # macOS
```

### Testing

```bash
# Validate Python syntax
python3 -m py_compile ai_clip_generator.py

# Test with example video
python3 ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

## Project Structure

```
vid-clipper/
├── ai_clip_generator.py          # Main orchestrator script (~700 lines)
├── requirements.txt               # Python dependencies
├── CLAUDE.md                      # This file - project documentation
├── README.md                      # User-facing documentation
├── quick_start.sh                 # Quick setup script
├── .gitignore                     # Git ignore rules
│
├── prompt_templates/              # AI analysis templates
│   └── clip_analysis_prompt.md   # Claude clip analysis template
│
├── remotion-captions/             # Phase 2: Animated caption system
│   ├── package.json              # Node.js dependencies
│   ├── tsconfig.json             # TypeScript config
│   ├── remotion.config.ts        # Remotion config
│   └── src/
│       ├── index.ts              # Remotion entry point
│       ├── Root.tsx              # Composition registration
│       ├── CaptionedClip.tsx     # Main video+caption composition
│       ├── convert-whisper.ts    # Whisper JSON → Remotion captions
│       ├── render-clip.ts        # CLI render script
│       └── CaptionStyles/        # Caption animation styles
│           ├── types.ts          # Shared types & utilities
│           ├── ColoredWords.tsx  # Highlight active word
│           ├── ScalingWords.tsx  # Pop/bounce effect
│           ├── AnimatedBackground.tsx  # CapCut-style box
│           └── index.ts          # Style exports
│
├── scripts/
│   └── install-remotion.sh       # Remotion setup script
│
├── downloads/                     # Per-video working directories (gitignored)
│   ├── .gitkeep                  # Keeps folder in git
│   └── VIDEO_ID/                 # Individual video folders
│       ├── original.mp4          # Downloaded video
│       ├── original.json         # Whisper transcript with timestamps
│       ├── metadata.json         # Video metadata (title, duration, etc.)
│       ├── analysis_request.md   # Generated Claude prompt
│       ├── clip_recommendations.json # Claude's JSON output
│       ├── SUMMARY.md            # Final report with recommendations
│       └── clips/                # Generated clips
│           ├── clip_001_*.mp4           # Standard format
│           ├── clip_001_*_instagram.mp4 # 9:16 vertical
│           ├── clip_001_*_captioned.mp4 # With animated captions
│           └── clip_001_*_instagram_captioned.mp4  # 9:16 with captions
│
├── logs/                          # Reserved for future logging (gitignored)
│   └── .gitkeep
│
├── docs/                          # Additional documentation
│   ├── EXAMPLES.md               # Usage examples
│   ├── IMPLEMENTATION_STATUS.md  # Development status
│   └── SKILL_INSTALLATION.md     # Skill setup guide
│
├── legacy/                        # Old implementations (reference only)
│   ├── create_instagram_clips.py # Original hardcoded script
│   ├── clip_youtube_video.sh     # Shell script version
│   └── youtube_video_clipping_guide.md # Manual process docs
│
├── skill-package/                 # Claude Code skill package
│   └── viral-video-clipper/      # Skill installation files
│
└── viral-video-clipper.skill      # Packaged skill file
```

## Critical Code Patterns

### FFmpeg Clip Generation

The `generate_clips()` function creates two versions of each clip:

```python
# Standard clip (preserves aspect ratio)
ffmpeg -i original.mp4 -ss START -to END -c:v libx264 -c:a aac -preset fast -crf 23 output.mp4

# Instagram vertical (9:16 with padding)
ffmpeg -i clip.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black" output_instagram.mp4
```

### Whisper Transcript Formatting

Transcripts are formatted for Claude with `[MM:SS]` timestamps:
```
[00:05] This is the transcribed text
[00:12] Next segment of text
```

### Claude JSON Schema

The `clip_recommendations.json` must follow this structure:
```json
{
  "clips": [
    {
      "clip_number": 1,
      "start_time": 5.2,
      "end_time": 32.8,
      "duration": 27.6,
      "title": "Hook: Title Here",
      "description": "What happens in this clip",
      "virality_score": 9,
      "virality_factors": ["strong_hook", "visual_demo"],
      "suggested_caption": "Ready-to-use caption 🎯",
      "content_type": "hook",
      "target_audience": "Who this is for",
      "key_moments": ["0:05 - Event", "0:15 - Event"]
    }
  ],
  "video_summary": "Brief summary",
  "overall_theme": "Category",
  "target_audience": "Primary audience",
  "hashtag_suggestions": ["#tag1", "#tag2"]
}
```

### Validation Rules

The `validate_clip_recommendations()` function enforces:
- All timestamps within video duration
- start_time < end_time
- Duration between 15-60 seconds (warning if outside range)
- Required fields: start_time, end_time, title, description
- Clips ordered chronologically

## File Handling

### Per-Video Isolation

Each video gets its own directory under `downloads/VIDEO_ID/`:
- Prevents file conflicts when processing multiple videos
- Makes cleanup easy (delete one directory)
- Allows parallel processing in future

### Safe Filename Generation

Clip filenames are sanitized:
```python
safe_title = re.sub(r'[^\w\s-]', '', title)  # Remove special chars
safe_title = re.sub(r'[-\s]+', '_', safe_title)  # Replace spaces/dashes
filename = f"clip_{clip_num:03d}_{safe_title[:30]}"  # Limit length
```

## Troubleshooting Common Issues

### YouTube Download Failures
- Age-restricted videos require cookies (Chrome/Firefox)
- Region-blocked videos may need VPN
- Fallback: Manual download and use `--skip-download`

### Whisper Memory Issues
- Long videos (>30 min) may fail with base model
- Script automatically tries tiny model as fallback
- Manual: Edit script to force tiny model

### Invalid JSON from Claude
- Remove markdown code blocks (```json and ```)
- Validate with: `python -m json.tool clip_recommendations.json`
- Ensure file starts with `{` and ends with `}`

### FFmpeg Missing/Errors
- Install: `brew install ffmpeg` (macOS)
- Verify: `which ffmpeg`
- Path issues: Use absolute path to ffmpeg

## Integration Points

### Adding Claude API Support (Future)

To replace interactive mode with API calls, modify `invoke_claude_analysis()`:
1. Read prompt from `analysis_request.md`
2. Call Anthropic API with prompt
3. Parse JSON response
4. Save to `clip_recommendations.json`
5. Remove user input prompt

### Caption Generation (Phase 2 - Implemented)

The Remotion caption system works as follows:

1. **Whisper JSON Conversion** (`convert-whisper.ts`):
   - Extracts word-level timestamps from Whisper JSON
   - Converts to Remotion Caption format with startMs/endMs
   - Clips captions to the specific video segment

2. **Caption Styles** (`CaptionStyles/`):
   - `background`: Animated box jumps word-to-word (CapCut style)
   - `scaling`: Words pop/bounce with spring animation
   - `colored`: Active word highlighted in accent color

3. **Render Pipeline**:
   - `generate_captions_for_clip()` in Python calls Remotion render
   - Outputs `*_captioned.mp4` alongside standard clips
   - Creates 9:16 Instagram versions with captions

**To modify caption styles:**
- Edit components in `remotion-captions/src/CaptionStyles/`
- Preview with `npx remotion studio` in `remotion-captions/`
- Add new styles by creating new components and registering in `CaptionedClip.tsx`

## Phase 2: Remotion Captions

### Setup

```bash
# Install Remotion dependencies (requires Node.js 18+)
./scripts/install-remotion.sh

# Or manually
cd remotion-captions && npm install
```

### Caption Style Architecture

Each style is a React component that receives:
```typescript
interface CaptionStyleProps {
  captions: RemotionCaption[];  // Word-level captions
  currentFrame: number;         // Current video frame
  fps: number;                  // Frames per second
  accentColor: string;          // Highlight color
  fontFamily: string;           // Font family
}
```

The `getActiveWords()` utility finds which words are visible at the current frame,
allowing each style to animate based on timing.

### Adding New Caption Styles

1. Create component in `remotion-captions/src/CaptionStyles/NewStyle.tsx`
2. Export from `remotion-captions/src/CaptionStyles/index.ts`
3. Add to `CaptionStyle` type in `types.ts`
4. Add case in `CaptionRenderer` switch in `CaptionedClip.tsx`
5. Add choice to `--caption-style` in `ai_clip_generator.py`

### Whisper JSON Format

The converter expects Whisper's JSON format with word-level timestamps:
```json
{
  "segments": [{
    "start": 0.0,
    "end": 2.5,
    "text": "Hello world",
    "words": [
      {"word": "Hello", "start": 0.0, "end": 0.5},
      {"word": "world", "start": 0.5, "end": 1.0}
    ]
  }]
}
```

If word-level timestamps are unavailable, the converter estimates timing
by distributing segment duration evenly across words.

## Claude Prompt Engineering

The `clip_analysis_prompt.md` template is critical for output quality:

- **Selection Criteria:** Defines what makes clips viral (hooks, value bombs, emotional peaks, story arcs)
- **Constraints:** 15-60s duration, self-contained clips, natural speech boundaries
- **Output Format:** Strict JSON schema with validation rules
- **Quality Guidelines:** Prioritize visual demos, high energy, strong hooks

To improve clip quality, adjust:
1. Duration constraints (line 38)
2. Virality factors (line 82)
3. Content type categories (line 84)
4. Example clips (lines 88-103)

## Legacy Files

These files are preserved in the `legacy/` directory as reference implementations:
- `legacy/create_instagram_clips.py` - Original hardcoded clip script
- `legacy/clip_youtube_video.sh` - Shell script version
- `legacy/youtube_video_clipping_guide.md` - Manual process documentation

Do not modify these unless explicitly requested.
