# Project Structure

This document explains the organization of the AI Video Clipper project.

## Directory Overview

```
vid-clipper/
├── Core Files (Root Level)
│   ├── ai_clip_generator.py      # Main script - runs the entire workflow
│   ├── requirements.txt           # Python dependencies
│   ├── CLAUDE.md                  # Development guide for AI assistants
│   ├── README.md                  # User documentation
│   ├── quick_start.sh             # Quick setup helper
│   └── .gitignore                 # Git ignore rules
│
├── docs/                          # Additional Documentation
│   ├── EXAMPLES.md                # Usage examples and tutorials
│   ├── IMPLEMENTATION_STATUS.md   # Development roadmap and status
│   └── SKILL_INSTALLATION.md      # Claude Code skill setup guide
│
├── legacy/                        # Old Implementations (Reference Only)
│   ├── create_instagram_clips.py  # Original hardcoded approach
│   ├── clip_youtube_video.sh      # Shell script version
│   └── youtube_video_clipping_guide.md  # Manual process docs
│
├── prompt_templates/              # AI Analysis Templates
│   └── clip_analysis_prompt.md    # Claude AI clip identification prompt
│
├── downloads/                     # Video Processing Workspace (Ignored by Git)
│   ├── .gitkeep                   # Keeps folder structure in git
│   └── {VIDEO_ID}/                # Per-video directories
│       ├── original.mp4           # Downloaded video
│       ├── original.json          # Whisper transcript
│       ├── metadata.json          # Video info
│       ├── analysis_request.md    # Generated AI prompt
│       ├── clip_recommendations.json  # AI analysis output
│       ├── SUMMARY.md             # Final report
│       └── clips/                 # Generated clip files
│           ├── clip_001_*.mp4     # Standard clips
│           └── clip_001_*_instagram.mp4  # 9:16 Instagram versions
│
├── logs/                          # Application Logs (Ignored by Git)
│   └── .gitkeep                   # Future logging directory
│
├── skill-package/                 # Claude Code Skill Package
│   └── universal-video-clipper/   # Skill source files (handles YouTube + local files)
│
└── universal-video-clipper.skill  # Packaged skill file for installation
```

## What Gets Tracked by Git?

### ✅ Tracked (Versioned)
- Core Python scripts (`ai_clip_generator.py`)
- Documentation files (`*.md`)
- Prompt templates (`prompt_templates/`)
- Requirements file (`requirements.txt`)
- Skill package source files
- Empty directory markers (`.gitkeep`)

### ❌ Ignored (Not Tracked)
- All video files (`downloads/` contents)
- Generated clips and transcripts
- Python cache (`__pycache__/`)
- Virtual environments (`venv/`, `env/`)
- System files (`.DS_Store`, `Thumbs.db`)
- IDE configurations (`.vscode/`, `.idea/`)
- Log files (`logs/` contents)

## Key Files Explained

### Root Level

**`ai_clip_generator.py`** - The main orchestrator that:
- Downloads YouTube videos
- Transcribes audio with Whisper
- Generates AI analysis prompts
- Creates clips with FFmpeg
- Produces summary reports

**`CLAUDE.md`** - Project guide for AI assistants containing:
- Architecture overview
- Development commands
- Code patterns and conventions
- Integration points for future features

**`README.md`** - User-facing documentation with:
- Installation instructions
- Quick start guide
- Usage examples
- Troubleshooting tips

### Prompt Templates

**`clip_analysis_prompt.md`** - The AI analysis template that:
- Defines viral clip selection criteria
- Specifies output JSON format
- Provides examples of high-performing clips
- Sets quality guidelines

This template is critical - it determines the quality of AI-identified clips.

### Documentation (`docs/`)

**`EXAMPLES.md`** - Real-world usage examples
**`IMPLEMENTATION_STATUS.md`** - Development progress tracker
**`SKILL_INSTALLATION.md`** - Guide for installing the Claude Code skill

### Legacy (`legacy/`)

Historical implementations kept for reference:
- Shows the evolution from manual to AI-powered workflow
- Useful for understanding design decisions
- Not actively maintained

## Working with the Project

### For Development
1. Edit `ai_clip_generator.py` for core functionality
2. Update `prompt_templates/clip_analysis_prompt.md` to improve clip quality
3. Modify `CLAUDE.md` when architecture changes

### For Documentation
1. Update `README.md` for user-facing changes
2. Add examples to `docs/EXAMPLES.md`
3. Track progress in `docs/IMPLEMENTATION_STATUS.md`

### For Video Processing
1. Run `python3 ai_clip_generator.py "<youtube-url>"`
2. Output goes to `downloads/{VIDEO_ID}/`
3. Each video gets its own isolated directory

## Git Workflow

### Initialize Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### What You'll Commit
- Source code changes
- Documentation updates
- Template modifications
- Configuration files

### What You Won't Commit
- Downloaded videos in `downloads/`
- Generated clips and transcripts
- Python cache and logs
- System files

## Clean Up Commands

### Remove all generated content
```bash
rm -rf downloads/*/
rm -rf logs/*.log
```

### Clean Python cache
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Remove system files
```bash
find . -name ".DS_Store" -delete
```

---

Last updated: 2026-02-13
