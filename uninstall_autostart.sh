#!/bin/bash
# Uninstall Snooker Shot Clock Autostart

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "======================================"
echo "Snooker Shot Clock - Uninstall Autostart"
echo "======================================"
echo ""

# Remove all autostart entries
echo "Removing autostart entries..."
crontab -l 2>/dev/null | grep -v "snooker-shotclock\|${SCRIPT_DIR}/run.sh" | crontab - 2>/dev/null || true
rm -f ~/.config/autostart/snooker-shotclock.desktop 2>/dev/null || true

echo ""
echo "======================================"
echo "✅ Uninstall Complete!"
echo "======================================"
echo ""
echo "The app will no longer start automatically."
echo ""
