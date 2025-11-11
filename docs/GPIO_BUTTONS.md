# GPIO Button Setup Guide

## Übersicht

Die Shot Clock unterstützt jetzt physische Buttons über GPIO:
- **Start Button** (GPIO 5) - Startet einen neuen Frame
- **Reset Button** (GPIO 6) - Setzt den Frame zurück
- **5 LEDs** (GPIO 17, 27, 22, 23, 24) - Countdown-Anzeige

## Hardware Setup

### Benötigte Komponenten

**Für LEDs:**
- 5x LEDs (beliebige Farbe, empfohlen: Grün/Gelb/Rot)
- 5x 220Ω Widerstände
- Jumper-Kabel
- Breadboard

**Für Buttons:**
- 2x Taster/Buttons (normalerweise offen)
- 2x Jumper-Kabel
- Optional: 2x 10kΩ Pull-up Widerstände (Software Pull-up wird verwendet)

### Schaltplan

```
┌─────────────────────────────────────────────────────────┐
│                    Raspberry Pi                         │
│                                                         │
│  GPIO 5  ────────┐                                      │
│                  │                                      │
│  GPIO 6  ────────┼───┐                                  │
│                  │   │                                  │
│  GPIO 17 ────────┼───┼───[220Ω]──┬─ LED 1 ─┬           │
│  GPIO 27 ────────┼───┼───[220Ω]──┼─ LED 2 ─┼           │
│  GPIO 22 ────────┼───┼───[220Ω]──┼─ LED 3 ─┼           │
│  GPIO 23 ────────┼───┼───[220Ω]──┼─ LED 4 ─┼           │
│  GPIO 24 ────────┼───┼───[220Ω]──┼─ LED 5 ─┼           │
│                  │   │            │         │           │
│  GND ────────────┴───┴────────────┴─────────┘           │
└─────────────────────────────────────────────────────────┘
         │       │
     [Button] [Button]
      Start   Reset
```

### Detaillierte Verkabelung

#### LEDs (Outputs)
Jede LED wird wie folgt angeschlossen:

```
Raspberry Pi GPIO Pin → 220Ω Widerstand → LED Anode (+) → LED Kathode (-) → GND
```

**Pin-Belegung:**
- GPIO 17 → LED 1 (5 Sekunden)
- GPIO 27 → LED 2 (4 Sekunden)
- GPIO 22 → LED 3 (3 Sekunden)
- GPIO 23 → LED 4 (2 Sekunden)
- GPIO 24 → LED 5 (1 Sekunde)

**LED Polarität:**
- Längeres Beinchen = Anode (+) → zum GPIO über Widerstand
- Kürzeres Beinchen = Kathode (-) → zu GND

#### Buttons (Inputs)

Jeder Button wird wie folgt angeschlossen:

```
Raspberry Pi GPIO Pin ──┬── Button ── GND
                        │
                   (Pull-up in Software)
```

**Pin-Belegung:**
- GPIO 5 → Start Button → GND
- GPIO 6 → Reset Button → GND

**Funktionsweise:**
- Button **nicht gedrückt**: GPIO Pin ist HIGH (3.3V durch internen Pull-up)
- Button **gedrückt**: GPIO Pin wird auf GND gezogen → LOW Signal

**Wichtig:**
- Keine externen Pull-up Widerstände nötig (Software Pull-up wird verwendet)
- Button verbindet GPIO Pin direkt mit GND
- Debouncing wird in Software gemacht (100ms)

## Konfiguration

### 1. GPIO aktivieren

Bearbeite `config.py`:

```python
# GPIO aktivieren
USE_GPIO = True

# LED Pins (Outputs)
LED_PINS = [17, 27, 22, 23, 24]

# Button Pins (Inputs)
BUTTON_START_PIN = 5   # Start Frame
BUTTON_RESET_PIN = 6   # Reset Frame

# UI LED-Anzeige (unabhängig von physischen LEDs)
SHOW_LED_INDICATORS = True  # Zeige LED-Kreise in der UI
```

### 2. Andere GPIO Pins verwenden

Falls du andere Pins verwenden möchtest:

