# YouTube Video Clipping Guide for Instagram Reels

> **NOTE:** This guide demonstrates manual video clipping. For automated AI-powered clipping, see the new **[AI Video Clipper](README.md)** tool that uses Claude AI to automatically identify viral-worthy moments!
>
> **Quick Start:**
> ```bash
> python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
> ```
>
> See [README.md](README.md) for full documentation and [EXAMPLES.md](EXAMPLES.md) for a complete walkthrough.

---

## Original Manual Clipping Guide

This guide shows the manual process of analyzing and clipping videos. The AI Video Clipper automates most of these steps!

## Video Information

| Property | Value |
|----------|-------|
| **Title** | I Made an Apple Shortcuts MCP 🤯 |
| **Author** | littlehakr (19.1K subscribers) |
| **Duration** | 6:51 (6 minutes 51 seconds) |
| **URL** | https://www.youtube.com/watch?v=QE_Nt5dMLHI |
| **Views** | ~126 views |
| **Posted** | ~3 weeks ago |

## Video Description

"I made an Apple Shortcuts MCP that connects to AI to generate Shortcuts for you! Check it out as I test it using Gemini CLI. Coming soon?"

## Content Analysis

### What is this video about?
This is a tech tutorial/demo video showcasing:
1. **MCP (Model Context Protocol)** - A protocol for AI assistants to interact with external tools
2. **Apple Shortcuts Integration** - Creating shortcuts programmatically using AI
3. **Gemini CLI Testing** - Demonstrating the MCP server with Google's Gemini CLI

### Target Audience
- Tech enthusiasts
- Apple ecosystem users
- AI/automation developers
- MCP protocol adopters

## Recommended 5 Instagram Clip Segments

Based on the video content type and viral potential, here are the recommended segments for Instagram Reels (optimized for 15-60 second clips):

### Clip 1: THE HOOK (0:00 - 0:30)
**Title:** "I Made AI Create Apple Shortcuts!"  
**Why viral:** Immediate hook showing the revolutionary concept  
**Content:** Introduction/demo of the MCP concept  
**Instagram format:** 9:16 vertical, add text overlay with key points

### Clip 2: THE "HOW IT WORKS" (1:00 - 1:45)
**Title:** "Watch AI Build Shortcuts in Real-Time"  
**Why viral:** Demonstrates the "magic" moment - AI creating something useful  
**Content:** Technical demonstration of the MCP server in action  
**Instagram format:** 9:16 vertical, speed up 1.5x for engagement

### Clip 3: THE GEMINI CLI DEMO (2:30 - 3:15)
**Title:** "Using Gemini CLI to Control Apple Shortcuts"  
**Why viral:** Cross-platform appeal (Google + Apple + AI)  
**Content:** Testing the MCP with Gemini CLI  
**Instagram format:** 9:16 vertical, highlight command inputs

### Clip 4: THE PRACTICAL USE CASE (4:00 - 4:45)
**Title:** "This Shortcut Would Take HOURS to Make Manually"  
**Why viral:** Shows time-saving value proposition  
**Content:** Complex shortcut created effortlessly  
**Instagram format:** 9:16 vertical, before/after comparison

### Clip 5: THE FUTURE OF AI AUTOMATION (5:30 - 6:20)
**Title:** "The Future of AI Automation is Here"  
**Why viral:** Forward-looking, inspiring content  
**Content:** Closing thoughts, possibilities, "coming soon" teaser  
**Instagram format:** 9:16 vertical, add inspiring music

---

## How to Download & Clip the Video

### Method 1: Using yt-dlp (Recommended)

```bash
# Install yt-dlp
pip install yt-dlp

# Download the video (highest quality)
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  -o "apple_shortcuts_mcp.mp4" \
  "https://www.youtube.com/watch?v=QE_Nt5dMLHI"

# Or download with cookies if blocked
yt-dlp --cookies-from-browser chrome \
  -o "apple_shortcuts_mcp.mp4" \
  "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

### Method 2: Using Browser Extension
1. Install "Video DownloadHelper" or similar extension
2. Play the video on YouTube
3. Click the extension to download

### Method 3: Online Services
- y2mate.com
- savefrom.net
- ssyoutube.com (add "ss" before youtube in URL)

---

## Clipping with FFmpeg

Once you have the video downloaded, use these FFmpeg commands to create your Instagram clips:

### Clip 1 (0:00 - 0:30)
```bash
ffmpeg -i apple_shortcuts_mcp.mp4 -ss 0:00 -to 0:30 -c:v libx264 -c:a aac -strict experimental clip1_hook.mp4
```

### Clip 2 (1:00 - 1:45)
```bash
ffmpeg -i apple_shortcuts_mcp.mp4 -ss 1:00 -to 1:45 -c:v libx264 -c:a aac -strict experimental clip2_demo.mp4
```

### Clip 3 (2:30 - 3:15)
```bash
ffmpeg -i apple_shortcuts_mcp.mp4 -ss 2:30 -to 3:15 -c:v libx264 -c:a aac -strict experimental clip3_gemini.mp4
```

### Clip 4 (4:00 - 4:45)
```bash
ffmpeg -i apple_shortcuts_mcp.mp4 -ss 4:00 -to 4:45 -c:v libx264 -c:a aac -strict experimental clip4_usecase.mp4
```

### Clip 5 (5:30 - 6:20)
```bash
ffmpeg -i apple_shortcuts_mcp.mp4 -ss 5:30 -to 6:20 -c:v libx264 -c:a aac -strict experimental clip5_future.mp4
```

### Convert to Instagram Reel Format (9:16 vertical)
```bash
# For each clip, convert to vertical format with blur background
ffmpeg -i clip1_hook.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black,setsar=1" \
  -c:v libx264 -c:a aac -preset fast -crf 23 \
  clip1_hook_instagram.mp4
