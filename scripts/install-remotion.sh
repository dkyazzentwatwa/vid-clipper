#!/bin/bash
#
# Install Remotion dependencies for animated captions
# Requires: Node.js 18+
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
REMOTION_DIR="$PROJECT_DIR/remotion-captions"

echo "========================================"
echo "  Remotion Captions Setup"
echo "========================================"
echo ""

# Check Node.js version
check_node() {
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found!"
        echo ""
        echo "Install Node.js 18+ using one of these methods:"
        echo "  brew install node        # macOS"
        echo "  nvm install 18           # Using nvm"
        echo "  fnm install 18           # Using fnm"
        exit 1
    fi

    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "❌ Node.js 18+ required (found v$NODE_VERSION)"
        echo "Please upgrade Node.js and try again."
        exit 1
    fi

    echo "✓ Node.js $(node -v) detected"
}

# Check npm
check_npm() {
    if ! command -v npm &> /dev/null; then
        echo "❌ npm not found!"
        exit 1
    fi
    echo "✓ npm $(npm -v) detected"
}

# Install dependencies
install_deps() {
    echo ""
    echo "Installing Remotion dependencies..."
    echo ""

    cd "$REMOTION_DIR"

    if [ -d "node_modules" ]; then
        echo "⚠️  node_modules already exists. Reinstalling..."
        rm -rf node_modules
    fi

    npm install

    echo ""
    echo "✓ Dependencies installed successfully!"
}

# Verify installation
verify_install() {
    echo ""
    echo "Verifying installation..."

    cd "$REMOTION_DIR"

    # Check if remotion CLI works
    if npx remotion --version &> /dev/null; then
        echo "✓ Remotion CLI: $(npx remotion --version)"
    else
        echo "❌ Remotion CLI verification failed"
        exit 1
    fi

    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "========================================"
    echo "  Usage"
    echo "========================================"
    echo ""
    echo "Generate clips with animated captions:"
    echo "  python3 ai_clip_generator.py <url> --add-captions"
    echo ""
    echo "Choose caption style:"
    echo "  --caption-style background  # CapCut style (default)"
    echo "  --caption-style scaling     # Pop/bounce effect"
    echo "  --caption-style colored     # Clean highlight"
    echo ""
    echo "Preview captions in browser:"
    echo "  cd remotion-captions && npx remotion studio"
    echo ""
}

# Main
main() {
    check_node
    check_npm
    install_deps
    verify_install
}

main
