# Raspberry Pi Setup Guide

## Installation

1. **Update System**
```bash
sudo apt update
sudo apt upgrade
```

2. **Install System Dependencies**
```bash
# Install required system libraries
sudo apt install -y \
    python3-pip \
    python3-gpiozero \
    espeak \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-numpy
```

3. **Clone Repository**
```bash
git clone https://github.com/mneuhaus/snooker-shotclock.git
cd snooker-shotclock
```

4. **Install Python Packages**
```bash
# Install pygame and other dependencies
pip3 install -r requirements.txt

# If pygame fails, try installing from system package:
# sudo apt install python3-pygame
# pip3 install pyttsx3
```

## Configuration

1. **Enable GPIO and Audio**
Edit `config.py`:
```python
FULLSCREEN = True  # Full screen mode
USE_GPIO = True    # Enable GPIO for LEDs
```

2. **Test GPIO**
```bash
# Test individual LED
python3 -c "from gpiozero import LED; led = LED(17); led.on(); import time; time.sleep(2); led.off()"
```

## Running the Application

### Standard Mode
```bash
python3 main.py
```

### Auto-start on Boot
Create systemd service:
```bash
sudo nano /etc/systemd/system/shotclock.service
```

Add:
```ini
[Unit]
Description=Snooker Shot Clock
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/snooker-shotclock
Environment="DISPLAY=:0"
ExecStart=/usr/bin/python3 /home/pi/snooker-shotclock/main.py
Restart=always

[Install]
WantedBy=graphical.target
```

Enable service:
```bash
sudo systemctl enable shotclock.service
sudo systemctl start shotclock.service
```

## Troubleshooting

### SDL2_ttf Error: "libSDL2_ttf-2.0.so.0: cannot open shared object file"

This error means the SDL2 TTF library is missing. This is the **most common error** on fresh Raspberry Pi installations.

**Solution: Install SDL2 libraries**
```bash
sudo apt install -y libsdl2-ttf-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0
```

If that doesn't work, install the full development packages:
```bash
sudo apt install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev
```

Then reinstall pygame:
```bash
pip3 uninstall pygame
pip3 install pygame --no-cache-dir
```

**Alternative: Use system pygame package**
```bash
pip3 uninstall pygame
sudo apt install python3-pygame
pip3 install pyttsx3  # Still need this for TTS
```

### NEON Warning: "system is neon capable but pygame not compiled"

This warning appears because pygame wasn't compiled with ARM NEON optimizations. The app should still work, but may be slightly slower.

**Option 1: Ignore (Recommended)**
The warning is harmless if the app runs smoothly. Just monitor performance.

**Option 2: Use System Pygame**
```bash
pip3 uninstall pygame
sudo apt install python3-pygame
```

**Option 3: Compile from Source**
```bash
pip3 uninstall pygame
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev
pip3 install pygame --no-binary :all:
```

### Audio Not Working

1. **Check ALSA Output**
```bash
speaker-test -t wav -c 2
```

2. **Set Audio Output**
```bash
# For 3.5mm jack
sudo raspi-config
# Navigate to: Advanced Options > Audio > Force 3.5mm jack
```

3. **Test TTS**
```bash
espeak "Testing text to speech"
```

### LEDs Not Working

1. **Check GPIO Pins**
Default pins: 17, 27, 22, 23, 24

2. **Verify Wiring**
- LED anode (+) → GPIO pin (via 220Ω resistor)
- LED cathode (-) → Ground

3. **Test Individual Pin**
```bash
python3 -c "from gpiozero import LED; led = LED(17); led.on(); input('Press enter'); led.off()"
```

## Hardware Setup

### Required Components
- Raspberry Pi 4 (2GB+ RAM recommended)
- MicroSD card (16GB+)
- HDMI display (1920x1080)
- USB Mouse
- 5x LEDs (any color)
- 5x 220Ω resistors
- Breadboard + jumper wires
- Speaker/Headphones

### GPIO Wiring
```
GPIO 17 ──[220Ω]──>|── GND  (LED 1)
GPIO 27 ──[220Ω]──>|── GND  (LED 2)
GPIO 22 ──[220Ω]──>|── GND  (LED 3)
GPIO 23 ──[220Ω]──>|── GND  (LED 4)
GPIO 24 ──[220Ω]──>|── GND  (LED 5)
```

## Performance Tips

1. **Disable Desktop Environment (Optional)**
For maximum performance:
```bash
sudo raspi-config
# System Options > Boot / Auto Login > Console Autologin
```

Then run with:
```bash
xinit python3 /home/pi/snooker-shotclock/main.py
```

2. **Overclock (Optional)**
```bash
sudo raspi-config
# Performance Options > Overclock
```

3. **Close Background Apps**
Stop unnecessary services to free resources.
