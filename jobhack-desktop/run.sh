#!/bin/bash
# JobHack Desktop Quick Start Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║              JOBHACK DESKTOP - QUICK START                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Java version
echo "Checking Java version..."
if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Please install Java 17 or higher."
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | awk -F'.' '{print $1}')
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "❌ Java 17 or higher required. Current version: $JAVA_VERSION"
    exit 1
fi
echo "✅ Java $JAVA_VERSION detected"

# Check Maven
echo "Checking Maven..."
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven not found. Please install Maven 3.6+"
    exit 1
fi
echo "✅ Maven detected"

# Check API key
echo "Checking Anthropic API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo "   Set it with: export ANTHROPIC_API_KEY='your-key'"
    echo "   Or configure in ~/.jobhack/application.conf"
else
    echo "✅ API key configured"
fi

echo ""
echo "Building JobHack Desktop..."
mvn clean compile -q

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Check errors above."
    exit 1
fi

echo "✅ Build successful"
echo ""
echo "Starting JobHack Desktop..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

mvn javafx:run
