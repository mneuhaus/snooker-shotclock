#!/bin/bash
# Uninstall Snooker Shot Clock from crontab

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "======================================"
echo "Snooker Shot Clock - Remove Cron Autostart"
echo "======================================"
echo ""

# Check if crontab entry exists
if ! crontab -l 2>/dev/null | grep -q "snooker-shotclock\|${SCRIPT_DIR}/run.sh"; then
    echo "ℹ️  Cron autostart is not installed."
    exit 0
fi

# Show current entry
echo "Current crontab entry:"
crontab -l | grep -A1 "Snooker"
echo ""

# Confirm removal
read -p "Remove this entry? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Remove crontab entry
echo "🗑️  Removing crontab entry..."
crontab -l | grep -v "snooker-shotclock\|${SCRIPT_DIR}/run.sh" | crontab -
echo "✅ Crontab entry removed"
echo ""

echo "======================================"
echo "✅ Uninstallation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock will no longer start automatically."
echo ""
echo "To run manually:"
echo "  ./run.sh"
echo ""
echo "To reinstall autostart:"
echo "  ./install_autostart_cron.sh"
echo ""
