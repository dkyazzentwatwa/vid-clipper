#!/bin/bash
# YouTube Video Clipping Script for Instagram Reels
# Video: "I Made an Apple Shortcuts MCP" by littlehakr
# Duration: 6:51

set -e

echo "=========================================="
echo "  YouTube Video Clipping Script"
echo "  Video: I Made an Apple Shortcuts MCP"
echo "=========================================="

VIDEO_URL="https://www.youtube.com/watch?v=QE_Nt5dMLHI"
OUTPUT_DIR="./instagram_clips"
INPUT_FILE="apple_shortcuts_mcp_original.mp4"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if video already downloaded
if [ ! -f "$INPUT_FILE" ]; then
    echo ""
    echo "Step 1: Downloading video..."
    echo ""
    
    # Try multiple download methods
    if command -v yt-dlp &> /dev/null; then
        echo "Using yt-dlp..."
        
        # Try with different methods
        yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
            -o "$INPUT_FILE" \
            "$VIDEO_URL" 2>/dev/null || \
        yt-dlp --cookies-from-browser chrome \
            -o "$INPUT_FILE" \
            "$VIDEO_URL" 2>/dev/null || \
        yt-dlp --cookies-from-browser firefox \
            -o "$INPUT_FILE" \
            "$VIDEO_URL" 2>/dev/null || \
        {
            echo ""
            echo "⚠️  Automated download blocked by YouTube."
            echo "Please download manually using one of these methods:"
            echo ""
            echo "1. Browser Extension: Video DownloadHelper"
            echo "2. Online: y2mate.com or savefrom.net"
            echo "3. Add 'ss' before youtube in URL: syoutube.com/watch?v=QE_Nt5dMLHI"
            echo ""
            echo "Save the downloaded file as: $INPUT_FILE"
            echo "Then run this script again."
            exit 1
        }
    else
        echo "yt-dlp not found. Please install it first:"
        echo "pip install yt-dlp"
        exit 1
    fi
fi

echo ""
echo "Step 2: Creating clips..."
echo ""

# Define clips (start, end, name, description)
declare -a CLIPS=(
    "0:00 0:30 clip1_hook 'THE HOOK - Introduction'"
    "1:00 1:45 clip2_demo 'THE DEMO - How It Works'"
    "2:30 3:15 clip3_gemini 'GEMINI CLI - Cross-Platform'"
    "4:00 4:45 clip4_usecase 'USE CASE - Practical Value'"
    "5:30 6:20 clip5_future 'FUTURE - AI Automation'"
)

# Create each clip
for clip_info in "${CLIPS[@]}"; do
    read -r start end name desc <<< "$clip_info"
    
    echo "Creating $name - $desc"
    echo "  Time: $start to $end"
    
    # Extract clip
    ffmpeg -i "$INPUT_FILE" \
        -ss "$start" -to "$end" \
        -c:v libx264 -c:a aac \
        -preset fast -crf 23 \
        -y "$OUTPUT_DIR/${name}.mp4" 2>/dev/null
    
    # Create Instagram vertical version (9:16)
    ffmpeg -i "$OUTPUT_DIR/${name}.mp4" \
        -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black" \
        -c:v libx264 -c:a aac \
        -preset fast -crf 23 \
        -y "$OUTPUT_DIR/${name}_instagram.mp4" 2>/dev/null
    
    echo "  ✓ Created ${name}.mp4 and ${name}_instagram.mp4"
    echo ""
done

echo "=========================================="
echo "  ✅ All clips created successfully!"
echo "=========================================="
echo ""
echo "Output files in $OUTPUT_DIR:"
ls -la "$OUTPUT_DIR"
echo ""
echo "Instagram-Ready Files (9:16 vertical):"
ls -la "$OUTPUT_DIR"/*_instagram.mp4
echo ""
echo "🎯 Next Steps:"
echo "1. Review each clip"
echo "2. Add text overlays/captions in Instagram or editing app"
echo "3. Add trending audio"
echo "4. Post with optimized hashtags!"
