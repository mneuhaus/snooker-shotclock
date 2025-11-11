# Snooker Shot Clock - Dokumentation

Eine umfassende Anleitung für Entwickler mit HTML/JavaScript/CSS Hintergrund.

## 📚 Inhaltsverzeichnis

1. [Projektübersicht](#projektübersicht)
2. [Technologie-Stack](#technologie-stack)
3. [Projektstruktur](#projektstruktur)
4. [Wie funktioniert das?](#wie-funktioniert-das)
5. [Detaillierte Komponentenbeschreibung](#detaillierte-komponentenbeschreibung)
6. [Von HTML/JS zu Python/Pygame](#von-htmljs-zu-pythonpygame)
7. [Installation & Setup](#installation--setup)
8. [Anpassungen vornehmen](#anpassungen-vornehmen)
9. [Deployment auf Raspberry Pi](#deployment-auf-raspberry-pi)

---

## Projektübersicht

Die Snooker Shot Clock ist eine professionelle Timer-Anwendung für Snooker-Spiele, die:
- **Frame Timer** (10 Minuten Gesamtzeit) und **Shot Timer** (15s/10s) anzeigt
- Visuelles und akustisches Feedback gibt
- Mit verschiedenen Eingabegeräten funktioniert (Maus, Tastatur, Gamepad)
- Auf einem Raspberry Pi mit Touchscreen läuft

### Hauptfunktionen:
- ⏱️ Zwei separate Timer (Frame & Shot)
- 🔊 Sprachansagen bei wichtigen Events
- 💡 5 LED-Countdown Anzeige
- 🎮 Multiple Input-Methoden
- 🎯 "Balls Rolling" Pause-Funktion

---

## Technologie-Stack

### Warum Python + Pygame?

Wenn du von HTML/JavaScript kommst, fragst du dich vielleicht: "Warum nicht einfach eine Web-App?"

**Vergleich:**

| Feature | Web (HTML/JS) | Python + Pygame |
|---------|---------------|-----------------|
| Fullscreen ohne Browser | ❌ Schwierig | ✅ Einfach |
| GPIO (Hardware) | ❌ Nicht möglich | ✅ Direkt |
| Performance | ⚠️ OK | ✅ Sehr gut |
| Gamepad/Controller | ⚠️ Kompliziert | ✅ Einfach |
| Offline | ✅ Ja | ✅ Ja |
| Deployment | ⚠️ Browser nötig | ✅ Standalone |

**Für einen Raspberry Pi mit Hardware-Integration ist Python + Pygame ideal!**

### Die Technologien:

1. **Python 3.11+**
   - Wie JavaScript, aber: Typisierung, einfachere Syntax
   - Läuft direkt auf dem System (kein Browser nötig)

2. **Pygame**
   - Game-Framework für Python
   - Vergleichbar mit: Canvas API + Event Listeners in JavaScript
   - Kümmert sich um: Display, Input, Audio

3. **pygame.freetype**
   - Für schöne, skalierbare Schriften
   - Wie CSS `@font-face`, aber für Pygame

4. **pyttsx3**
   - Text-to-Speech Bibliothek
   - Wie Browser's `SpeechSynthesis API`

5. **RPi.GPIO / gpiozero** (optional)
   - Für Hardware-Steuerung (LEDs)
   - Gibt es nicht im Web!

---

## Projektstruktur

```
snooker-shotclock/
├── main.py                 # 🚀 Entry Point (wie index.html)
├── config.py               # ⚙️ Konfiguration (wie .env oder config.js)
├── requirements.txt        # 📦 Dependencies (wie package.json)
├── run.sh                  # 🏃 Start-Script
│
├── assets/                 # 🎨 Statische Dateien
│   ├── SFW-Logo.png
│   └── sounds/
│       └── zonk.mp3
│
├── src/                    # 📁 Source Code (wie /src in React)
│   ├── __init__.py         # Python package marker
│   ├── game_state.py       # 🎮 State Management (wie Redux/Zustand)
│   ├── ui.py               # 🎨 UI Rendering (wie React Components)
│   ├── input_handler.py    # 🖱️ Event Handling (wie addEventListener)
│   ├── audio.py            # 🔊 Audio System (wie Web Audio API)
│   └── gpio_control.py     # 💡 Hardware Control (LED)
│
├── docs/                   # 📚 Dokumentation
│   └── README.md           # Diese Datei
│
└── venv/                   # 🐍 Virtual Environment (wie node_modules)
```

---

## Wie funktioniert das?

### Der Ablauf (vereinfacht)

```
1. main.py startet
   ↓
2. Pygame initialisiert Display + Audio
   ↓
3. Komponenten werden erstellt:
   - TimerState (Game State)
   - UI (Rendering)
   - InputHandler (Events)
   - AudioSystem (Sounds + TTS)
   - GPIOControl (LEDs)
   ↓
4. GAME LOOP startet (60x pro Sekunde):
   │
   ├─→ Input verarbeiten (Maus, Tastatur, etc.)
   ├─→ State aktualisieren (Timer runterzählen)
   ├─→ Audio checken (Sounds abspielen?)
   ├─→ LEDs aktualisieren
   ├─→ UI neu zeichnen
   └─→ Zurück zu 4.
```

### Vergleich mit Web-Entwicklung:

**In JavaScript würdest du schreiben:**
```javascript
// Game Loop
function gameLoop() {
  handleInput();
  updateState();
  checkAudio();
  render();
  requestAnimationFrame(gameLoop);
}
```

**In Python mit Pygame:**
```python
# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    handle_input()
    update_state()
    check_audio()
    render()
    clock.tick(60)  # 60 FPS
```

**Fast identisch!**

---

## Detaillierte Komponentenbeschreibung

### 1. `main.py` - Der Entry Point

**Aufgabe:** Alles zusammenbringen und die Game Loop starten

**Vergleich:**
```html
<!-- In Web wäre das: -->
<html>
  <body>
    <div id="app"></div>
    <script src="app.js"></script>
  </body>
</html>
```

**In Python:**
```python
# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

# Komponenten erstellen
timer_state = TimerState()
ui = UI(screen)
input_handler = InputHandler(ui, timer_state)
audio_system = AudioSystem()

# Game Loop
while running:
    running = input_handler.handle_events()  # Events
    timer_state.update()                      # State
    audio_system.update(timer_state)          # Audio
    ui.draw(timer_state)                      # Render
    clock.tick(60)                            # 60 FPS
```

**Was passiert:**
1. Display wird erstellt (wie `document.body`)
2. Alle Komponenten werden instanziiert
3. Game Loop läuft mit 60 FPS

---

### 2. `config.py` - Die Konfiguration

**Aufgabe:** Zentrale Einstellungen

**Vergleich zu JavaScript:**
```javascript
// config.js
export const CONFIG = {
  SCREEN_WIDTH: 1920,
  SCREEN_HEIGHT: 1080,
  FRAME_DURATION: 10 * 60,
  SHOT_TIME_FIRST_HALF: 15
};
```

**In Python:**
```python
# config.py
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FRAME_DURATION = 10 * 60
SHOT_TIME_FIRST_HALF = 15
```

**Wichtig:** In Python gibt es keine `export` - einfach Variablen definieren!

**Verwendung:**
```python
import config
print(config.SCREEN_WIDTH)  # 1920
```

---

### 3. `game_state.py` - State Management

**Aufgabe:** Verwaltet den Zustand der Timer

**Vergleich zu React/Redux:**
```javascript
// In React mit useState:
const [frameTime, setFrameTime] = useState(600);
const [shotTime, setShotTime] = useState(15);
const [state, setState] = useState('idle');
```

**In Python (OOP):**
```python
class TimerState:
    def __init__(self):
        self.frame_time_remaining = 600
        self.shot_time_remaining = 15
        self.state = GameState.IDLE
    
    def update(self):
        # Timer runterzählen
        delta = time.time() - self.last_update
        self.frame_time_remaining -= delta
        self.shot_time_remaining -= delta
```

**Vorteile der OOP-Variante:**
- Alles zusammen in einer Klasse
- Methoden wie `start_frame()`, `reset_shot()` direkt dabei
- Kein Prop Drilling nötig

**Wichtige Methoden:**

| Methode | Beschreibung | Äquivalent in Web |
|---------|--------------|-------------------|
| `start_frame()` | Frame starten | `onClick={() => startGame()}` |
| `reset_shot()` | Shot zurücksetzen | `onClick={() => resetTimer()}` |
| `update()` | Timer aktualisieren | In `useEffect(() => {...}, [time])` |
| `get_frame_time_str()` | Format: "10:00" | `${Math.floor(time/60)}:${time%60}` |

---

### 4. `ui.py` - Das User Interface

**Aufgabe:** Alles auf den Bildschirm zeichnen

**Vergleich zu React:**
```jsx
// React Component
function ShotClock({ frameTime, shotTime }) {
  return (
    <div className="container">
      <button>Start Frame</button>
      <div className="timer-large">{frameTime}</div>
      <div className="timer-shot">{shotTime}</div>
    </div>
  );
}
```

**In Python mit Pygame:**
```python
class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.freetype.SysFont(None, 600)
        self.button_start = Button(30, 30, 220, 220, "Start\nFrame")
    
    def draw(self, timer_state):
        # Clear screen (wie Virtual DOM diff)
        self.screen.fill(COLOR_BACKGROUND)
        
        # Draw button
        self.button_start.draw(self.screen, self.font)
        
        # Draw frame timer
        frame_text = timer_state.get_frame_time_str()
        self.font.render_to(self.screen, (50, 500), frame_text, COLOR_TEXT)
        
        # Update display (wie ReactDOM.render)
        pygame.display.flip()
```

**Wichtige Unterschiede zu Web:**

| Web (HTML/CSS) | Pygame |
|----------------|--------|
| `<div>` | `pygame.Rect()` |
| `background-color` | `screen.fill(color)` |
| `font-size: 60px` | `SysFont(None, 60)` |
| `position: absolute` | Direkte x/y Koordinaten |
| CSS Flexbox | Manuelle Berechnung |

**Beispiel - Button zeichnen:**
```python
def draw_button(self, screen):
    # Hintergrund (wie background-color)
    pygame.draw.rect(screen, COLOR_BUTTON, self.rect, border_radius=20)
    
    # Border (wie border)
    pygame.draw.rect(screen, COLOR_WHITE, self.rect, 5, border_radius=20)
    
    # Text (wie innerHTML)
    text_rect = font.get_rect("Start Frame")
    text_rect.center = self.rect.center
    font.render_to(screen, text_rect, "Start Frame", COLOR_WHITE)
```

---

### 5. `input_handler.py` - Event Handling

**Aufgabe:** Maus, Tastatur, Gamepad Events verarbeiten

**Vergleich zu JavaScript:**
```javascript
// Event Listeners in Web
document.addEventListener('keydown', (e) => {
  if (e.key === ' ') startFrame();
  if (e.key === 'r') resetFrame();
});

document.addEventListener('click', (e) => {
  if (isButtonClicked(e.x, e.y)) {
    startFrame();
  }
});
```

**In Pygame:**
```python
def handle_events(self):
    for event in pygame.event.get():
        # Keyboard Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.timer_state.start_frame()
            elif event.key == pygame.K_r:
                self.timer_state.reset_frame()
        
        # Mouse Events
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.ui.button_start.is_clicked(pos):
                self.timer_state.start_frame()
```

**Event Types:**

| Pygame Event | Web Equivalent | Beschreibung |
|--------------|----------------|--------------|
| `KEYDOWN` | `keydown` | Taste gedrückt |
| `MOUSEBUTTONDOWN` | `click` | Maus geklickt |
| `MOUSEMOTION` | `mousemove` | Maus bewegt |
| `JOYBUTTONDOWN` | Gamepad API | Controller-Button |
| `QUIT` | `beforeunload` | Fenster schließen |

---

### 6. `audio.py` - Das Audio-System

**Aufgabe:** Sounds abspielen + Sprachausgabe

**Vergleich zu Web Audio API:**
```javascript
// Web Audio
const audio = new Audio('zonk.mp3');
audio.play();

// Text-to-Speech
const utterance = new SpeechSynthesisUtterance('15 seconds shot clock');
speechSynthesis.speak(utterance);
```

**In Pygame + pyttsx3:**
```python
# Sound laden
self.zonk_sound = pygame.mixer.Sound('assets/sounds/zonk.mp3')

# Sound abspielen
self.zonk_sound.play(maxtime=1000)  # 1 Sekunde

# Text-to-Speech
self.tts_engine = pyttsx3.init()
self.tts_engine.say("15 seconds shot clock now in operation")
self.tts_engine.runAndWait()
```

**Threading für TTS:**
```python
def announce(message):
    def speak():
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()
    
    # In separatem Thread (blockiert nicht die Game Loop)
    thread = threading.Thread(target=speak, daemon=True)
    thread.start()
```

**Warum Threading?**
- TTS dauert mehrere Sekunden
- Game Loop muss weiterlaufen (60 FPS)
- Wie `async/await` in JavaScript!

---

### 7. `gpio_control.py` - Hardware-Steuerung

**Aufgabe:** LEDs am Raspberry Pi steuern

**Das gibt es NICHT im Web!** Dies ist ein Hauptvorteil von Python auf Raspberry Pi.

**Wie funktioniert GPIO?**

```python
from gpiozero import LED

# LED-Objekte für GPIO-Pins erstellen
led1 = LED(17)  # GPIO Pin 17
led2 = LED(27)  # GPIO Pin 27

# LEDs ein/aus schalten
led1.on()   # LED an
led1.off()  # LED aus
led1.blink(on_time=0.5, off_time=0.5)  # Blinken
```

**In unserer Shot Clock:**
```python
def update(self, timer_state):
    shot_time = int(timer_state.shot_time_remaining)
    leds_lit = min(5, max(0, shot_time))
    
    # 5 LEDs ansteuern
    for i in range(5):
        if i < leds_lit:
            self.leds[i].on()   # LED an
        else:
            self.leds[i].off()  # LED aus
```

**Resultat:** Bei 5 Sekunden leuchten 5 LEDs, bei 4 Sekunden 4 LEDs, etc.

---

## Von HTML/JS zu Python/Pygame

### Konzept-Mapping

| HTML/CSS/JS Konzept | Pygame Äquivalent |
|---------------------|-------------------|
| `<div>` Element | `pygame.Rect()` |
| `document.querySelector()` | Direkter Zugriff auf Objekte |
| `addEventListener()` | `pygame.event.get()` Loop |
| `setInterval()` | Game Loop mit `clock.tick()` |
| `canvas.getContext('2d')` | `screen` Surface |
| CSS `position: absolute` | x/y Koordinaten |
| CSS `color: white` | `(255, 255, 255)` RGB Tuple |
| CSS `font-size: 60px` | `SysFont(None, 60)` |
| `requestAnimationFrame()` | `clock.tick(60)` |
| `audio.play()` | `sound.play()` |
| React State | Klassen-Attribute |
| React Props | Methoden-Parameter |

### Code-Beispiele im Vergleich

**Button mit Click-Handler:**

```javascript
// JavaScript + HTML
<button onclick="startFrame()" style="width: 220px">
  Start Frame
</button>

function startFrame() {
  frameRunning = true;
}
```

```python
# Python + Pygame
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Usage:
if button.is_clicked(mouse_pos):
    timer_state.start_frame()
```

**Timer mit Update:**

```javascript
// JavaScript
let timeLeft = 600;
setInterval(() => {
  timeLeft -= 1;
  document.getElementById('timer').textContent = timeLeft;
}, 1000);
```

```python
# Python
class TimerState:
    def __init__(self):
        self.time_left = 600
        self.last_update = time.time()
    
    def update(self):
        delta = time.time() - self.last_update
        self.time_left -= delta
        self.last_update = time.time()

# In Game Loop (60x pro Sekunde):
timer_state.update()
```

---

## Installation & Setup

### 1. Voraussetzungen

```bash
# Python 3.11 oder 3.12 (NICHT 3.14!)
python3.11 --version

# Git
git --version
```

### 2. Repository klonen

```bash
git clone https://github.com/mneuhaus/snooker-shotclock.git
cd snooker-shotclock
```

### 3. Virtual Environment erstellen

**Was ist das?**
- Wie `node_modules` in JavaScript
- Isolierte Python-Umgebung für das Projekt
- Verhindert Konflikte mit anderen Python-Projekten

```bash
# Erstellen
python3.11 -m venv venv

# Aktivieren (macOS/Linux)
source venv/bin/activate

# Aktivieren (Windows)
venv\Scripts\activate
```

### 4. Dependencies installieren

```bash
pip install -r requirements.txt
```

**Was wird installiert:**
- `pygame` - Game Framework
- `pyttsx3` - Text-to-Speech
- `numpy` - Für Audio-Generierung
- `RPi.GPIO` - Nur auf Raspberry Pi
- `gpiozero` - Nur auf Raspberry Pi

### 5. Starten

```bash
# Mit Script
./run.sh

# Oder direkt
python3 main.py
```

---

## Anpassungen vornehmen

### Farben ändern

**Datei:** `config.py`

```python
# Farbwerte als RGB Tuples (0-255)
COLOR_BACKGROUND = (55, 75, 80)     # Hintergrund
COLOR_TEXT = (255, 255, 255)        # Text (weiß)
COLOR_WARNING = (255, 100, 0)       # Orange
COLOR_CRITICAL = (255, 0, 0)        # Rot
```

**Tipp:** Nutze einen Color Picker für RGB-Werte!

### Timer-Zeiten ändern

**Datei:** `config.py`

```python
FRAME_DURATION = 10 * 60        # 10 Minuten (in Sekunden)
FIRST_HALF_DURATION = 5 * 60    # Nach 5 Min wechseln
SHOT_TIME_FIRST_HALF = 15       # 15 Sekunden (erste Hälfte)
SHOT_TIME_SECOND_HALF = 10      # 10 Sekunden (zweite Hälfte)
```

### Schriftgrößen ändern

**Datei:** `src/ui.py`

```python
# In __init__() Methode:
self.font_frame_timer = pygame.freetype.SysFont(None, 380)  # Frame Timer
self.font_shot_timer = pygame.freetype.SysFont(None, 700)   # Shot Timer
self.font_button = pygame.freetype.SysFont(None, 70)        # Buttons
```

**Größere Zahl = größere Schrift!**

### Logo austauschen

1. Neues Logo als PNG speichern
2. Ersetzen: `assets/SFW-Logo.png`
3. Optional Größe anpassen in `src/ui.py`:

```python
self.logo_size = 280  # Pixel
```

### Stimme ändern

**Datei:** `src/audio.py`

```python
# In __init__() Methode, suche nach:
if 'moira' in voice.name.lower():

# Ersetze 'moira' durch andere Stimme:
if 'samantha' in voice.name.lower():  # US
if 'karen' in voice.name.lower():     # Australisch
if 'tessa' in voice.name.lower():     # Südafrikanisch
```

### Sprachgeschwindigkeit ändern

**Datei:** `src/audio.py`

```python
self.tts_engine.setProperty('rate', 172)  # Wörter pro Minute
# Niedriger = langsamer
# Höher = schneller
# Standard: 150
```

### GPIO Pins ändern

**Datei:** `config.py`

```python
USE_GPIO = True  # Auf Raspberry Pi auf True setzen!

LED_PINS = [17, 27, 22, 23, 24]  # GPIO Pin-Nummern
#           LED1 LED2 LED3 LED4 LED5
```

---

## Deployment auf Raspberry Pi

### 1. Raspberry Pi Setup

```bash
# System updaten
sudo apt-get update
sudo apt-get upgrade

# Python 3.11 installieren (falls nicht vorhanden)
sudo apt-get install python3.11 python3.11-venv

# Git installieren
sudo apt-get install git
```

### 2. Projekt auf Pi kopieren

```bash
# Via Git
git clone https://github.com/mneuhaus/snooker-shotclock.git
cd snooker-shotclock

# Virtual Environment + Dependencies
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. GPIO aktivieren

**Datei:** `config.py`

```python
USE_GPIO = True
```

### 4. Autostart einrichten

**Datei erstellen:** `/home/pi/.config/autostart/shotclock.desktop`

```ini
[Desktop Entry]
Type=Application
Name=Snooker Shot Clock
Exec=/home/pi/snooker-shotclock/run.sh
```

### 5. Fullscreen + Touchscreen

**Für optimale Performance:**

```bash
# In config.py:
FULLSCREEN = True

# Maus-Cursor verstecken (optional):
# In main.py nach pygame.init():
pygame.mouse.set_visible(False)
```

### 6. LEDs anschließen

**Hardware Setup:**

```
GPIO Pin → 220Ω Widerstand → LED Anode (+)
LED Kathode (-) → GND
```

**Pin-Belegung (Standard):**
- GPIO 17 → LED 1 (5 Sekunden)
- GPIO 27 → LED 2 (4 Sekunden)
- GPIO 22 → LED 3 (3 Sekunden)
- GPIO 23 → LED 4 (2 Sekunden)
- GPIO 24 → LED 5 (1 Sekunde)

### 7. Testen

```bash
./run.sh
```

---

## Troubleshooting

### "pygame not found"
```bash
# Virtual Environment aktiviert?
source venv/bin/activate

# Neu installieren
pip install pygame
```

### "TTS voice not working"
```bash
# Auf Raspberry Pi:
sudo apt-get install espeak

# Auf macOS: Sollte funktionieren
# Auf Windows: Sollte funktionieren
```

### "GPIO not available"
```bash
# Nur auf Raspberry Pi nötig:
pip install RPi.GPIO gpiozero
```

### "Font rendering error"
```bash
# Pygame neu kompilieren:
pip uninstall pygame
pip install pygame --no-cache-dir
```

### Python 3.14 Probleme
```bash
# WICHTIG: Python 3.14 hat Pygame-Bugs!
# Nutze Python 3.11 oder 3.12
python3.11 -m venv venv
```

---

## Weitere Ressourcen

### Pygame lernen:
- [Pygame Docs](https://www.pygame.org/docs/)
- [Pygame Tutorial](https://realpython.com/pygame-a-primer/)

### Python lernen (für JS-Entwickler):
- [Python for JavaScript Developers](https://www.pythonforjs.com/)
- [Python in Y Minutes](https://learnxinyminutes.com/docs/python/)

### Raspberry Pi + Python:
- [Raspberry Pi GPIO Guide](https://gpiozero.readthedocs.io/)
- [Raspberry Pi Projects](https://projects.raspberrypi.org/)

---

## Support & Kontakt

- **GitHub Issues:** [github.com/mneuhaus/snooker-shotclock/issues](https://github.com/mneuhaus/snooker-shotclock/issues)
- **Repository:** [github.com/mneuhaus/snooker-shotclock](https://github.com/mneuhaus/snooker-shotclock)

---

## Lizenz

MIT License - Frei verwendbar für private und kommerzielle Projekte.
