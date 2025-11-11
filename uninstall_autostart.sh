#!/bin/bash
# Uninstall Snooker Shot Clock autostart service
# This script removes the systemd service

set -e  # Exit on error

SERVICE_NAME="snooker-shotclock"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "======================================"
echo "Snooker Shot Clock - Autostart Removal"
echo "======================================"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run with sudo"
    echo "Usage: sudo ./uninstall_autostart.sh"
    exit 1
fi

# Check if service exists
if [ ! -f "${SERVICE_FILE}" ]; then
    echo "ℹ️  Service is not installed."
    exit 0
fi

# Confirm removal
echo "This will remove the autostart service for Snooker Shot Clock."
echo ""
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Stop service if running
if systemctl is-active --quiet ${SERVICE_NAME}.service; then
    echo "⏹️  Stopping service..."
    systemctl stop ${SERVICE_NAME}.service
    echo "✅ Service stopped"
    echo ""
fi

# Disable service
if systemctl is-enabled --quiet ${SERVICE_NAME}.service 2>/dev/null; then
    echo "🔓 Disabling service..."
    systemctl disable ${SERVICE_NAME}.service
    echo "✅ Service disabled"
    echo ""
fi

# Remove service file
echo "🗑️  Removing service file..."
rm -f ${SERVICE_FILE}
echo "✅ Service file removed"
echo ""

# Reload systemd
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
systemctl reset-failed 2>/dev/null || true
echo "✅ Daemon reloaded"
echo ""

echo "======================================"
echo "✅ Uninstallation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock service has been removed."
echo "The application files are still in place and can be run manually."
echo ""
echo "To run manually:"
echo "  python3 main.py"
echo ""
echo "To reinstall autostart:"
echo "  sudo ./install_autostart.sh"
echo ""
