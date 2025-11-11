"""Audio system for warnings and notifications"""
import pygame
import os
import math
import threading
import config

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 not available - TTS disabled")


class AudioSystem:
    """Manages sound effects and text-to-speech"""
    
    def __init__(self):
        self.enabled = config.SOUND_ENABLED
        if self.enabled:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(config.SOUND_VOLUME)
            
            # Load zonk sound
            zonk_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds', 'zonk.mp3')
            try:
                self.zonk_sound = pygame.mixer.Sound(zonk_path)
                self.zonk_sound.set_volume(config.SOUND_VOLUME)
                print(f"Zonk sound loaded from {zonk_path}")
            except Exception as e:
                print(f"Failed to load zonk sound: {e}")
                self.zonk_sound = None
        
        # Initialize TTS
        self.tts_engine = None
        if TTS_AVAILABLE and self.enabled:
            try:
                self.tts_engine = pyttsx3.init()
                # Set Moira voice (Irish English)
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if 'moira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        print(f"TTS voice set to: {voice.name}")
                        break
                self.tts_engine.setProperty('rate', 172)  # Speed (15% faster: 150 * 1.15 = 172.5)
                print("TTS initialized")
            except Exception as e:
                print(f"Failed to initialize TTS: {e}")
                self.tts_engine = None
            
        self.last_second = None  # Track which second we're at for beeps
        self.shot_expired_played = False  # Track if we played the expiry sound
        self.frame_expired_played = False  # Track if we played frame expiry sound
        self.announced_15s = False  # Track if we announced 15s
        self.announced_10s = False  # Track if we announced 10s
        
    def announce_shot_clock(self, seconds):
        """Announce shot clock time with TTS (run in thread to not block)"""
        if not self.tts_engine:
            return
            
        def speak():
            try:
                message = f"{seconds} seconds shot clock now in operation"
                print(f"TTS: {message}")
                self.tts_engine.say(message)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS failed: {e}")
        
        # Run in thread so it doesn't block the game
        thread = threading.Thread(target=speak, daemon=True)
        thread.start()
    
    def update(self, timer_state):
        """Update audio based on timer state"""
        if not self.enabled:
            return
            
        # Reset announcement flags when not running
        if timer_state.state.value != "running":
            self.announced_15s = False
            self.announced_10s = False
            self.frame_expired_played = False
            return
        
        # Check for shot clock announcements at frame start
        if not self.announced_15s and timer_state.frame_time_remaining > config.FIRST_HALF_DURATION:
            # First half - 15 seconds
            self.announce_shot_clock(15)
            self.announced_15s = True
        
        # Announcement at 5 minute mark (switch to 10 seconds)
        if not self.announced_10s and timer_state.frame_time_remaining <= config.FIRST_HALF_DURATION:
            self.announce_shot_clock(10)
            self.announced_10s = True
        
        # Play ZONK when frame time expires (10 minutes up)
        if timer_state.frame_time_remaining <= 0 and not self.frame_expired_played:
            print("Frame time expired! Playing zonk")
            self._play_zonk()
            self.frame_expired_played = True
            return
        
        # Don't play sounds while balls are rolling
        if timer_state.balls_rolling:
            return
            
        shot_time = timer_state.shot_time_remaining
        current_second = math.ceil(shot_time)
        
        # Reset expired flag when timer is reset
        if shot_time > 0 and self.shot_expired_played:
            self.shot_expired_played = False
            self.last_second = None
            
        # Play zonk sound when timer expires (only once) - CHECK FIRST
        if shot_time <= 0 and not self.shot_expired_played:
            print(f"Timer expired! shot_time={shot_time}, playing zonk")
            self._play_zonk()
            self.shot_expired_played = True
            return
        
        # Check if we're at a new second for tick sounds
        if current_second != self.last_second:
            self.last_second = current_second
            
            # Play tick sound every second when <= 5 seconds (but > 0)
            if 0 < shot_time <= 5:
                self._play_tick()
                
    def _play_tick(self):
        """Play a light tick/beep sound for countdown"""
        try:
            import numpy as np
            sample_rate = 22050
            duration = 0.1  # Short tick
            samples = int(sample_rate * duration)
            
            # Light beep at 800 Hz
            wave = np.sin(2.0 * np.pi * 800 * np.arange(samples) / sample_rate)
            # Apply fade out envelope for softer sound
            envelope = np.linspace(1.0, 0.0, samples)
            wave = wave * envelope * 0.3  # Lower volume (30%)
            wave = (wave * 32767).astype(np.int16)
            
            # Convert to stereo
            stereo_wave = np.zeros((samples, 2), dtype=np.int16)
            stereo_wave[:, 0] = wave
            stereo_wave[:, 1] = wave
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
        except Exception as e:
            print(f"Tick playback failed: {e}")
            
    def _play_zonk(self):
        """Play the ZONK sound from MP3 file (shortened to 1s)"""
        try:
            if self.zonk_sound:
                print("Playing ZONK sound!")
                # Play but limit to 1 second
                self.zonk_sound.play(maxtime=1000)  # maxtime in milliseconds
            else:
                print("No zonk sound loaded, using fallback")
                # Fallback to generated sound if file not available
                self._play_zonk_fallback()
        except Exception as e:
            print(f"Zonk playback failed: {e}")
            self._play_zonk_fallback()
            
    def _play_zonk_fallback(self):
        """Fallback ZONK sound if MP3 not available"""
        try:
            import numpy as np
            sample_rate = 22050
            duration = 0.8
            samples = int(sample_rate * duration)
            
            t = np.arange(samples) / sample_rate
            
            # Classic "ZONK" - descending frequency buzzer
            start_freq = 400
            end_freq = 150
            freq = start_freq - (start_freq - end_freq) * (t / duration) ** 1.5
            
            # Add harmonics for buzzer-like quality
            wave = np.sin(2.0 * np.pi * freq * t)
            wave += 0.3 * np.sin(2.0 * np.pi * freq * 2 * t)
            wave += 0.2 * np.sin(2.0 * np.pi * freq * 3 * t)
            
            # Add some noise for "buzziness"
            noise = np.random.normal(0, 0.05, samples)
            wave = wave + noise
            
            # Envelope
            envelope = np.ones(samples)
            attack = int(samples * 0.05)
            release = int(samples * 0.4)
            envelope[:attack] = np.linspace(0, 1, attack)
            envelope[-release:] = np.linspace(1, 0, release)
            
            wave = wave * envelope
            wave = wave / np.max(np.abs(wave))
            wave = (wave * 32767 * 0.8).astype(np.int16)
            
            # Convert to stereo
            stereo_wave = np.zeros((samples, 2), dtype=np.int16)
            stereo_wave[:, 0] = wave
            stereo_wave[:, 1] = wave
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
        except Exception as e:
            print(f"Fallback zonk sound failed: {e}")
