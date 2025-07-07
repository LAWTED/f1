#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Singapore GP Tickets
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🏎️
# @raycast.packageName Singapore GP

# Documentation:
# @raycast.description Check Singapore F1 ticket availability
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
echo "🏎️  Singapore GP Ticket Checker"
echo "=================================="

# Run ticket checker with available-only filter
echo "🔍 Checking available tickets..."
echo ""

python3 check_tickets.py --available-only

echo ""
echo "🔗 Buy tickets: https://singaporegp.sg/en/tickets/general-tickets/grandstands/"
echo ""
echo "💡 Tip: Run 'python monitor_tickets.py' for target ticket monitoring"

