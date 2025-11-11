# Responsive Design in Pygame

## Problem

Die ursprüngliche Implementierung verwendete hardcodierte Pixel-Werte basierend auf 1920x1080:
- Schriftgrößen: 380px, 700px, 70px
- Button-Größe: 220x220 Pixel
- Abstände: 30px, 40px fest

**Resultat:** Auf kleineren/größeren Bildschirmen sieht das Layout schlecht aus.

## Lösung: Responsive Skalierung

### 1. Scale Factor berechnen

```python
self.scale = min(self.width / 1920, self.height / 1080)
```

Dieser Faktor sagt uns, wie viel kleiner/größer der aktuelle Bildschirm im Vergleich zu 1920x1080 ist.

**Beispiele:**
- 1920x1080 → scale = 1.0 (Referenzgröße)
- 1280x720 → scale = 0.667 (66.7% der Referenz)
- 3840x2160 (4K) → scale = 2.0 (doppelt so groß)

### 2. Alle Größen mit Scale multiplizieren

#### Schriftgrößen
```python
# Alt (hardcoded):
self.font_frame_timer = pygame.freetype.SysFont(None, 380)

# Neu (responsive):
self.font_frame_timer = pygame.freetype.SysFont(None, int(380 * self.scale))
```

Bei 1280x720:
- 380 * 0.667 = 253px (automatisch kleiner!)

#### Button-Größen
```python
# Alt (hardcoded):
button_width = 220
button_height = 220

# Neu (responsive - Prozent der Bildschirmgröße):
button_width = int(self.width * 0.11)    # 11% der Bildschirmbreite
button_height = int(self.height * 0.20)  # 20% der Bildschirmhöhe
```

Bei 1920x1080:
- Breite: 1920 * 0.11 = 211px
- Höhe: 1080 * 0.20 = 216px

Bei 1280x720:
- Breite: 1280 * 0.11 = 140px
- Höhe: 720 * 0.20 = 144px

#### Abstände und Margins
```python
# Alt (hardcoded):
button_margin = 30
spacing = 40

# Neu (responsive - Prozent):
button_margin = int(self.width * 0.015)  # 1.5% der Breite
spacing = int(self.width * 0.02)         # 2% der Breite
```

### 3. Prozentuale Positionierung

Statt absoluter Pixel-Positionen verwenden wir Prozente:

```python
# Frame Timer bei 25% von links (Mitte des linken Bereichs)
frame_x = int(self.width * 0.25)

# Shot Timer bei 80% von links (Mitte des rechten Bereichs)
shot_x = int(self.width * 0.80)

# Boundary bei 60% (teilt Bildschirm 60/40)
boundary = int(self.width * 0.60)
```

## Vergleich: Vorher vs. Nachher

### Vorher (Hardcoded)
```python
# 1920x1080
font_size = 380               # → 380px
button_width = 220            # → 220px
margin = 30                   # → 30px

# 1280x720 (PROBLEM!)
font_size = 380               # → 380px (viel zu groß!)
button_width = 220            # → 220px (viel zu groß!)
margin = 30                   # → 30px (sieht komisch aus)
```

### Nachher (Responsive)
```python
# 1920x1080 (Referenz)
scale = 1.0
font_size = int(380 * 1.0)    # → 380px
button_width = int(1920 * 0.11)  # → 211px
margin = int(1920 * 0.015)    # → 29px

# 1280x720 (Passt sich an!)
scale = 0.667
font_size = int(380 * 0.667)  # → 253px (passend!)
button_width = int(1280 * 0.11)  # → 140px (passend!)
margin = int(1280 * 0.015)    # → 19px (passend!)
```

## Responsive Elemente

### Buttons
```python
class Button:
    def __init__(self, x, y, width, height, text, scale=1.0):
        self.scale = scale
        self.border_radius = int(20 * scale)  # Responsive border
        self.border_width = max(3, int(5 * scale))  # Min. 3px
```

### LEDs
```python
def draw_led_indicators(self, timer_state):
    led_size = int(30 * self.scale)      # Responsive LED-Größe
    led_spacing = int(10 * self.scale)   # Responsive Abstand
    start_x = int(self.width - (450 * self.scale))
```

### Text-Abstand in Buttons
```python
# Dynamischer Zeilenabstand basierend auf Schriftgröße
text_rect_sample = font.get_rect(lines[0] if lines else "A")
line_height = int(text_rect_sample.height * 1.4)  # 40% Padding
```

## Vorteile

1. **Automatische Anpassung**: Funktioniert auf jedem Bildschirm
2. **Proportionen bleiben gleich**: Verhältnisse sind immer korrekt
3. **Kein manuelles Anpassen**: Einmal definiert, funktioniert überall
4. **Bessere Lesbarkeit**: Text passt sich Bildschirmgröße an

## Debugging

Die UI-Klasse gibt jetzt Debug-Informationen aus:

```python
print(f"Screen: {self.width}x{self.height}, Scale factor: {self.scale:.2f}")
print(f"Font sizes - Frame: {int(380 * self.scale)}, Shot: {int(700 * self.scale)}")
print(f"Button size: {button_width}x{button_height}")
```

Beispiel-Output auf Raspberry Pi (1280x720):
```
Screen: 1280x720, Scale factor: 0.67
Font sizes - Frame: 254, Shot: 467, Button: 47
Button size: 140x144, margin: 19, spacing: 25
```

## Testen mit verschiedenen Auflösungen

In `config.py` kannst du verschiedene Auflösungen testen:

```python
# Testen mit verschiedenen Größen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False
```

Probiere:
- 1920x1080 (Full HD - Referenz)
- 1280x720 (HD - Raspberry Pi typisch)
- 1366x768 (Laptop)
- 800x480 (Kleine Displays)
- 3840x2160 (4K)

Alles sollte proportional gut aussehen!

## Best Practices

1. **Verwende immer `self.scale` für fixe Pixel-Werte**
   ```python
   size = int(100 * self.scale)  # ✅ Gut
   size = 100                     # ❌ Schlecht
   ```

2. **Verwende Prozente für Layout**
   ```python
   x = int(self.width * 0.50)    # ✅ Gut (50% der Breite)
   x = 960                        # ❌ Schlecht (nur bei 1920px korrekt)
   ```

3. **Minimum-Werte für kleine Elemente**
   ```python
   border = max(2, int(5 * self.scale))  # ✅ Mindestens 2px
   ```

4. **Teste auf dem Zielgerät**
   - Entwickle auf Desktop (1920x1080)
   - Teste auf Raspberry Pi (tatsächliche Auflösung)
   - Passe bei Bedarf Prozent-Werte an

## Anpassungen vornehmen

Wenn etwas zu groß/klein ist, passe die Prozent-Werte an:

```python
# Buttons zu klein? Erhöhe die Prozente:
button_width = int(self.width * 0.15)   # Von 0.11 → 0.15
button_height = int(self.height * 0.25) # Von 0.20 → 0.25

# Schrift zu groß? Reduziere die Basis-Größe:
self.font_shot_timer = pygame.freetype.SysFont(None, int(600 * self.scale))  # Von 700 → 600
```

Die Änderungen wirken sich automatisch auf alle Bildschirmgrößen aus!
