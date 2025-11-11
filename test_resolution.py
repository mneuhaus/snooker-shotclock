#!/usr/bin/env python3
"""
Quick resolution test script for Raspberry Pi
Shows actual screen resolution and calculated scale factor
"""

import pygame
import sys

def test_resolution():
    """Test and display screen resolution"""
    pygame.init()
    
    # Get display info
    info = pygame.display.Info()
    print("=" * 60)
    print("DISPLAY INFORMATION")
    print("=" * 60)
    print(f"Native Resolution: {info.current_w} x {info.current_h}")
    
    # Calculate scale factor
    scale = min(info.current_w / 1920, info.current_h / 1080)
    print(f"Scale Factor: {scale:.3f}")
    print()
    
    # Show what font sizes will be used
    print("CALCULATED SIZES:")
    print("-" * 60)
    print(f"Frame Timer Font: {int(380 * scale)} px (base: 380)")
    print(f"Shot Timer Font:  {int(700 * scale)} px (base: 700)")
    print(f"Button Font:      {int(70 * scale)} px (base: 70)")
    print(f"Hint Font:        {int(45 * scale)} px (base: 45)")
    print()
    
    # Show button sizes
    button_width = int(info.current_w * 0.11)
    button_height = int(info.current_h * 0.20)
    print(f"Button Size:      {button_width} x {button_height} px")
    print(f"  (11% width, 20% height)")
    print()
    
    # Show logo size
    logo_size = int(280 * scale)
    print(f"Logo Size:        {logo_size} x {logo_size} px (base: 280)")
    print()
    
    # Create test window
    print("=" * 60)
    print("Creating test window...")
    print("Press ESC or close window to exit")
    print("=" * 60)
    
    try:
        screen = pygame.display.set_mode((info.current_w, info.current_h))
        pygame.display.set_caption("Resolution Test - Press ESC to exit")
        
        # Initialize font
        pygame.freetype.init()
        import pygame.freetype
        font = pygame.freetype.SysFont(None, int(70 * scale))
        
        # Simple render loop
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Clear screen
            screen.fill((55, 75, 80))
            
            # Draw resolution info
            texts = [
                f"Screen: {info.current_w} x {info.current_h}",
                f"Scale: {scale:.3f}",
                f"",
                f"Frame Font: {int(380 * scale)}px",
                f"Shot Font: {int(700 * scale)}px",
                f"Button: {button_width}x{button_height}",
                f"",
                "Press ESC to exit"
            ]
            
            y = 100
            for text in texts:
                if text:
                    rect = font.get_rect(text)
                    rect.center = (info.current_w // 2, y)
                    font.render_to(screen, rect, text, (255, 255, 255))
                y += int(60 * scale)
            
            pygame.display.flip()
            clock.tick(30)
        
    except Exception as e:
        print(f"Error creating window: {e}")
        return False
    
    pygame.quit()
    return True

if __name__ == "__main__":
    success = test_resolution()
    sys.exit(0 if success else 1)
