#!/bin/bash
# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Log file
LOG_FILE="$SCRIPT_DIR/autostart.log"

# Setup environment for cron (no X11/Audio by default)
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}

# PulseAudio environment
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export PULSE_RUNTIME_PATH=/run/user/$(id -u)/pulse
export PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native

# Log start
echo "=== $(date) ===" >> "$LOG_FILE"
echo "Starting Snooker Shot Clock..." >> "$LOG_FILE"
echo "DISPLAY=$DISPLAY" >> "$LOG_FILE"
echo "USER=$USER" >> "$LOG_FILE"
echo "PWD=$PWD" >> "$LOG_FILE"
echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR" >> "$LOG_FILE"
echo "PULSE_SERVER=$PULSE_SERVER" >> "$LOG_FILE"

# Check for virtual environment in multiple locations
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated: venv/" >> "$LOG_FILE"
elif [ -f "$HOME/venv/bin/activate" ]; then
    source "$HOME/venv/bin/activate"
    echo "Virtual environment activated: $HOME/venv/" >> "$LOG_FILE"
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated: .venv/" >> "$LOG_FILE"
else
    echo "No virtual environment found, using system Python" >> "$LOG_FILE"
fi

# Find the correct Python with pygame
PYTHON_CMD="python3"
for py in python3.11 python3.9 python3.7 python3; do
    if command -v $py &> /dev/null; then
        if $py -c "import pygame" 2>/dev/null; then
            PYTHON_CMD=$py
            echo "Found Python with pygame: $PYTHON_CMD" >> "$LOG_FILE"
            break
        fi
    fi
done

# Run the application (redirect output to log)
echo "Executing: $PYTHON_CMD main.py" >> "$LOG_FILE"
$PYTHON_CMD main.py "$@" >> "$LOG_FILE" 2>&1
