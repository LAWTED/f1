#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title F1 Monitor Check
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🎯
# @raycast.packageName Singapore GP

# Documentation:
# @raycast.description Check for target F1 tickets (monitoring mode)
# @raycast.author lawted
# @raycast.authorURL https://raycast.com/lawted

# Set the script directory
SCRIPT_DIR="/Users/lawtedwu/Documents/f1"

# Change to script directory
cd "$SCRIPT_DIR" || {
    echo "❌ Error: Cannot find F1 ticket checker directory"
    echo "📁 Expected location: $SCRIPT_DIR"
    exit 1
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install requests beautifulsoup4 > /dev/null 2>&1
    echo "✅ Environment ready!"
else
    source venv/bin/activate
fi

# Show header
echo "🎯 Singapore GP Target Ticket Monitor"
echo "======================================"

# Show monitoring criteria
echo "🔍 Monitoring for:"
echo "   🔥 Sunday grandstand tickets"
echo "   🔥 3-day tickets ≤ \$1500"  
echo "   🟡 Grandstand tickets ≤ \$300"
echo ""

# Run monitor script
python3 monitor_tickets.py

echo ""
echo "🤖 For 24/7 monitoring, set up GitHub Actions (see MONITOR_SETUP.md)"