# AI Video Clipper - Complete Example

This guide walks through the entire process of creating viral clips from a YouTube video using the AI Video Clipper.

---

## Quick Start with Natural Language

Instead of running CLI commands, simply tell an AI assistant what you want:

> "Create viral clips from this YouTube video: https://www.youtube.com/watch?v=QE_Nt5dMLHI"

The AI will handle everything - downloading, transcribing, analyzing, and generating the clips.

---

## Example Video

We'll use this tech tutorial as our example:
- **Title:** "I Made an Apple Shortcuts MCP"
- **Author:** littlehakr
- **Duration:** 6:51
- **URL:** https://www.youtube.com/watch?v=QE_Nt5dMLHI
- **Content:** Demo of using AI to generate Apple Shortcuts via MCP protocol

---

## Prerequisites Check

Before first use, verify you have everything installed:

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

---

## Step-by-Step Walkthrough

### Step 1: Start the Process

**Natural Language (Recommended):**
Tell your AI assistant:
> "Create viral clips from https://www.youtube.com/watch?v=QE_Nt5dMLHI"

**Or via CLI (Alternative):**
```bash
cd /Users/cypher/Public/code/vid-clipper
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

### Step 2: Video Download (1-2 minutes)

The tool downloads the YouTube video:

```
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

### Step 3: Audio Transcription (2-5 minutes)

Whisper transcribes the audio:

```
🎙️  Transcribing video...
   Trying Whisper model: base...
   ✓ Transcription complete with base model
```

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

### Step 4: AI Analysis (Interactive)

The script pauses and waits for AI analysis:

```
🤖 AI Analysis Required
============================================================
Next steps:
1. Review the analysis prompt at:
   downloads/QE_Nt5dMLHI/analysis_request.md

2. Run AI on this prompt to generate clip recommendations

3. Save AI's JSON output to:
   downloads/QE_Nt5dMLHI/clip_recommendations.json

4. Press Enter when the JSON file is ready...
============================================================
```

**How to complete this step:**

1. Read `downloads/QE_Nt5dMLHI/analysis_request.md` - Contains the transcript with timestamps
2. Run an AI on this prompt to analyze and recommend clips
3. The AI returns JSON with 3-7 clip recommendations
4. Save the JSON to `clip_recommendations.json`
5. Press Enter to continue

**Expected AI response format:**

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
      "content_type": "hook"
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
      "content_type": "demo"
    }
  ],
  "video_summary": "Tutorial demonstrating an MCP server that enables AI assistants to programmatically create Apple Shortcuts",
  "overall_theme": "AI Automation",
  "hashtag_suggestions": ["#apple", "#shortcuts", "#AI", "#automation", "#MCP"]
}
```

### Step 5: Clip Generation (2-3 minutes)

FFmpeg creates the video clips:

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

   ✅ Successfully created 3/3 clips
```

### Step 6: Summary Report

A detailed report is generated at `SUMMARY.md` with:
- Virality scores
- Suggested captions with emojis
- Hashtag recommendations
- Target audience insights

---

## Expected Output Structure

After completion:

```
downloads/QE_Nt5dMLHI/
├── original.mp4                      # Full video (411s, ~150MB)
├── original.json                     # Whisper transcript
├── metadata.json                     # Video info
├── analysis_request.md               # AI prompt
├── clip_recommendations.json         # AI analysis results
├── SUMMARY.md                        # Final report
└── clips/
    ├── clip_001_Hook_AI_Creates_Apple_Short.mp4
    ├── clip_001_Hook_AI_Creates_Apple_Short_instagram.mp4
    ├── clip_002_MCP_Server_Demo.mp4
    ├── clip_002_MCP_Server_Demo_instagram.mp4
    └── ...
```

---

## Reviewing the Output

### 1. Read the Summary Report

Open `downloads/QE_Nt5dMLHI/SUMMARY.md`:

```markdown
# Video Clipping Summary Report

## Video Information
- Title: I Made an Apple Shortcuts MCP 🤯
- Duration: 411 seconds

## Generated Clips

### Clip 1: Hook: AI Creates Apple Shortcuts
- Time: 0:00 - 0:28
- Duration: 28.0s
- Virality Score: 9/10
- Suggested Caption: 🤯 I made AI create Apple Shortcuts from scratch!
```

### 2. Watch the Clips

Open the clips in your video player:
```bash
# macOS
open downloads/QE_Nt5dMLHI/clips/clip_001_*_instagram.mp4
```

### 3. Choose Your Best Clips

Look for:
- High virality scores (8+)
- Strong hooks in first 3 seconds
- Clear value or entertainment
- Visual demonstrations

---

## Posting to Instagram/TikTok

### Using the Suggested Captions

From `SUMMARY.md`, copy the suggested caption:

```
🤯 I made AI create Apple Shortcuts from scratch! This MCP server
connects Claude to your iPhone automations 🔥

#apple #shortcuts #AI #automation #MCP #tech
```

**Pro tips:**
- Add call-to-action: "Follow for more AI automation tips!"
- Use line breaks for readability
- Include 5-10 hashtags (not all 20)

---

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

### Optimizing the AI Analysis

You can customize the prompt template: `prompt_templates/clip_analysis_prompt.md`

**Examples of customizations:**

1. **Focus on specific content types:**
   ```
   Prioritize clips that demonstrate:
   - Visual "wow" moments
   - Technical implementations
   ```

2. **Adjust duration preferences:**
   ```
   Duration: 20-35 seconds per clip (optimal: 25-30 seconds)
   ```

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Download fails | `brew upgrade yt-dlp` or use browser cookies |
| Transcription fails | `pip install openai-whisper` |
| Invalid JSON from AI | Remove markdown code blocks, validate required fields |

---

## CLI Reference (Alternative)

If you prefer direct script execution instead of natural language:

```bash
# Basic usage
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"

# Skip download if already exists
python ai_clip_generator.py "URL" --skip-download

# Skip transcription if already done
python ai_clip_generator.py "URL" --skip-download --skip-transcription

# With animated captions
python ai_clip_generator.py "URL" --add-captions
python ai_clip_generator.py "URL" --add-captions --caption-style scaling
```

---

## Next Steps

Now that you've successfully created clips:

1. **Experiment** - Try various content types
2. **Build a calendar** - Process videos consistently
3. **Track performance** - Note which clips perform best
4. **Iterate** - Adjust selection criteria and captions

Happy clipping!
