# AI Video Clipper - Complete Example

This guide walks through the entire process of creating viral clips from a YouTube video using the AI Video Clipper.

## Example Video

We'll use this tech tutorial as our example:
- **Title:** "I Made an Apple Shortcuts MCP"
- **Author:** littlehakr
- **Duration:** 6:51
- **URL:** https://www.youtube.com/watch?v=QE_Nt5dMLHI
- **Content:** Demo of using AI to generate Apple Shortcuts via MCP protocol

## Prerequisites Check

Before starting, verify you have everything installed:

```bash
# Check Python version (need 3.8+)
python --version
# Output: Python 3.11.x (or similar)

# Check ffmpeg
ffmpeg -version
# Should show version info

# Check yt-dlp
yt-dlp --version
# Should show version number

# Check whisper
whisper --help
# Should show usage info
```

If any are missing, see the [Installation](README.md#installation) section in README.md.

## Step-by-Step Walkthrough

### Step 1: Run the Script

Open your terminal and navigate to the project directory:

```bash
cd /Users/cypher/Public/code/vid-clipper

# Run the AI clip generator
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

### Step 2: Video Download (1-2 minutes)

You'll see output like this:

```
============================================================
  AI-Powered Video Clipper
  Automated Viral Clip Generation
============================================================

✓ Video ID: QE_Nt5dMLHI
✓ Output directory: downloads/QE_Nt5dMLHI

📥 Downloading video...
   Video ID: QE_Nt5dMLHI

   Trying: Chrome cookies...
   ✓ Download successful!
   Title: I Made an Apple Shortcuts MCP 🤯
   Duration: 411s
```

**What's happening:**
- Script extracts video ID from URL
- Creates directory: `downloads/QE_Nt5dMLHI/`
- Tries multiple download methods (Chrome cookies first)
- Saves video as `original.mp4`
- Extracts metadata to `metadata.json`

**If download fails:**
```bash
# Try manual download with yt-dlp
yt-dlp -o downloads/QE_Nt5dMLHI/original.mp4 "https://www.youtube.com/watch?v=QE_Nt5dMLHI"

# Then re-run with skip flag
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI" --skip-download
```

### Step 3: Audio Transcription (2-5 minutes)

Next, Whisper will transcribe the audio:

```
🎙️  Transcribing video...
   Trying Whisper model: base...
   ✓ Transcription complete with base model
```

**What's happening:**
- Whisper extracts audio from video
- Generates text transcript with timestamps
- Saves to `original.json`
- Uses "base" model (better accuracy) or falls back to "tiny" (faster)

**Sample transcript output** (`original.json`):
```json
{
  "text": "hey everyone today I'm going to show you...",
  "segments": [
    {
      "start": 0.0,
      "end": 4.5,
      "text": "hey everyone today I'm going to show you"
    },
    {
      "start": 4.5,
      "end": 9.2,
      "text": "something really cool about MCP and Apple Shortcuts"
    }
  ]
}
```

### Step 4: Prompt Generation (instant)

The script formats the transcript for Claude:

```
📝 Generating Claude analysis prompt...
   ✓ Prompt saved to: downloads/QE_Nt5dMLHI/analysis_request.md
```

**What's created:**

`analysis_request.md` contains:
1. Video metadata (title, duration, etc.)
2. Formatted transcript with [MM:SS] timestamps:
   ```
   [00:00] hey everyone today I'm going to show you
   [00:04] something really cool about MCP and Apple Shortcuts
   [00:09] I built this server that lets AI like Claude
   ```
3. Instructions for Claude to analyze and identify clips

### Step 5: AI Analysis (Interactive - 2-5 minutes)

This is where you interact with Claude:

```
🤖 Claude AI Analysis Required
============================================================

Next steps:
1. Review the analysis prompt at:
   /Users/cypher/Public/code/vid-clipper/downloads/QE_Nt5dMLHI/analysis_request.md

2. Run Claude Code on this prompt to generate clip recommendations

3. Save Claude's JSON output to:
   /Users/cypher/Public/code/vid-clipper/downloads/QE_Nt5dMLHI/clip_recommendations.json

4. Press Enter when the JSON file is ready...
============================================================

Press Enter to continue...
```

**How to complete this step:**

#### Option A: Using Claude Code (Recommended)

```bash
# In another terminal, open Claude Code
claude code

# In the Claude Code interface, type:
"Please analyze the video transcript in downloads/QE_Nt5dMLHI/analysis_request.md
and generate clip recommendations. Save the JSON output to
downloads/QE_Nt5dMLHI/clip_recommendations.json"
```

#### Option B: Using Claude Web Interface

1. Open the file `downloads/QE_Nt5dMLHI/analysis_request.md`
2. Copy the entire contents
3. Go to https://claude.ai
4. Paste the prompt into Claude
5. Copy Claude's JSON response
6. Save to `downloads/QE_Nt5dMLHI/clip_recommendations.json`

**Expected Claude response:**

Claude will return JSON like this:

```json
{
  "clips": [
    {
      "clip_number": 1,
      "start_time": 0,
      "end_time": 28,
      "duration": 28,
      "title": "Hook: AI Creates Apple Shortcuts",
      "description": "Opens with bold claim and immediate demonstration of AI-powered shortcut creation",
      "virality_score": 9,
      "virality_factors": ["strong_hook", "visual_demo", "trending_topic"],
      "suggested_caption": "🤯 I made AI create Apple Shortcuts from scratch! This MCP server connects Claude to your iPhone automations 🔥",
      "content_type": "hook",
      "target_audience": "iOS users, automation enthusiasts, AI developers",
      "key_moments": ["0:00 - Hook intro", "0:10 - First demo", "0:23 - Quick result"]
    },
    {
      "clip_number": 2,
      "start_time": 60,
      "end_time": 95,
      "duration": 35,
      "title": "MCP Server Demo",
      "description": "Live demonstration of the MCP server generating shortcuts via AI commands",
      "virality_score": 8,
      "virality_factors": ["visual_demo", "value_bomb", "technical_showcase"],
      "suggested_caption": "Watch AI build a complex Apple Shortcut in SECONDS! ⚡️ The power of MCP is insane",
      "content_type": "demo",
      "target_audience": "Developers, tech enthusiasts, automation nerds",
      "key_moments": ["1:00 - Setup", "1:15 - AI command", "1:25 - Shortcut created"]
    },
    {
      "clip_number": 3,
      "start_time": 150,
      "end_time": 185,
      "duration": 35,
      "title": "Gemini CLI Integration",
      "description": "Testing the MCP server with Google's Gemini CLI for cross-platform AI control",
      "virality_score": 8,
      "virality_factors": ["trending_topic", "cross_platform", "visual_demo"],
      "suggested_caption": "Using Gemini CLI to control Apple Shortcuts 🧙‍♂️ Cross-platform AI automation is finally here!",
      "content_type": "demo",
      "target_audience": "Google AI users, iOS developers, tech early adopters",
      "key_moments": ["2:30 - Gemini intro", "2:45 - Command execution", "3:00 - Result"]
    }
  ],
  "video_summary": "Tutorial demonstrating an MCP server that enables AI assistants like Claude and Gemini to programmatically create and control Apple Shortcuts",
  "overall_theme": "AI Automation",
  "target_audience": "Tech enthusiasts, iOS developers, AI/automation early adopters",
  "hashtag_suggestions": ["#apple", "#shortcuts", "#AI", "#automation", "#MCP", "#gemini", "#claude", "#tech", "#ios", "#developer"]
}
```

**Save this JSON** to `downloads/QE_Nt5dMLHI/clip_recommendations.json`

**IMPORTANT:** Make sure the JSON is valid:
- Remove any markdown code blocks (```json and ```)
- File should start with `{` and end with `}`
- No extra text before or after the JSON

Once saved, press Enter in the terminal to continue.

### Step 6: Validation (instant)

The script validates Claude's recommendations:

```
✅ Validating clip recommendations...
   Found 3 clips
   ⚠️  Clip 2: duration 35.0s within 15-60s range
   ✓ All clips validated successfully
```

**What's checked:**
- JSON is properly formatted
- All required fields are present
- Timestamps are valid (start < end)
- Clips don't exceed video duration
- Reasonable clip lengths (15-60s)

### Step 7: Clip Generation (2-3 minutes)

FFmpeg creates the actual video clips:

```
✂️  Generating clips...

   📹 Creating clip 1: Hook: AI Creates Apple Shortcuts
      Time: 0:00 - 0:28
      ✓ Created clip_001_Hook_AI_Creates_Apple_Short.mp4
      ✓ Created clip_001_Hook_AI_Creates_Apple_Short_instagram.mp4 (9:16)

   📹 Creating clip 2: MCP Server Demo
      Time: 1:00 - 1:35
      ✓ Created clip_002_MCP_Server_Demo.mp4
      ✓ Created clip_002_MCP_Server_Demo_instagram.mp4 (9:16)

   📹 Creating clip 3: Gemini CLI Integration
      Time: 2:30 - 3:05
      ✓ Created clip_003_Gemini_CLI_Integration.mp4
      ✓ Created clip_003_Gemini_CLI_Integration_instagram.mp4 (9:16)

   ✅ Successfully created 3/3 clips
```

**What's happening:**
- FFmpeg extracts each clip from the original video
- Creates two versions per clip:
  - **Standard:** Preserves original aspect ratio
  - **Instagram:** Converts to 9:16 vertical (1080x1920)
- Adds black padding for vertical format
- Uses H.264 encoding for compatibility

### Step 8: Summary Report (instant)

A detailed report is generated:

```
📊 Generating summary report...
   ✓ Report saved to: downloads/QE_Nt5dMLHI/SUMMARY.md
```

### Completion

```
============================================================
  ✅ Video Clipping Complete!
============================================================

📁 All files saved to: downloads/QE_Nt5dMLHI
📊 Summary report: downloads/QE_Nt5dMLHI/SUMMARY.md
🎬 Generated 6 clip files

🎯 Next Steps:
1. Review clips in the clips/ directory
2. Use suggested captions from SUMMARY.md
3. Add captions (Phase 2 feature coming soon)
4. Post to Instagram/TikTok with recommended hashtags
```

## Expected Output Structure

After completion, you'll have:

```
downloads/QE_Nt5dMLHI/
├── original.mp4                      # Full video (411s, ~150MB)
├── original.json                     # Whisper transcript
├── original.info.json                # Raw yt-dlp metadata
├── metadata.json                     # Cleaned metadata
├── analysis_request.md               # Claude prompt
├── clip_recommendations.json         # AI analysis results
├── SUMMARY.md                        # Final report
└── clips/
    ├── clip_001_Hook_AI_Creates_Apple_Short.mp4
    ├── clip_001_Hook_AI_Creates_Apple_Short_instagram.mp4
    ├── clip_002_MCP_Server_Demo.mp4
    ├── clip_002_MCP_Server_Demo_instagram.mp4
    ├── clip_003_Gemini_CLI_Integration.mp4
    └── clip_003_Gemini_CLI_Integration_instagram.mp4
```

**File sizes:**
- Original video: ~150MB
- Each standard clip: ~5-15MB
- Each Instagram clip: ~8-20MB
- Total for 3 clips: ~60-100MB

## Reviewing the Output

### 1. Read the Summary Report

Open `downloads/QE_Nt5dMLHI/SUMMARY.md`:

```markdown
# Video Clipping Summary Report

## Video Information
- Title: I Made an Apple Shortcuts MCP 🤯
- Video ID: QE_Nt5dMLHI
- Duration: 411 seconds
- Generated: 2026-02-13 14:30:22

## Analysis Results
- Total Clips Recommended: 3
- Overall Theme: AI Automation
- Target Audience: Tech enthusiasts, iOS developers, AI/automation early adopters
- Hashtags: #apple, #shortcuts, #AI, #automation, #MCP, #gemini, #claude

## Generated Clips

### Clip 1: Hook: AI Creates Apple Shortcuts
- Time: 0:00 - 0:28
- Duration: 28.0s
- Virality Score: 9/10
- Description: Opens with bold claim and immediate demonstration
- Suggested Caption: 🤯 I made AI create Apple Shortcuts from scratch!
- Content Type: hook

[... more clips ...]
```

### 2. Watch the Clips

Open the clips in your video player:

```bash
# macOS
open downloads/QE_Nt5dMLHI/clips/clip_001_*_instagram.mp4

# Linux
vlc downloads/QE_Nt5dMLHI/clips/clip_001_*_instagram.mp4

# Windows
start downloads/QE_Nt5dMLHI/clips/clip_001_*_instagram.mp4
```

**What to check:**
- Clip starts and ends smoothly (no mid-sentence cuts)
- Audio is clear and in sync
- Content is engaging and self-contained
- Instagram version has proper vertical formatting

### 3. Choose Your Best Clips

Look for:
- High virality scores (8+)
- Strong hooks in first 3 seconds
- Clear value or entertainment
- Visual demonstrations (not just talking)

## Posting to Instagram/TikTok

### Preparing for Upload

1. **Choose the Instagram version:**
   - Use files ending in `_instagram.mp4`
   - These are pre-formatted for mobile (9:16)

2. **Transfer to your phone:**
   ```bash
   # Via AirDrop (macOS to iPhone)
   # Or use Google Drive, Dropbox, etc.
   ```

3. **Add finishing touches in Instagram:**
   - Trending audio/music
   - Text overlays or stickers
   - Filter adjustments

### Using the Suggested Captions

From `SUMMARY.md`, copy the suggested caption:

```
🤯 I made AI create Apple Shortcuts from scratch! This MCP server
connects Claude to your iPhone automations 🔥

#apple #shortcuts #AI #automation #MCP #gemini #claude #tech
```

**Pro tips:**
- Add call-to-action: "Follow for more AI automation tips!"
- Tag relevant accounts if appropriate
- Use line breaks for readability
- Include 5-10 hashtags (not all 20)

### Best Posting Times

Based on the target audience (tech enthusiasts):
- **Tuesday-Thursday:** 11 AM - 1 PM EST
- **Friday:** 2 PM - 4 PM EST
- **Weekend:** 9 AM - 11 AM EST

### Tracking Performance

After posting, monitor:
- Views in first 24 hours
- Engagement rate (likes + comments / views)
- Shares and saves
- Follower growth

Use insights to refine future clips!

## Tips for Best Results

### Content Selection

**Good video candidates:**
- Tech tutorials with visual demos
- Product showcases
- How-to guides with clear steps
- Reaction videos with emotional peaks
- Educational content with "aha" moments

**Less ideal:**
- Pure talking head with no visuals
- Very long, slow-paced content
- Poor audio quality
- Niche content without broad appeal

### Optimizing the AI Analysis

You can customize the prompt template to get better results:

**Edit:** `prompt_templates/clip_analysis_prompt.md`

**Examples of customizations:**

1. **Focus on specific content types:**
   ```
   Prioritize clips that demonstrate:
   - Visual "wow" moments
   - Technical implementations
   - Before/after comparisons
   ```

2. **Adjust duration preferences:**
   ```
   Duration: 20-35 seconds per clip (optimal: 25-30 seconds)
   ```

3. **Target different audiences:**
   ```
   Audience: Beginner-friendly, avoid technical jargon
   ```

### Batch Processing Multiple Videos

```bash
# Process several videos
python ai_clip_generator.py "https://youtube.com/watch?v=VIDEO1"
python ai_clip_generator.py "https://youtube.com/watch?v=VIDEO2"
python ai_clip_generator.py "https://youtube.com/watch?v=VIDEO3"

# Or create a script
for url in $(cat video_urls.txt); do
  python ai_clip_generator.py "$url"
done
```

### Saving Disk Space

After you've posted the clips:

```bash
# Delete the original video (keep clips)
rm downloads/QE_Nt5dMLHI/original.mp4

# Keep only Instagram versions
rm downloads/QE_Nt5dMLHI/clips/*[^instagram].mp4

# Archive old projects
tar -czf QE_Nt5dMLHI_clips.tar.gz downloads/QE_Nt5dMLHI/clips/
rm -rf downloads/QE_Nt5dMLHI/
```

## Common Issues and Solutions

### Issue: Clips are not engaging enough

**Solution:**
- Review the virality scores - only post clips rated 8+
- Manually adjust timestamps in `clip_recommendations.json`
- Look for moments with more energy/excitement
- Re-run with edited recommendations

### Issue: Audio is out of sync

**Solution:**
```bash
# Re-encode with audio sync
ffmpeg -i clip_001.mp4 -async 1 -c:v copy -c:a aac clip_001_fixed.mp4
```

### Issue: Vertical format has too much black padding

**Solution:**
The script uses black padding for videos that aren't 9:16. To use blur background instead:

```bash
# Custom Instagram conversion with blur background
ffmpeg -i clip_001.mp4 \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,
    setsar=1[fg];[0:v]scale=1080:1920:force_original_aspect_ratio=increase,
    boxblur=20:10,setsar=1[bg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:a copy clip_001_instagram_blur.mp4
```

### Issue: Want different clip suggestions

**Solution:**
1. Edit `clip_recommendations.json` manually
2. Adjust timestamps and titles
3. Re-run with skip flags:
   ```bash
   python ai_clip_generator.py "URL" --skip-download --skip-transcription
   ```

## Advanced: Customizing the Workflow

### Skip Steps You've Already Done

```bash
# Already have the video downloaded?
python ai_clip_generator.py "URL" --skip-download

# Already transcribed?
python ai_clip_generator.py "URL" --skip-download --skip-transcription

# Just want to regenerate clips with edited JSON?
python ai_clip_generator.py "URL" --skip-download --skip-transcription
# (Then manually update clip_recommendations.json between steps)
```

### Process a Local Video File

If you have a video file that's not from YouTube:

```bash
# Create the directory structure
mkdir -p downloads/my_video
cp my_video.mp4 downloads/my_video/original.mp4

# Create minimal metadata
echo '{"video_id": "my_video", "duration": 600}' > downloads/my_video/metadata.json

# Run transcription manually
whisper downloads/my_video/original.mp4 --output_format json --output_dir downloads/my_video

# Continue with the rest of the workflow
python ai_clip_generator.py "https://youtube.com/watch?v=my_video" --skip-download
```

## Next Steps

Now that you've successfully created clips:

1. **Experiment with different videos**
   - Try various content types
   - Find what works for your audience

2. **Build a content calendar**
   - Process 5-10 videos per week
   - Schedule posts consistently

3. **Track and iterate**
   - Note which clips perform best
   - Adjust your selection criteria
   - Refine captions and hashtags

4. **Explore Phase 2 features**
   - Stay tuned for automated caption generation
   - Test Remotion-based overlays when available

## Questions?

- Check the [Troubleshooting](README.md#troubleshooting) section
- Review this example again
- Open an issue with your specific case

Happy clipping!
