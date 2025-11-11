#!/bin/bash
# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Log file
LOG_FILE="$SCRIPT_DIR/autostart.log"

# Log start
echo "=== $(date) ===" >> "$LOG_FILE"
echo "Starting Snooker Shot Clock..." >> "$LOG_FILE"
echo "DISPLAY=$DISPLAY" >> "$LOG_FILE"
echo "USER=$USER" >> "$LOG_FILE"
echo "PWD=$PWD" >> "$LOG_FILE"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated" >> "$LOG_FILE"
fi

# Run the application (redirect output to log)
echo "Executing: python3 main.py" >> "$LOG_FILE"
python3 main.py "$@" >> "$LOG_FILE" 2>&1
