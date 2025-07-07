#!/bin/bash
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install requests beautifulsoup4
else
    source venv/bin/activate
fi

# Run the ticket checker
python3 check_tickets.py "$@"