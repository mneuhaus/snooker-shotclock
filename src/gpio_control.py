"""GPIO control for LED indicators and buttons on Raspberry Pi"""
import config

# Try to import GPIO libraries (only available on Raspberry Pi)
try:
    if config.USE_GPIO:
        from gpiozero import LED, Button
        GPIO_AVAILABLE = True
    else:
        GPIO_AVAILABLE = False
except ImportError:
    GPIO_AVAILABLE = False


class GPIOControl:
    """Controls 5 LED indicators and 2 input buttons via GPIO"""
    
    def __init__(self, timer_state=None):
        self.enabled = config.USE_GPIO and GPIO_AVAILABLE
        self.leds = []
        self.button_start = None
        self.button_reset = None
        self.timer_state = timer_state
        
        if self.enabled:
            try:
                # Initialize 5 LEDs (outputs)
                for pin in config.LED_PINS:
                    self.leds.append(LED(pin))
                print(f"GPIO: {len(self.leds)} LEDs initialized on pins {config.LED_PINS}")
                
                # Initialize input buttons with pull-up resistors
                # Buttons connect GPIO pin to GND when pressed
                self.button_start = Button(config.BUTTON_START_PIN, pull_up=True, bounce_time=0.1)
                self.button_reset = Button(config.BUTTON_RESET_PIN, pull_up=True, bounce_time=0.1)
                
                # Set up button callbacks
                if self.timer_state:
                    self.button_start.when_pressed = self._on_start_pressed
                    self.button_reset.when_pressed = self._on_reset_pressed
                
                print(f"GPIO: Input buttons initialized on pins {config.BUTTON_START_PIN} (Start), {config.BUTTON_RESET_PIN} (Reset)")
            except Exception as e:
                print(f"Failed to initialize GPIO: {e}")
                self.enabled = False
    
    def _on_start_pressed(self):
        """Callback when Start button is pressed"""
        if self.timer_state:
            print("GPIO: Start button pressed")
            self.timer_state.start_frame()
    
    def _on_reset_pressed(self):
        """Callback when Reset button is pressed"""
        if self.timer_state:
            print("GPIO: Reset button pressed")
            self.timer_state.reset_frame()
                
    def update(self, timer_state):
        """Update LED states based on timer - countdown style"""
        if not self.enabled:
            return
            
        try:
            shot_time = int(timer_state.shot_time_remaining)
            
            if timer_state.state.value != "running":
                # All LEDs off when not running
                self.all_off()
            else:
                # Light up LEDs based on remaining seconds (max 5)
                leds_lit = min(5, max(0, shot_time))
                
                for i in range(5):
                    if i < leds_lit:
                        self.leds[i].on()
                    else:
                        self.leds[i].off()
                    
        except Exception as e:
            print(f"GPIO update failed: {e}")
            
    def all_off(self):
        """Turn all LEDs off"""
        if self.enabled:
            for led in self.leds:
                led.off()
                
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.enabled:
            self.all_off()
            for led in self.leds:
                led.close()
            if self.button_start:
                self.button_start.close()
            if self.button_reset:
                self.button_reset.close()
