"""Development Configuration for Desktop/Mac
Copy this to config.py for development on non-Raspberry Pi systems
"""

# Display settings (Windowed for development)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FULLSCREEN = False  # Windowed mode for development
FPS = 60

# Colors
COLOR_BACKGROUND = (55, 75, 80)  # Dunkelgrau-Blau wie im Screenshot
COLOR_TEXT = (255, 255, 255)     # Weiß
COLOR_BUTTON = (55, 75, 80)
COLOR_BUTTON_BORDER = (255, 255, 255)
COLOR_BUTTON_HOVER = (75, 95, 100)
COLOR_WARNING = (255, 100, 0)    # Orange für Warnungen
COLOR_CRITICAL = (255, 0, 0)     # Rot für kritische Zeit

# Timer settings (in seconds)
FRAME_DURATION = 10 * 60  # 10 Minuten
FIRST_HALF_DURATION = 5 * 60  # Erste 5 Minuten
SHOT_TIME_FIRST_HALF = 15  # 15 Sekunden in erster Hälfte
SHOT_TIME_SECOND_HALF = 10  # 10 Sekunden in zweiter Hälfte

# Warning thresholds
SHOT_WARNING_TIME = 5  # Warnung bei 5 Sekunden
SHOT_CRITICAL_TIME = 3  # Kritisch bei 3 Sekunden

# GPIO settings (Disabled for development)
USE_GPIO = False  # No GPIO on desktop

# LED Output Pins (not used on desktop)
LED_PINS = [17, 27, 22, 23, 24]

# Button Input Pins (not used on desktop)
BUTTON_START_PIN = 5
BUTTON_RESET_PIN = 6

# UI settings
SHOW_LED_INDICATORS = True  # Show LED circles in UI for testing

# Audio settings
SOUND_ENABLED = True  # Sound effects enabled
SOUND_VOLUME = 0.7   # Volume level (0.0 - 1.0)
TTS_ENABLED = True   # Text-to-Speech (uses macOS voices on Mac)
TTS_VOICE = 'en-gb+f3'  # espeak voice (not used on macOS)
TTS_SPEED = 175      # Speech rate in WPM (not used on macOS)
