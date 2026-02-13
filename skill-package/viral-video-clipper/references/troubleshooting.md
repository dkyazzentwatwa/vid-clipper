# Troubleshooting Guide

## Common Issues and Solutions

### Download Failures

**YouTube 403 Forbidden Error**
```bash
# Update yt-dlp to latest version
brew upgrade yt-dlp
# Or with pip
pip install --upgrade yt-dlp
```

**Private/Age-Restricted Videos**
- Requires browser cookies authentication
- Script automatically tries Chrome then Firefox cookies
- Ensure you're logged into YouTube in your browser

**No cookies method working**
- Download manually and save as `downloads/{video_id}/original.mp4`
- Run script with `--skip-download` flag

### Transcription Issues

**Whisper Not Found**
```bash
pip install openai-whisper
```

**Memory Errors (Long Videos)**
```bash
# Use tiny model instead of base
whisper video.mp4 --model tiny --output_format json
```

**Slow Transcription**
- Expected for videos >10 minutes
- Use smaller model (tiny/base) for faster processing
- GPU acceleration: Install CUDA-enabled PyTorch

### Clip Generation Issues

**FFmpeg Not Found**
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

**Audio/Video Sync Problems**
- Usually caused by variable frame rate videos
- Re-encode with constant frame rate first:
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 23 -r 30 output.mp4
```

**Invalid Timestamps**
- Check that end_time doesn't exceed video duration
- Ensure start_time < end_time
- Verify timestamps are in seconds (not MM:SS format)

### JSON Validation Errors

**Invalid JSON from Claude**
- Remove markdown code blocks (```json)
- Ensure no extra text before/after JSON
- Validate at jsonlint.com

**Missing Required Fields**
Required in each clip:
- clip_number
- start_time
- end_time
- title
- description
- virality_score
- suggested_caption

**Timestamp Out of Range**
- Verify all timestamps are within video duration
- Check for decimal precision issues (use max 2 decimals)

## Performance Optimization

### Large Video Files

For videos >1 hour:
1. Use `--skip-download` if video already exists
2. Use `--skip-transcription` if transcript exists
3. Consider splitting into smaller segments first

### Disk Space

Each video requires ~3x its size in disk space:
- Original video
- Transcription temporary files
- Generated clips

Clean up with:
```bash
rm -rf downloads/{video_id}/original.info.json
rm -rf downloads/{video_id}/*.vtt
```

### Batch Processing

Process multiple videos:
```bash
for url in $(cat urls.txt); do
    python3 ai_clip_generator.py "$url"
done
```

## Installation Issues

### Python Version
- Requires Python 3.8+
- Check: `python3 --version`

### Permission Errors (macOS)
```bash
# Use brew instead of pip for system packages
brew install yt-dlp ffmpeg
```

### Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
