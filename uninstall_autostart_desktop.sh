#!/bin/bash
# Uninstall Snooker Shot Clock Desktop Autostart

set -e  # Exit on error

DESKTOP_FILE="${HOME}/.config/autostart/snooker-shotclock.desktop"

echo "======================================"
echo "Snooker Shot Clock - Remove Desktop Autostart"
echo "======================================"
echo ""

# Check if desktop file exists
if [ ! -f "${DESKTOP_FILE}" ]; then
    echo "ℹ️  Desktop autostart is not installed."
    exit 0
fi

# Confirm removal
echo "This will remove the desktop autostart entry."
echo ""
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Remove desktop file
echo "🗑️  Removing autostart entry..."
rm -f "${DESKTOP_FILE}"
echo "✅ Desktop autostart removed"
echo ""

echo "======================================"
echo "✅ Uninstallation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock will no longer start automatically."
echo "The application files are still in place and can be run manually."
echo ""
echo "To run manually:"
echo "  ./run.sh"
echo ""
echo "To reinstall autostart:"
echo "  ./install_autostart_desktop.sh"
echo ""
