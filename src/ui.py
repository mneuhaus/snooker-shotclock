"""UI rendering for the shot clock"""
import pygame
import pygame.freetype
import os
import math
import config


class Button:
    """A clickable button"""
    
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, screen, font):
        """Draw the button"""
        color = config.COLOR_BUTTON_HOVER if self.is_hovered else config.COLOR_BUTTON
        
        # Draw rounded rectangle background
        pygame.draw.rect(screen, color, self.rect, border_radius=20)
        pygame.draw.rect(screen, config.COLOR_BUTTON_BORDER, self.rect, 5, border_radius=20)
        
        # Draw text with proper padding
        lines = self.text.split('\n')
        line_height = 50
        total_height = len(lines) * line_height
        y_offset = self.rect.centery - total_height // 2 + line_height // 2
        
        for line in lines:
            text_rect = font.get_rect(line)
            text_rect.center = (self.rect.centerx, y_offset)
            font.render_to(screen, text_rect, line, config.COLOR_TEXT)
            y_offset += line_height
            
    def handle_mouse(self, pos):
        """Update hover state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(pos)


class UI:
    """Main UI renderer"""
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize fonts using freetype (more stable)
        pygame.freetype.init()
        # Optimized font sizes for 2/3 layout
        self.font_frame_timer = pygame.freetype.SysFont(None, 380)  # Smaller for 2/3 width
        self.font_shot_timer = pygame.freetype.SysFont(None, 700)   # Big for 1/3 width
        self.font_button = pygame.freetype.SysFont(None, 70)        # Bigger buttons
        self.font_hint = pygame.freetype.SysFont(None, 45)
        
        # Load logo first to calculate layout
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'SFW-Logo.png')
        self.logo_size = 280  # Bigger logo
        try:
            self.logo = pygame.image.load(logo_path)
            # Scale logo to match button size
            self.logo = pygame.transform.smoothscale(self.logo, (self.logo_size, self.logo_size))
            print(f"Logo loaded from {logo_path}")
        except Exception as e:
            print(f"Failed to load logo: {e}")
            self.logo = None
        
        # Create buttons with layout: [Start] [Logo] [Reset] - LEFT ALIGNED
        # Buttons + Logo should take ~2/3 of screen width
        button_width = 220   # Bigger buttons
        button_height = 220
        button_margin = 30
        spacing = 40  # Space between elements
        
        # Left-aligned layout (not centered)
        start_x = button_margin
        
        self.button_start = Button(
            start_x, button_margin,
            button_width, button_height,
            "Start\nFrame"
        )
        
        # Logo position (between buttons)
        self.logo_x = start_x + button_width + spacing
        self.logo_y = button_margin
        
        # Reset button to the right of logo
        self.button_reset = Button(
            self.logo_x + self.logo_size + spacing, button_margin,
            button_width, button_height,
            "Reset\nFrame"
        )
        
    def draw_logo(self):
        """Draw the club logo between the buttons"""
        # Position logo at calculated position (same y as buttons)
        center_x = self.logo_x + self.logo_size // 2
        center_y = self.logo_y + self.logo_size // 2
        
        if self.logo:
            # Draw the actual logo
            logo_rect = self.logo.get_rect(center=(center_x, center_y))
            self.screen.blit(self.logo, logo_rect)
        else:
            # Fallback to placeholder circle
            radius = self.logo_size // 2
            pygame.draw.circle(self.screen, (100, 150, 200), (center_x, center_y), radius)
            pygame.draw.circle(self.screen, config.COLOR_TEXT, (center_x, center_y), radius, 4)
            
            logo_font = pygame.freetype.SysFont(None, 60)
            text_rect = logo_font.get_rect("LOGO")
            text_rect.center = (center_x, center_y)
            logo_font.render_to(self.screen, text_rect, "LOGO", config.COLOR_TEXT)
    
    def draw_led_indicators(self, timer_state):
        """Draw 5 LED circles for countdown visualization"""
        # Position: top center, right of "Press Shot Timer to reset" text
        led_size = 30  # Diameter of each LED
        led_spacing = 10  # Space between LEDs
        start_x = self.width - 450
        start_y = 100
        
        # Calculate how many LEDs should be lit based on shot time
        shot_time = math.ceil(timer_state.shot_time_remaining)
        leds_lit = min(5, max(0, shot_time))  # 5s=5 LEDs, 4s=4 LEDs, ..., 0s=0 LEDs
        
        # Draw 5 LEDs
        for i in range(5):
            x = start_x + i * (led_size + led_spacing)
            y = start_y
            
            # LED is lit if index < leds_lit
            if i < leds_lit:
                # Lit LED - bright color
                if leds_lit <= 2:
                    color = config.COLOR_CRITICAL  # Red for critical (1-2s)
                elif leds_lit <= 3:
                    color = config.COLOR_WARNING   # Orange for warning (3s)
                else:
                    color = (100, 255, 100)        # Green for OK (4-5s)
            else:
                # Unlit LED - dark gray
                color = (60, 70, 75)
            
            # Draw LED circle
            pygame.draw.circle(self.screen, color, (x + led_size//2, y), led_size//2)
            # Draw border
            pygame.draw.circle(self.screen, (255, 255, 255), (x + led_size//2, y), led_size//2, 2)
        
    def draw(self, timer_state):
        """Draw the entire UI"""
        # Clear screen
        self.screen.fill(config.COLOR_BACKGROUND)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        self.button_start.handle_mouse(mouse_pos)
        self.button_reset.handle_mouse(mouse_pos)
        
        self.button_start.draw(self.screen, self.font_button)
        self.button_reset.draw(self.screen, self.font_button)
        
        # Draw logo
        self.draw_logo()
        
        # Draw LED countdown indicators (5 circles, top center)
        self.draw_led_indicators(timer_state)
        
        # Draw hint texts
        hint_top_rect = self.font_hint.get_rect("Press Shot Timer to reset")
        hint_top_rect.topright = (self.width - 40, 40)
        self.font_hint.render_to(self.screen, hint_top_rect, "Press Shot Timer to reset", config.COLOR_TEXT)
        
        hint_bottom_rect = self.font_hint.get_rect("Press Frame Timer to pause frame")
        hint_bottom_rect.bottomleft = (50, self.height - 40)
        self.font_hint.render_to(self.screen, hint_bottom_rect, "Press Frame Timer to pause frame", config.COLOR_TEXT)
        
        # Define precise layout areas
        # Left area for Frame Timer: 0 to 2/3 width
        # Right area for Shot Timer: 2/3 to full width
        boundary = int(self.width * 0.65)  # 65% boundary to give more space
        
        # Draw frame timer (LEFT area - constrained to not exceed boundary)
        frame_time_text = timer_state.get_frame_time_str()
        frame_rect = self.font_frame_timer.get_rect(frame_time_text)
        
        # Position frame timer: right-aligned at 60% of screen width
        frame_x = int(self.width * 0.30)  # Center of left area
        frame_rect.center = (frame_x, self.height // 2)
        
        # Make sure frame timer doesn't overlap boundary
        if frame_rect.right > boundary - 50:
            frame_rect.right = boundary - 50
            
        self.font_frame_timer.render_to(self.screen, frame_rect, frame_time_text, config.COLOR_TEXT)
        
        # Draw shot timer (RIGHT area - starts after boundary)
        shot_time_text = timer_state.get_shot_time_str()
        
        # Change color based on time remaining
        shot_color = config.COLOR_TEXT
        if timer_state.is_shot_critical():
            shot_color = config.COLOR_CRITICAL
        elif timer_state.is_shot_warning():
            shot_color = config.COLOR_WARNING
            
        shot_rect = self.font_shot_timer.get_rect(shot_time_text)
        # Position shot timer: center of right area
        shot_x = boundary + (self.width - boundary) // 2
        shot_rect.center = (shot_x, self.height // 2)
        self.font_shot_timer.render_to(self.screen, shot_rect, shot_time_text, shot_color)
        
        # Draw "Balls Rolling" indicator when middle mouse is held
        if timer_state.balls_rolling:
            rolling_text = "BALLS ROLLING - Timer Paused"
            rolling_font = pygame.freetype.SysFont(None, 50)
            rolling_rect = rolling_font.get_rect(rolling_text)
            rolling_rect.center = (self.width // 2, self.height // 2 + 200)
            
            # Draw semi-transparent background
            padding = 30
            overlay = pygame.Surface((rolling_rect.width + padding * 2, rolling_rect.height + padding))
            overlay.set_alpha(220)
            overlay.fill((40, 40, 40))
            overlay_rect = overlay.get_rect(center=rolling_rect.center)
            self.screen.blit(overlay, overlay_rect)
            
            # Draw text
            rolling_font.render_to(self.screen, rolling_rect, rolling_text, (255, 200, 0))
        
        pygame.display.flip()
