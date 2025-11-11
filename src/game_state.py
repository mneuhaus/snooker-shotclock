"""Game state management and timer logic"""
import time
import math
from enum import Enum
import config


class GameState(Enum):
    """Game states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"


class TimerState:
    """Manages the shot clock timer state"""
    
    def __init__(self):
        self.frame_time_remaining = config.FRAME_DURATION
        self.shot_time_remaining = config.SHOT_TIME_FIRST_HALF
        self.state = GameState.IDLE
        self.last_update = None
        self.balls_rolling = False  # True when middle mouse button is held
        
    def start_frame(self):
        """Start a new frame"""
        self.frame_time_remaining = config.FRAME_DURATION
        self.shot_time_remaining = config.SHOT_TIME_FIRST_HALF
        self.state = GameState.RUNNING
        self.last_update = time.time()
        
    def reset_frame(self):
        """Reset frame to initial state"""
        self.frame_time_remaining = config.FRAME_DURATION
        self.shot_time_remaining = self._get_shot_time_for_current_frame()
        self.state = GameState.IDLE
        self.last_update = None
        
    def pause_frame(self):
        """Pause/unpause the frame timer"""
        if self.state == GameState.RUNNING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.RUNNING
            self.last_update = time.time()
            
    def reset_shot(self):
        """Reset shot timer (can be called even when timer expired)"""
        if self.state == GameState.RUNNING or self.state == GameState.PAUSED:
            self.shot_time_remaining = self._get_shot_time_for_current_frame()
            # Restart timing if we were running
            if self.state == GameState.RUNNING:
                self.last_update = time.time()
            
    def _get_shot_time_for_current_frame(self):
        """Get correct shot time based on frame time remaining"""
        if self.frame_time_remaining > config.FIRST_HALF_DURATION:
            return config.SHOT_TIME_FIRST_HALF
        else:
            return config.SHOT_TIME_SECOND_HALF
            
    def set_balls_rolling(self, rolling):
        """Set balls rolling state (pauses shot timer, resets it when pressed)"""
        self.balls_rolling = rolling
        if rolling:
            # Reset shot timer when middle button is pressed
            self.shot_time_remaining = self._get_shot_time_for_current_frame()
            self.last_update = time.time()
            
    def update(self):
        """Update timers - call this every frame"""
        if self.state != GameState.RUNNING or self.last_update is None:
            return
            
        current_time = time.time()
        delta = current_time - self.last_update
        self.last_update = current_time
        
        # Update frame timer (always runs, even when balls rolling)
        self.frame_time_remaining -= delta
        if self.frame_time_remaining < 0:
            self.frame_time_remaining = 0
            self.state = GameState.IDLE
            
        # Update shot timer only when balls are NOT rolling
        if not self.balls_rolling:
            self.shot_time_remaining -= delta
            if self.shot_time_remaining < 0:
                self.shot_time_remaining = 0
            
    def get_frame_time_str(self):
        """Get frame time as MM:SS string"""
        minutes = int(self.frame_time_remaining // 60)
        seconds = int(self.frame_time_remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def get_shot_time_str(self):
        """Get shot time as integer seconds string"""
        # Use ceiling so it shows 15 until it reaches 14.0
        seconds = math.ceil(self.shot_time_remaining)
        if seconds < 0:
            seconds = 0
        return str(seconds)
        
    def is_shot_warning(self):
        """Check if shot time is in warning zone"""
        return 0 < self.shot_time_remaining <= config.SHOT_WARNING_TIME
        
    def is_shot_critical(self):
        """Check if shot time is critical"""
        return 0 < self.shot_time_remaining <= config.SHOT_CRITICAL_TIME
