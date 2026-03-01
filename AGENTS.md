# AGENTS.md

## Project Purpose
`vid-clipper` converts long-form videos into short, viral-ready social clips (Reels/TikTok) using:
1. video ingest/download,
2. Whisper transcription,
3. AI-based clip recommendation,
4. FFmpeg clip rendering,
5. optional caption workflows.

This repository currently contains:
- Main script: `/Users/cypher/Public/code/vid-clipper/ai_clip_generator.py`
- Prompt template: `/Users/cypher/Public/code/vid-clipper/prompt_templates/clip_analysis_prompt.md`
- Skill package(s):
  - `/Users/cypher/Public/code/vid-clipper/skill-package/viral-video-clipper`
  - `/Users/cypher/Public/code/vid-clipper/skill-package/universal-video-clipper`

## Primary Skill To Use
Use `viral-video-clipper` when the task is to generate clips from a YouTube video.
Skill file:
- `/Users/cypher/.codex/skills/viral-video-clipper/SKILL.md`

If the user provides a local/uploaded file path, prefer `universal-video-clipper`.
Skill file:
- `/Users/cypher/.codex/skills/universal-video-clipper/SKILL.md`

## Standard Operating Workflow

### A) YouTube Source (`viral-video-clipper`)
Run:
```bash
python3 /Users/cypher/Public/code/vid-clipper/ai_clip_generator.py "<youtube-url>"
```

### B) Local/Uploaded Source (`universal-video-clipper`)
Run:
```bash
python3 /Users/cypher/.codex/skills/universal-video-clipper/scripts/ai_clip_generator.py "</absolute/path/to/video>"
```

### C) Interactive Analysis Step (Required)
The script pauses after generating `analysis_request.md` and waits for:
- `clip_recommendations.json` in the video output folder.

Agent must:
1. Read transcript and metadata.
2. Produce valid JSON recommendations (3-7 clips, timestamps within bounds).
3. Save JSON to the expected path.
4. Continue the paused run (press Enter programmatically).

## Dependencies
Verify before major runs:
```bash
yt-dlp --version
whisper --help
ffmpeg -version
```

Install if needed:
```bash
pip install -r /Users/cypher/Public/code/vid-clipper/requirements.txt
brew install ffmpeg
```

## Output Contract
For each processed video, expected artifacts live under:
- `/Users/cypher/Public/code/vid-clipper/downloads/<video_id>/`

Required files:
- `original.*` (downloaded/copied source)
- `original.json` (transcript)
- `metadata.json`
- `analysis_request.md`
- `clip_recommendations.json`
- `SUMMARY.md`
- `clips/*.mp4` (standard + `_instagram.mp4` variants)

## JSON Recommendation Requirements
`clip_recommendations.json` must contain:
- top-level `clips` array,
- each clip with: `start_time`, `end_time`, `title`, `description`,
- non-overlapping, valid ranges,
- timestamp boundaries inside source duration,
- recommended duration target: 15-60 seconds.

## Project-Specific Guardrails
1. Do not claim success without verifying rendered files exist.
2. If transcription succeeds but no JSON transcript appears, inspect Whisper output naming/path behavior.
3. For silent videos (no audio stream), generate a placeholder transcript and continue with visual-only recommendations.
4. Keep clip titles filesystem-safe and concise.
5. Preserve existing user changes in unrelated files.

## Fast Validation Checklist
After each run:
```bash
find /Users/cypher/Public/code/vid-clipper/downloads/<video_id> -maxdepth 2 -type f | sort
```

Confirm:
- summary exists,
- recommendations JSON exists,
- expected number of clip files were generated,
- instagram variants exist.

## Troubleshooting Shortcuts
- Download issues: `brew upgrade yt-dlp`
- Whisper missing: `pip install openai-whisper`
- FFmpeg missing: `brew install ffmpeg`
- Invalid recommendation JSON: remove markdown fences and revalidate required fields.

## Definition of Done
A task is complete when:
1. Pipeline reaches final success banner,
2. clips are rendered and discoverable on disk,
3. `SUMMARY.md` is generated,
4. output paths are reported clearly to the user.
