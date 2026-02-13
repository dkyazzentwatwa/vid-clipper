#!/bin/bash
# Quick start script for AI Video Clipper

set -e

echo "=========================================="
echo "  AI Video Clipper - Quick Start"
echo "=========================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python 3 found"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found"
    echo "Install with: brew install ffmpeg"
    exit 1
fi
echo "✓ ffmpeg found"

# Install dependencies
echo
echo "📦 Installing Python dependencies..."
pip3 install -q yt-dlp openai-whisper || {
    echo "❌ Failed to install dependencies"
    exit 1
}
echo "✓ Dependencies installed"

# Test installation
echo
echo "🧪 Testing installation..."
python3 -c "import whisper; import yt_dlp" || {
    echo "❌ Import test failed"
    exit 1
}
echo "✓ All imports working"

echo
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo
echo "Usage:"
echo "  python3 ai_clip_generator.py <youtube_url>"
echo
echo "Example:"
echo "  python3 ai_clip_generator.py 'https://www.youtube.com/watch?v=QE_Nt5dMLHI'"
echo
