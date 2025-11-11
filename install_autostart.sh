#!/bin/bash
# Install Snooker Shot Clock as autostart service
# This script creates a systemd service that starts the shot clock on boot

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICE_NAME="snooker-shotclock"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
USER=$(whoami)

echo "======================================"
echo "Snooker Shot Clock - Autostart Setup"
echo "======================================"
echo ""
echo "Installation directory: $SCRIPT_DIR"
echo "User: $USER"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run with sudo"
    echo "Usage: sudo ./install_autostart.sh"
    exit 1
fi

# Check if service already exists
if systemctl is-enabled --quiet ${SERVICE_NAME}.service 2>/dev/null; then
    echo "⚠️  Service is already installed!"
    echo ""
    read -p "Do you want to reinstall? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo "Stopping and removing existing service..."
    systemctl stop ${SERVICE_NAME}.service 2>/dev/null || true
    systemctl disable ${SERVICE_NAME}.service 2>/dev/null || true
fi

# Create systemd service file
echo "📝 Creating systemd service file..."
cat > ${SERVICE_FILE} << EOF
[Unit]
Description=Snooker Shot Clock
After=graphical.target network.target
Wants=graphical.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${SCRIPT_DIR}
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/${USER}/.Xauthority"
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/main.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical.target
EOF

echo "✅ Service file created: ${SERVICE_FILE}"
echo ""

# Set correct permissions
chmod 644 ${SERVICE_FILE}
echo "✅ Permissions set"
echo ""

# Reload systemd
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
echo "✅ Daemon reloaded"
echo ""

# Enable service
echo "🚀 Enabling service..."
systemctl enable ${SERVICE_NAME}.service
echo "✅ Service enabled"
echo ""

# Ask if user wants to start now
read -p "Do you want to start the service now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "▶️  Starting service..."
    systemctl start ${SERVICE_NAME}.service
    echo ""
    sleep 2
    
    # Check status
    if systemctl is-active --quiet ${SERVICE_NAME}.service; then
        echo "✅ Service is running!"
    else
        echo "❌ Service failed to start. Check logs:"
        echo "   sudo journalctl -u ${SERVICE_NAME}.service -n 50"
    fi
else
    echo "ℹ️  Service will start on next boot"
fi

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock will now start automatically on boot."
echo ""
echo "Useful commands:"
echo "  sudo systemctl start ${SERVICE_NAME}      - Start service"
echo "  sudo systemctl stop ${SERVICE_NAME}       - Stop service"
echo "  sudo systemctl restart ${SERVICE_NAME}    - Restart service"
echo "  sudo systemctl status ${SERVICE_NAME}     - Check status"
echo "  sudo journalctl -u ${SERVICE_NAME} -f    - View logs (live)"
echo ""
echo "To uninstall:"
echo "  sudo ./uninstall_autostart.sh"
echo ""