```python
# Beispiel: Andere Pins
BUTTON_START_PIN = 16   # Statt GPIO 5
BUTTON_RESET_PIN = 20   # Statt GPIO 6

LED_PINS = [12, 13, 18, 19, 25]  # Statt 17,27,22,23,24
```

**Wichtig:** Verwende nur GPIO-Pins, keine anderen (Power, GND, etc.)!

**Sichere GPIO Pins für Raspberry Pi 4:**
- Alle Pins außer: 0, 1, 14, 15 (reserviert für I2C/UART)
- Empfohlen: 2-27 (außer 0, 1, 14, 15)

### 3. UI LED-Anzeige ein/ausblenden

Die 5 LED-Kreise in der UI sind unabhängig von den physischen LEDs:

```python
# LED-Kreise in der UI anzeigen
SHOW_LED_INDICATORS = True   # Standard

# LED-Kreise ausblenden (z.B. wenn physische LEDs vorhanden)
SHOW_LED_INDICATORS = False
```

## Installation

### 1. Abhängigkeiten installieren

```bash
# System-Pakete
sudo apt install python3-gpiozero

# Oder via pip
pip3 install gpiozero
```

### 2. GPIO-Berechtigungen

Stelle sicher, dass dein User zur GPIO-Gruppe gehört:

```bash
# User zur GPIO-Gruppe hinzufügen
sudo usermod -a -G gpio $USER

# Abmelden und wieder anmelden, dann prüfen:
groups
# Sollte "gpio" enthalten
```

### 3. Testen

**LEDs testen:**
```bash
python3 -c "from gpiozero import LED; import time; led = LED(17); led.on(); time.sleep(2); led.off()"
```

**Button testen:**
```bash
python3 -c "from gpiozero import Button; btn = Button(5); btn.wait_for_press(); print('Button pressed!')"
# Drücke den Button an GPIO 5
```

## Verwendung

Wenn GPIO aktiviert ist:

1. **Start Button drücken** → Startet einen neuen Frame
2. **Reset Button drücken** → Setzt den Frame zurück
3. **LEDs leuchten automatisch** basierend auf verbleibender Shot-Zeit
   - 5-4 Sekunden: Alle 5 LEDs (Grün)
   - 3 Sekunden: 3 LEDs (Orange)
   - 2-1 Sekunden: 2-1 LEDs (Rot)

**Debug-Output in der Konsole:**
```
GPIO: 5 LEDs initialized on pins [17, 27, 22, 23, 24]
GPIO: Input buttons initialized on pins 5 (Start), 6 (Reset)
GPIO: Start button pressed
GPIO: Reset button pressed
```

## Troubleshooting

### Buttons funktionieren nicht

**1. GPIO-Berechtigungen prüfen:**
```bash
groups | grep gpio
# Sollte "gpio" zeigen
```

**2. Pin-Verbindung testen:**
```bash
# Manueller Test
python3
>>> from gpiozero import Button
>>> btn = Button(5)
>>> btn.is_pressed
False  # Sollte False sein wenn nicht gedrückt
>>> # Jetzt Button drücken
>>> btn.is_pressed
True   # Sollte True sein wenn gedrückt
```

**3. Pull-up aktiviert?**
Der Code aktiviert automatisch Pull-up Widerstände:
```python
Button(pin, pull_up=True)
```

### LEDs leuchten nicht

**1. LED-Polarität prüfen:**
- Längeres Bein → zum GPIO (über Widerstand)
- Kürzeres Bein → zu GND

**2. LED manuell testen:**
```bash
python3 -c "from gpiozero import LED; led = LED(17); led.on(); input('Press enter'); led.off()"
```

**3. Widerstand prüfen:**
- 220Ω verwenden (Rot-Rot-Braun-Gold)
- Ohne Widerstand kann LED durchbrennen!

### LEDs bleiben an nach Beenden

```bash
# GPIO Pins manuell zurücksetzen
python3 -c "from gpiozero import LED; [LED(p).off() for p in [17,27,22,23,24]]"
```

Der Code sollte das automatisch beim Beenden machen (`cleanup()`).

### "Permission denied" Fehler

```bash
# GPIO-Gruppe fehlt
sudo usermod -a -G gpio $USER

# Danach: Logout und wieder Login
```

