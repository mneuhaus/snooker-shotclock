#!/bin/bash
# Install Snooker Shot Clock via crontab @reboot
# Alternative method that's more reliable on some systems

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER=$(whoami)

echo "======================================"
echo "Snooker Shot Clock - Cron Autostart"
echo "======================================"
echo ""
echo "Installation directory: $SCRIPT_DIR"
echo "User: $USER"
echo ""

# Check if crontab entry already exists
CRON_CMD="@reboot sleep 30 && DISPLAY=:0 ${SCRIPT_DIR}/run.sh"
if crontab -l 2>/dev/null | grep -q "snooker-shotclock\|${SCRIPT_DIR}/run.sh"; then
    echo "⚠️  Cron entry already exists!"
    echo ""
    echo "Current crontab:"
    crontab -l | grep -E "snooker|${SCRIPT_DIR}"
    echo ""
    read -p "Do you want to reinstall? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    # Remove old entry
    crontab -l | grep -v "snooker-shotclock\|${SCRIPT_DIR}/run.sh" | crontab -
fi

# Add new crontab entry
echo "📝 Adding crontab entry..."
(crontab -l 2>/dev/null; echo "# Snooker Shot Clock - Autostart") | crontab -
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "✅ Crontab entry added"
echo ""

# Show current crontab
echo "Current crontab:"
crontab -l | grep -A1 "Snooker"
echo ""

echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock will start 30 seconds after boot."
echo ""
echo "To test without rebooting:"
echo "  DISPLAY=:0 ${SCRIPT_DIR}/run.sh"
echo ""
echo "To view logs after reboot:"
echo "  Check ~/snooker-shotclock/shotclock.log (if logging enabled)"
echo ""
echo "To uninstall:"
echo "  ./uninstall_autostart_cron.sh"
echo ""
