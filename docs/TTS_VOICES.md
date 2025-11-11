# TTS Voice Configuration

## espeak Voices on Raspberry Pi

espeak (default) hat hauptsächlich männliche Stimmen, aber es gibt Varianten:

### Empfohlene Stimmen:

```python
# In config.py:
TTS_VOICE = 'en-gb'        # Britisches Englisch (männlich)
TTS_VOICE = 'en-gb+f3'     # Britisches Englisch (weiblich, höher)
TTS_VOICE = 'en-gb+f4'     # Britisches Englisch (weiblich, sehr hoch)
TTS_VOICE = 'en-us'        # Amerikanisches Englisch (männlich)
TTS_VOICE = 'en-us+f3'     # Amerikanisches Englisch (weiblich)
```

### Stimm-Varianten:

espeak unterstützt Modifikatoren:
- `+f1` - leicht höher
- `+f2` - etwas höher
- `+f3` - weiblich (höher)
- `+f4` - sehr weiblich (sehr hoch)
- `+m1` - leicht tiefer
- `+m2` - etwas tiefer
- `+m3` - sehr tief

### Geschwindigkeit:

```python
TTS_SPEED = 150  # Langsam
TTS_SPEED = 175  # Standard (empfohlen)
TTS_SPEED = 200  # Schnell
```

## Bessere Stimmen mit espeak-ng

Für bessere Qualität, installiere `espeak-ng`:

```bash
sudo apt install espeak-ng
```

espeak-ng hat bessere Stimmen und Intonation.

**Nach Installation:**
```python
# In config.py bleibt alles gleich
TTS_VOICE = 'en-gb+f3'  # Weibliche Stimme
```

espeak-ng verwendet die gleichen Voice-IDs wie espeak.

## Alle verfügbaren Stimmen anzeigen:

```bash
espeak --voices
# oder
espeak-ng --voices
```

## Stimme testen:

```bash
# Männlich (Standard)
espeak -v en-gb "15 seconds shot clock now in operation"

# Weiblich
espeak -v en-gb+f3 "15 seconds shot clock now in operation"

# Amerikanisch weiblich
espeak -v en-us+f3 "15 seconds shot clock now in operation"

# Mit Geschwindigkeit
espeak -v en-gb+f3 -s 175 "15 seconds shot clock now in operation"
```

## Empfohlene Konfiguration:

### Für weibliche Stimme (empfohlen):

```python
# config.py
TTS_VOICE = 'en-gb+f3'   # Britisch, weiblich
TTS_SPEED = 175          # Etwas schneller als Standard
```

### Für männliche Stimme:

```python
# config.py
TTS_VOICE = 'en-gb'      # Britisch, männlich
TTS_SPEED = 175
```

### Für amerikanische Stimme:

```python
# config.py
TTS_VOICE = 'en-us+f3'   # Amerikanisch, weiblich
TTS_SPEED = 175
```

## Andere Sprachen:

espeak unterstützt viele Sprachen:

```python
TTS_VOICE = 'de'         # Deutsch
TTS_VOICE = 'de+f3'      # Deutsch, weiblich
TTS_VOICE = 'fr'         # Französisch
TTS_VOICE = 'es'         # Spanisch
```

**Hinweis:** Die Nachrichten sind auf Englisch, klingen aber mit deutscher Stimme komisch.

## Lautstärke:

espeak Lautstärke wird über die System-Lautstärke gesteuert, nicht über config.py.

```bash
# System-Lautstärke prüfen
amixer get PCM

# System-Lautstärke setzen
amixer set PCM 80%
```

## Troubleshooting:

### Stimme nicht gefunden:

```
Error: voice not found
```

**Lösung:**
```bash
# Verfügbare Stimmen auflisten
espeak --voices

# Stimme testen
espeak -v en-gb+f3 "test"
```

### Stimme zu hoch/tief:

Probiere verschiedene Varianten:
- `+f2` statt `+f3` (weniger hoch)
- `+f1` (nur leicht höher)
- Keine Variante (Standard männlich)

### Zu schnell/langsam:

```python
TTS_SPEED = 150  # Langsamer
TTS_SPEED = 200  # Schneller
```

## Installation espeak-ng (bessere Qualität):

```bash
# Auf Raspberry Pi
sudo apt update
sudo apt install espeak-ng

# Testen
espeak-ng -v en-gb+f3 "test message"
```

**Vorteil von espeak-ng:**
- Bessere Intonation
- Natürlichere Stimmen
- Mehr Sprachen
- Gleiche Voice-IDs wie espeak

## Quick Test verschiedener Stimmen:

```bash
# Alle weiblichen Varianten testen
for voice in en-gb+f1 en-gb+f2 en-gb+f3 en-gb+f4; do
  echo "Testing: $voice"
  espeak -v $voice "15 seconds shot clock now in operation"
  sleep 1
done
```

Finde heraus, welche dir am besten gefällt, und setze sie in `config.py`!

## Empfehlung für Snooker:

Für professionelle Snooker-Ansagen:

```python
TTS_VOICE = 'en-gb+f3'   # Britisch weiblich (klingt professionell)
TTS_SPEED = 175          # Klar und deutlich
```

Oder männlich für traditionelle Ansager-Stimme:

```python
TTS_VOICE = 'en-gb+m1'   # Britisch männlich, etwas tiefer
TTS_SPEED = 170          # Etwas langsamer für Klarheit
```
