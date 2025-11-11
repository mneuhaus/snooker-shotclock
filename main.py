#!/usr/bin/env python3
"""
Snooker Shot Clock
A pygame-based shot clock for snooker frames with LED indicators
"""
import sys
import pygame
import config
from src.game_state import TimerState
from src.ui import UI
from src.input_handler import InputHandler
from src.audio import AudioSystem
from src.gpio_control import GPIOControl


def main():
    """Main entry point"""
    # Initialize pygame
    pygame.init()
    
    # Initialize joystick support for Bluetooth controllers
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick detected: {joystick.get_name()}")
    
    # Create display
    if config.FULLSCREEN:
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
    pygame.display.set_caption("Snooker Shot Clock")
    
    # Hide mouse cursor in fullscreen
    if config.FULLSCREEN:
        pygame.mouse.set_visible(True)  # Keep visible for now, can be disabled later
    
    # Initialize components
    timer_state = TimerState()
    ui = UI(screen)
    input_handler = InputHandler(ui, timer_state)
    audio_system = AudioSystem()
    gpio_control = GPIOControl()
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    print("Snooker Shot Clock started")
    print("Controls:")
    print("  SPACE - Start Frame")
    print("  R - Reset Frame")
    print("  P - Pause Frame")
    print("  S - Reset Shot")
    print("  ESC/Q - Quit")
    
    try:
        while running:
            # Handle input
            running = input_handler.handle_events()
            
            # Update game state
            timer_state.update()
            
            # Update audio
            audio_system.update(timer_state)
            
            # Update GPIO LEDs
            gpio_control.update(timer_state)
            
            # Render UI
            ui.draw(timer_state)
            
            # Maintain frame rate
            clock.tick(config.FPS)
            
    finally:
        # Cleanup
        gpio_control.cleanup()
        pygame.quit()
        print("Shot clock stopped")
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
