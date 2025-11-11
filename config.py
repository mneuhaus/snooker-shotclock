"""Configuration for Snooker Shot Clock"""

# Display settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FULLSCREEN = False  # Set to True for production/Raspberry Pi
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
FIRST_HALF_DURATION = 20  # Erste 5 Minuten
SHOT_TIME_FIRST_HALF = 15  # 15 Sekunden in erster Hälfte
SHOT_TIME_SECOND_HALF = 10  # 10 Sekunden in zweiter Hälfte

# Warning thresholds
SHOT_WARNING_TIME = 5  # Warnung bei 5 Sekunden
SHOT_CRITICAL_TIME = 3  # Kritisch bei 3 Sekunden

# GPIO settings (für Raspberry Pi)
USE_GPIO = False  # Auf True setzen für Raspberry Pi
# 5 LED Buttons für Countdown-Anzeige (5 Sekunden)
LED_PINS = [17, 27, 22, 23, 24]  # GPIO Pins für 5 LEDs

# Audio settings
SOUND_ENABLED = True
SOUND_VOLUME = 0.7