```

---

## Instagram Reel Optimization Tips

### Caption Ideas:

**Clip 1:**
> 🤯 I made AI create Apple Shortcuts from scratch! 
> 
> This MCP server connects Claude & Gemini directly to your iPhone automations.
> 
> 🔗 Link in bio for the full breakdown
> 
> #apple #shortcuts #AI #automation #MCP #gemini #claude #tech

**Clip 2:**
> Watch AI build a shortcut in SECONDS that would take me HOURS manually 💪
> 
> The power of MCP + Apple Shortcuts is insane!
> 
> #automation #AI #apple #developer #shortcuts

**Clip 3:**
> Using Gemini CLI to control Apple Shortcuts 🧙‍♂️
> 
> Cross-platform AI automation is finally here!
> 
> #gemini #googleAI #apple #MCP #tech

### Hashtag Strategy:
Primary: #apple #shortcuts #AI #automation #MCP
Secondary: #iphone #mac #developer #productivity #tech
Trending: #AItools #automationtools #appleecosystem

### Best Posting Times:
- Tuesday-Thursday: 11 AM - 1 PM
- Friday: 2 PM - 4 PM
- Weekend: 9 AM - 11 AM

---

## Note on Video Downloading

YouTube has strict bot detection that prevents automated downloading. You'll need to:

1. **Use browser cookies** - yt-dlp can use cookies from your browser
2. **Download manually** - Use browser extensions or online tools
3. **Run locally** - The scripts above will work on your local machine

Once you have the video file, all the FFmpeg commands will work perfectly!

---

## Quick Start Script

Save this as `create_clips.sh` and run after downloading the video:

```bash
#!/bin/bash
INPUT="apple_shortcuts_mcp.mp4"

# Create clips
ffmpeg -i $INPUT -ss 0:00 -to 0:30 -c:v libx264 -c:a aac clip1_hook.mp4
ffmpeg -i $INPUT -ss 1:00 -to 1:45 -c:v libx264 -c:a aac clip2_demo.mp4
ffmpeg -i $INPUT -ss 2:30 -to 3:15 -c:v libx264 -c:a aac clip3_gemini.mp4
ffmpeg -i $INPUT -ss 4:00 -to 4:45 -c:v libx264 -c:a aac clip4_usecase.mp4
ffmpeg -i $INPUT -ss 5:30 -to 6:20 -c:v libx264 -c:a aac clip5_future.mp4

# Convert to Instagram format
for clip in clip*.mp4; do
  ffmpeg -i $clip \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black" \
    -c:v libx264 -c:a aac \
    ${clip%.mp4}_instagram.mp4
done

echo "All clips created successfully!"
```

---

## Comparison: Manual vs AI-Powered Workflow

### Manual Workflow (This Guide)
1. Manually watch and identify interesting moments
2. Note timestamps
3. Download video with yt-dlp
4. Run FFmpeg commands for each clip
5. Create Instagram versions manually
6. Write your own captions and hashtags

**Time:** 1-2 hours per video

### AI-Powered Workflow (Recommended)
1. Run: `python ai_clip_generator.py "URL"`
2. Review Claude's AI analysis
3. Let the script generate all clips automatically
4. Get AI-suggested captions and hashtags

**Time:** 10-15 minutes per video

### Which to Use?

**Use Manual Workflow when:**
- You want complete creative control
- You have specific clip ideas in mind
- You're clipping content you know very well
- You need custom clip boundaries

**Use AI-Powered Workflow when:**
- You want to save time
- You're processing multiple videos
- You want data-driven clip selection
- You need consistent quality across many videos

**Best Practice:** Use AI-powered workflow for initial clip discovery, then manually refine the best performers!

---

## Migration Guide: From Manual to AI-Powered

If you've been using this manual guide, here's how to switch:

### Step 1: Install the AI Tool
```bash
pip install -r requirements.txt
```

### Step 2: Run on the Same Video
```bash
python ai_clip_generator.py "https://www.youtube.com/watch?v=QE_Nt5dMLHI"
```

### Step 3: Compare Results
- Manual clips: Your hand-picked moments
- AI clips: Claude's recommendations with virality scores

### Step 4: Combine Approaches
- Use AI to discover clips you might have missed
- Use manual clipping for specific creative visions
- Let AI handle bulk processing, manual for special cases

---

*Original manual guide preserved below for reference. Consider using the [AI Video Clipper](README.md) for automated workflow!*