### Button reagiert mehrfach (Bouncing)

Der Code hat bereits Debouncing eingebaut:
```python
Button(pin, pull_up=True, bounce_time=0.1)  # 100ms Debounce
```

Falls Probleme bestehen, Bounce-Zeit erhöhen:
```python
# In gpio_control.py
bounce_time=0.2  # 200ms
```

## Erweiterte Konfiguration

### Andere Button-Aktionen hinzufügen

Du kannst weitere Buttons hinzufügen, z.B. für Shot-Reset:

**1. In `config.py`:**
```python
BUTTON_SHOT_RESET_PIN = 13  # Neuer Pin
```

**2. In `src/gpio_control.py`:**
```python
# In __init__
self.button_shot_reset = Button(config.BUTTON_SHOT_RESET_PIN, pull_up=True, bounce_time=0.1)
self.button_shot_reset.when_pressed = self._on_shot_reset_pressed

# Neue Methode
def _on_shot_reset_pressed(self):
    if self.timer_state:
        print("GPIO: Shot reset button pressed")
        self.timer_state.reset_shot()
```

### LED-Muster ändern

Du kannst eigene LED-Muster programmieren, z.B. Blinken bei kritischer Zeit:

```python
# In gpio_control.py, update() Methode
if leds_lit <= 2:
    # Blinken bei kritischer Zeit
    if int(time.time() * 2) % 2:  # 2Hz Blinken
        for i in range(leds_lit):
            self.leds[i].on()
    else:
        self.all_off()
```

## Pin-Referenz

### Raspberry Pi 4 GPIO Layout

```
3.3V  [1] [2]  5V
GPIO2 [3] [4]  5V
GPIO3 [5] [6]  GND
GPIO4 [7] [8]  GPIO14
GND   [9] [10] GPIO15
GPIO17[11][12] GPIO18
GPIO27[13][14] GND
GPIO22[15][16] GPIO23
3.3V  [17][18] GPIO24
GPIO10[19][20] GND
GPIO9 [21][22] GPIO25
GPIO11[23][24] GPIO8
GND   [25][26] GPIO7
GPIO0 [27][28] GPIO1
GPIO5 [29][30] GND
GPIO6 [31][32] GPIO12
GPIO13[33][34] GND
GPIO19[35][36] GPIO16
GPIO26[37][38] GPIO20
GND   [39][40] GPIO21
```

**In diesem Projekt verwendet:**
- Pin 29 (GPIO 5) - Start Button
- Pin 31 (GPIO 6) - Reset Button
- Pin 11 (GPIO 17) - LED 1
- Pin 13 (GPIO 27) - LED 2
- Pin 15 (GPIO 22) - LED 3
- Pin 16 (GPIO 23) - LED 4
- Pin 18 (GPIO 24) - LED 5
- Pin 6, 9, 14, 20, 25, 30, 34, 39 (GND) - Gemeinsame Masse

## Best Practices

1. **Immer Widerstände bei LEDs verwenden** (220Ω)
2. **Buttons mit Software Pull-ups** (kein externer Widerstand nötig)
3. **Debouncing aktiviert lassen** (100ms Standard)
4. **GPIO Cleanup** wird automatisch beim Beenden aufgerufen
5. **Richtige Pins verwenden** (keine Power/Ground Pins!)
6. **Kabel kurz halten** (weniger Störungen)
7. **Gemeinsame GND** für alle Komponenten

## Sicherheit

⚠️ **Wichtig:**
- Raspberry Pi GPIO Pins vertragen nur **3.3V**!
- Niemals 5V an GPIO Pins anlegen (Schaden am Pi!)
- LEDs immer mit Widerstand (220Ω minimum)
- Maximaler Strom pro Pin: 16mA
- Maximaler Gesamt-Strom alle Pins: 50mA

Bei 220Ω und 3.3V:
- Strom = 3.3V / 220Ω ≈ 15mA ✅ (sicher)

## Weitere Informationen

- **gpiozero Dokumentation:** https://gpiozero.readthedocs.io/
- **Raspberry Pi GPIO:** https://www.raspberrypi.com/documentation/computers/os.html#gpio
- **LED Rechner:** https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-led-series-resistor
