#!/bin/bash
# Raspberry Pi Installation Script for Snooker Shot Clock
# This script installs all dependencies and sets up the application

set -e  # Exit on error

echo "======================================"
echo "Snooker Shot Clock - Raspberry Pi Setup"
echo "======================================"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install SDL2 and system dependencies
echo "📦 Installing SDL2 libraries..."
sudo apt install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsdl2-ttf-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev

# Install Python dependencies
echo "📦 Installing Python packages..."
sudo apt install -y \
    python3-pip \
    python3-gpiozero \
    python3-numpy \
    espeak

# Install pygame and Python packages
echo "📦 Installing pygame and application dependencies..."
pip3 install --upgrade pip

# Try to install from requirements.txt
if pip3 install -r requirements.txt; then
    echo "✅ Python packages installed successfully"
else
    echo "⚠️  pip install failed, trying system pygame..."
    sudo apt install -y python3-pygame
    pip3 install pyttsx3
fi

# Enable GPIO and fullscreen
echo "⚙️  Configuring for Raspberry Pi..."
sed -i 's/FULLSCREEN = False/FULLSCREEN = True/' config.py
sed -i 's/USE_GPIO = False/USE_GPIO = True/' config.py

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Or use the run script:"
echo "  ./run.sh"
echo ""
echo "To setup autostart, see docs/RASPBERRY_PI_SETUP.md"
echo ""
