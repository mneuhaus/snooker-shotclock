"""GPIO control for LED indicators on Raspberry Pi"""
import config

# Try to import GPIO libraries (only available on Raspberry Pi)
try:
    if config.USE_GPIO:
        from gpiozero import LED
        GPIO_AVAILABLE = True
    else:
        GPIO_AVAILABLE = False
except ImportError:
    GPIO_AVAILABLE = False


class GPIOControl:
    """Controls 5 LED indicators via GPIO for countdown display"""
    
    def __init__(self):
        self.enabled = config.USE_GPIO and GPIO_AVAILABLE
        self.leds = []
        
        if self.enabled:
            try:
                # Initialize 5 LEDs
                for pin in config.LED_PINS:
                    self.leds.append(LED(pin))
                print(f"GPIO: {len(self.leds)} LEDs initialized on pins {config.LED_PINS}")
            except Exception as e:
                print(f"Failed to initialize GPIO: {e}")
                self.enabled = False
                
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
