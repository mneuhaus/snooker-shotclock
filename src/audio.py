"""Audio system for warnings and notifications"""
import pygame
import os
import math
import config


class AudioSystem:
    """Manages sound effects and voice announcements"""
    
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
            
            # Load voice announcement WAV files
            announcement_15_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.ANNOUNCEMENT_15_SECONDS)
            announcement_10_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.ANNOUNCEMENT_10_SECONDS)
            
            try:
                self.announcement_15 = pygame.mixer.Sound(announcement_15_path)
                self.announcement_15.set_volume(config.SOUND_VOLUME)
                print(f"15 seconds announcement loaded from {announcement_15_path}")
            except Exception as e:
                print(f"Failed to load 15 seconds announcement: {e}")
                self.announcement_15 = None
            
            try:
                self.announcement_10 = pygame.mixer.Sound(announcement_10_path)
                self.announcement_10.set_volume(config.SOUND_VOLUME)
                print(f"10 seconds announcement loaded from {announcement_10_path}")
            except Exception as e:
                print(f"Failed to load 10 seconds announcement: {e}")
                self.announcement_10 = None
            
        self.last_second = None  # Track which second we're at for beeps
        self.shot_expired_played = False  # Track if we played the expiry sound
        self.frame_expired_played = False  # Track if we played frame expiry sound
        self.announced_15s = False  # Track if we announced 15s
        self.announced_10s = False  # Track if we announced 10s
        
    def announce_shot_clock(self, seconds):
        """Announce shot clock time with WAV file"""
        if not self.enabled:
            return
            
        print(f"Announcement: {seconds} seconds shot clock")
        
        if seconds == 15 and self.announcement_15:
            self.announcement_15.play()
        elif seconds == 10 and self.announcement_10:
            self.announcement_10.play()
    
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
        
        # Track shot time for tick sounds
        shot_time = int(timer_state.shot_time_remaining)
        
        # Play tick sound every second from 5 to 1
        if shot_time <= 5 and shot_time >= 1:
            if self.last_second != shot_time:
                self._play_tick()
                self.last_second = shot_time
        else:
            self.last_second = None
        
        # Play ZONK when shot timer expires
        if shot_time <= 0 and not self.shot_expired_played:
            print("Shot time expired! Playing zonk")
            self._play_zonk()
            self.shot_expired_played = True
        elif shot_time > 0:
            self.shot_expired_played = False
    
    def _play_tick(self):
        """Play a tick sound (generated)"""
        if not self.enabled:
            return
        try:
            # Generate a short beep sound
            import numpy as np
            sample_rate = 22050
            duration = 0.1  # 100ms
            frequency = 800  # Hz
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * math.pi * frequency * t)
            
            # Apply envelope to avoid clicks
            envelope = np.exp(-t * 20)
            wave = wave * envelope
            
            # Convert to 16-bit integers
            wave = (wave * 32767).astype(np.int16)
            
            # Create stereo sound (duplicate mono to both channels)
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(config.SOUND_VOLUME * 0.3)  # Quieter tick
            sound.play()
        except Exception as e:
            pass  # Silently fail if numpy not available
    
    def _play_zonk(self):
        """Play the ZONK sound"""
        if not self.enabled or not self.zonk_sound:
            return
        try:
            # Play for 1 second max
            self.zonk_sound.play(maxtime=1000)
        except Exception as e:
            print(f"Failed to play zonk: {e}")
