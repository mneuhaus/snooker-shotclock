# Raspberry Pi Quick Start Guide

## 🚀 Fresh Installation (First Time)

Run these commands on your Raspberry Pi:

```bash
# 1. Clone the repository
git clone https://github.com/mneuhaus/snooker-shotclock.git
cd snooker-shotclock

# 2. Run the automated installer
./install_rpi.sh

# 3. Run the application
python3 main.py
```

That's it! The installer handles everything automatically.

---

## 🔧 If You Get the SDL2_ttf Error

```
ImportError: libSDL2_ttf-2.0.so.0: cannot open shared object file
```

**Quick Fix:**
```bash
sudo apt install -y libsdl2-ttf-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0
pip3 install pygame --no-cache-dir
```

**Alternative - Use System Pygame:**
```bash
pip3 uninstall pygame
sudo apt install python3-pygame
pip3 install pyttsx3
```

---

## 🎮 Quick Commands

| Task | Command |
|------|---------|
| Run app | `python3 main.py` |
| Update code | `git pull` |
| Test resolution | `python3 test_resolution.py` |
| Test LED | `python3 -c "from gpiozero import LED; led = LED(17); led.on(); input('Press enter'); led.off()"` |
| Test TTS | `espeak "Testing"` |
| Check logs | `journalctl -u shotclock -f` (if using systemd) |

---

## ⚙️ Configuration Files to Edit

### Enable GPIO & Fullscreen
Edit `config.py`:
```python
FULLSCREEN = True   # Full screen on boot
USE_GPIO = True     # Enable LEDs
```

### Change LED Pins
Edit `config.py`:
```python
LED_PINS = [17, 27, 22, 23, 24]  # Change these numbers
```

---

## 🔌 GPIO Wiring (Default Pins)

```
LED 1 (5s) → GPIO 17 → [220Ω] → LED → GND
LED 2 (4s) → GPIO 27 → [220Ω] → LED → GND
LED 3 (3s) → GPIO 22 → [220Ω] → LED → GND
LED 4 (2s) → GPIO 23 → [220Ω] → LED → GND
LED 5 (1s) → GPIO 24 → [220Ω] → LED → GND
```

**Legend:**
- `GPIO XX` = Connect to this GPIO pin number
- `[220Ω]` = Use a 220 Ohm resistor
- `LED` = LED component (anode to resistor, cathode to GND)
- `GND` = Any ground pin on Raspberry Pi

---

## 🏁 Auto-Start on Boot

### Automated Installation (Recommended)

```bash
# Install autostart service
sudo ./install_autostart.sh

# Uninstall autostart service
sudo ./uninstall_autostart.sh
```

The install script will:
- Create a systemd service
- Enable autostart on boot
- Configure correct user and display
- Add automatic restart on failure

**Useful commands after installation:**
```bash
sudo systemctl start snooker-shotclock      # Start now
sudo systemctl stop snooker-shotclock       # Stop service
sudo systemctl restart snooker-shotclock    # Restart service
sudo systemctl status snooker-shotclock     # Check status
sudo journalctl -u snooker-shotclock -f     # View logs (live)
```

### Manual Method: Desktop Autostart (Alternative)
```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/shotclock.desktop
```

Add this content:
```ini
[Desktop Entry]
Type=Application
Name=Snooker Shot Clock
Exec=/home/pi/snooker-shotclock/run.sh
```

---

## 🐛 Troubleshooting Quick Fixes

### UI looks too small/large or misaligned

The UI is now responsive and scales automatically. To check your resolution:

```bash
python3 test_resolution.py
```

This shows:
- Your actual screen resolution
- Scale factor being used
- Calculated font and button sizes

The UI is designed for 1920x1080 and scales proportionally. Common Raspberry Pi resolutions:
- 1920x1080 (Full HD) - Scale 1.0
- 1280x720 (HD) - Scale 0.67
- 1024x768 (Old monitors) - Scale 0.53

If layout still looks wrong, check `config.py`:
```python
SCREEN_WIDTH = 1920  # Should match your actual resolution
SCREEN_HEIGHT = 1080
```

### Screen is blank
```bash
# Check DISPLAY variable
echo $DISPLAY  # Should show :0 or :0.0

# Try running with explicit display
DISPLAY=:0 python3 main.py
```

### No sound
```bash
# Test audio output
speaker-test -t wav -c 2

# Set audio to 3.5mm jack
sudo raspi-config
# Navigate to: System Options → Audio → Force 3.5mm jack
```

### LEDs not working
```bash
# Test GPIO access
groups  # Should include 'gpio'

# Add user to gpio group if missing
sudo usermod -a -G gpio $USER

# Logout and login again
```

### Application crashes on start
```bash
# Check Python version (should be 3.9+)
python3 --version

# Check pygame version
python3 -c "import pygame; print(pygame.version.ver)"

# Reinstall everything
./install_rpi.sh
```

### "Permission denied" when running install_rpi.sh
```bash
chmod +x install_rpi.sh
./install_rpi.sh
```

---

## 📚 Full Documentation

- **Complete Setup Guide**: `docs/RASPBERRY_PI_SETUP.md`
- **Developer Guide**: `docs/README.md`
- **Main README**: `README.md`

---

## 🎯 Performance Tips

1. **Disable unnecessary services:**
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable cups
   ```

2. **Increase GPU memory:**
   ```bash
   sudo raspi-config
   # Performance Options → GPU Memory → Set to 256
   ```

3. **Overclock (optional):**
   ```bash
   sudo raspi-config
   # Performance Options → Overclock
   ```

---

## 🆘 Need More Help?

- **Check docs**: Look in `docs/RASPBERRY_PI_SETUP.md`
- **GitHub Issues**: https://github.com/mneuhaus/snooker-shotclock/issues
- **Test individual components**: See troubleshooting section above

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Application starts without errors
- [ ] Timers display correctly
- [ ] Buttons respond to clicks
- [ ] TTS voice works (announces "15 seconds shot clock")
- [ ] ZONK sound plays when timer expires
- [ ] LEDs light up during countdown (if using GPIO)
- [ ] Middle mouse button pauses shot timer

If all items are checked, you're ready to use the shot clock!
