#!/bin/bash
# Install Snooker Shot Clock Autostart
# Simple and reliable cron-based method

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "======================================"
echo "Snooker Shot Clock - Install Autostart"
echo "======================================"
echo ""

# Remove old entries if they exist
echo "Cleaning up old autostart entries..."
crontab -l 2>/dev/null | grep -v "snooker-shotclock\|${SCRIPT_DIR}/run.sh" | crontab - 2>/dev/null || true
rm -f ~/.config/autostart/snooker-shotclock.desktop 2>/dev/null || true

# Add cron entry
echo "Installing autostart (cron @reboot)..."
(crontab -l 2>/dev/null; echo "# Snooker Shot Clock") | crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && DISPLAY=:0 ${SCRIPT_DIR}/run.sh") | crontab -

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "The app will start automatically 30 seconds after boot."
echo ""
echo "To test: sudo reboot"
echo ""
