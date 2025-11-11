"""Configuration for Snooker Shot Clock"""

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FULLSCREEN = True  # Fullscreen mode for Raspberry Pi
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

# GPIO settings (Raspberry Pi)
USE_GPIO = True  # GPIO enabled for Raspberry Pi (LEDs and Buttons)

# LED Output Pins (5 LEDs für Countdown-Anzeige)
LED_PINS = [17, 27, 22, 23, 24]  # GPIO Pins für 5 LEDs

# Button Input Pins (physische Buttons)
BUTTON_START_PIN = 5   # GPIO Pin für Start Frame Button
BUTTON_RESET_PIN = 6   # GPIO Pin für Reset Frame Button

# UI settings
SHOW_LED_INDICATORS = False  # LED circles in UI disabled (use physical LEDs)

# Audio settings
SOUND_ENABLED = True  # Sound effects enabled
SOUND_VOLUME = 0.7   # Volume level (0.0 - 1.0)
TTS_ENABLED = True   # Text-to-Speech announcements (espeak on Raspberry Pi)
TTS_VOICE = 'en-gb+f3'  # espeak voice: en-gb (male), en-gb+f3 (female), en-us+f3 (female US)
TTS_SPEED = 175      # Speech rate in words per minute (150-200 recommended)
