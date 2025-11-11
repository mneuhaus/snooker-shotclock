# Snooker Shot Clock

Eine pygame-basierte Shot Clock für Snooker-Frames mit LED-Anzeigen und Bluetooth-Controller-Unterstützung.

## Features

- **Frame Timer**: 10 Minuten Gesamtzeit pro Frame
- **Shot Timer**: 
  - Erste 5 Minuten: 15 Sekunden pro Stoß
  - Letzte 5 Minuten: 10 Sekunden pro Stoß
- **Multiple Input-Methoden**:
  - Maus (klickbare Buttons und Timer)
  - Tastatur (Shortcuts)
  - Bluetooth/USB Game Controller
- **Audio-Warnungen**: 
  - Tick-Sound jede Sekunde ab 5 Sekunden
  - "ZONK" Sound bei Timer-Ablauf
- **GPIO LED-Steuerung** (Raspberry Pi):
  - Grün: Normale Zeit
  - Gelb: Warnung (< 5s)
  - Rot: Kritisch (< 3s)

## Installation

### Raspberry Pi (Recommended)

**Quick Install:**
```bash
git clone https://github.com/mneuhaus/snooker-shotclock.git
cd snooker-shotclock
./install_rpi.sh
```

The script will automatically:
- Install all SDL2 libraries (fixes pygame issues)
- Install Python dependencies
- Configure GPIO and fullscreen mode
- Setup everything for Raspberry Pi

**Manual Install:**
See [docs/RASPBERRY_PI_SETUP.md](docs/RASPBERRY_PI_SETUP.md) for detailed instructions.

### Desktop (Development)

```bash
# Virtual Environment erstellen (empfohlen: Python 3.11 oder 3.12)
python3.11 -m venv venv  # oder python3.12
source venv/bin/activate  # Auf Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

**Hinweis**: Python 3.14 hat derzeit Kompatibilitätsprobleme mit pygame 2.6.1. Bitte Python 3.11 oder 3.12 verwenden.

### Common Issues

**SDL2_ttf Error on Raspberry Pi:**
```bash
sudo apt install -y libsdl2-ttf-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0
pip3 install pygame --no-cache-dir
```

See [docs/RASPBERRY_PI_SETUP.md](docs/RASPBERRY_PI_SETUP.md) for more troubleshooting.

## Konfiguration

Passe `config.py` an:

- `FULLSCREEN`: True/False für Vollbildmodus
- `USE_GPIO`: True für Raspberry Pi LED-Steuerung
- `LED_PINS`: GPIO-Pin-Nummern anpassen
- Timer-Einstellungen nach Bedarf anpassen

## Verwendung

```bash
python main.py
```

### Steuerung

**Maus:**
- Linksklick auf "Start Frame" - Frame starten
- Linksklick auf "Reset Frame" - Frame zurücksetzen
- Linksklick auf Frame-Timer (links unten) - Pause/Resume
- Linksklick auf Shot-Timer (rechts) - Shot zurücksetzen
- **Mittlere Maustaste halten** - Shot-Timer zurücksetzen und pausieren während Kugeln rollen
  - Frame-Timer läuft weiter
  - Shot-Timer startet neu beim Loslassen

**Tastatur:**
- `SPACE` - Frame starten
- `R` - Frame zurücksetzen
- `P` - Frame pausieren/fortsetzen
- `S` - Shot zurücksetzen
- `ESC` oder `Q` - Beenden

**Bluetooth Controller:**
- Button A/X - Frame starten
- Button B/Circle - Shot zurücksetzen
- Button X/Square - Frame pausieren
- Button Y/Triangle - Frame zurücksetzen

## GPIO Setup (Raspberry Pi)

LED-Anschlüsse:
- GPIO 17 - Grüne LED
- GPIO 27 - Gelbe LED
- GPIO 22 - Rote LED

Jeweils mit 220Ω Widerstand in Serie zu GND.

## Entwicklung

Projektstruktur:
```
snooker-shotclock/
├── main.py              # Entry Point
├── config.py            # Konfiguration
├── requirements.txt     # Python-Abhängigkeiten
└── src/
    ├── game_state.py    # Timer-Logik
    ├── ui.py            # UI-Rendering
    ├── input_handler.py # Input-Events
    ├── audio.py         # Sound-System
    └── gpio_control.py  # LED-Steuerung
```
