#!/bin/bash
# Install Snooker Shot Clock as Desktop Autostart (User Session)
# This method works better for GUI applications on Raspberry Pi

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER=$(whoami)
AUTOSTART_DIR="${HOME}/.config/autostart"
DESKTOP_FILE="${AUTOSTART_DIR}/snooker-shotclock.desktop"

echo "======================================"
echo "Snooker Shot Clock - Desktop Autostart"
echo "======================================"
echo ""
echo "Installation directory: $SCRIPT_DIR"
echo "User: $USER"
echo ""

# Create autostart directory if it doesn't exist
mkdir -p "${AUTOSTART_DIR}"
echo "✅ Autostart directory ready: ${AUTOSTART_DIR}"
echo ""

# Check if desktop file already exists
if [ -f "${DESKTOP_FILE}" ]; then
    echo "⚠️  Autostart entry already exists!"
    echo ""
    read -p "Do you want to reinstall? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
fi

# Create desktop autostart file
echo "📝 Creating desktop autostart entry..."
cat > "${DESKTOP_FILE}" << EOF
[Desktop Entry]
Type=Application
Name=Snooker Shot Clock
Comment=Professional Snooker Shot Clock with Timer and Announcements
Exec=${SCRIPT_DIR}/run.sh
Path=${SCRIPT_DIR}
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOF

echo "✅ Desktop file created: ${DESKTOP_FILE}"
echo ""

# Make run.sh executable
chmod +x "${SCRIPT_DIR}/run.sh"
echo "✅ run.sh is executable"
echo ""

echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "The Snooker Shot Clock will start automatically when you log in."
echo ""
echo "To test without rebooting:"
echo "  ${SCRIPT_DIR}/run.sh"
echo ""
echo "To disable autostart:"
echo "  rm ${DESKTOP_FILE}"
echo ""
echo "Or use the uninstall script:"
echo "  ./uninstall_autostart_desktop.sh"
echo ""
