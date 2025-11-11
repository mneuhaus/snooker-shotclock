"""UI rendering for the shot clock"""
import pygame
import pygame.freetype
import os
import math
import config


class Button:
    """A clickable button"""
    
    def __init__(self, x, y, width, height, text, scale=1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.scale = scale
        self.border_radius = int(20 * scale)
        self.border_width = max(3, int(5 * scale))
        
    def draw(self, screen, font):
        """Draw the button"""
        color = config.COLOR_BUTTON_HOVER if self.is_hovered else config.COLOR_BUTTON
        
        # Draw rounded rectangle background
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, config.COLOR_BUTTON_BORDER, self.rect, 
                        self.border_width, border_radius=self.border_radius)
        
        # Draw text with proper padding and spacing
        lines = self.text.split('\n')
        # Get actual text height from font for better spacing
        text_rect_sample = font.get_rect(lines[0] if lines else "A")
        line_height = int(text_rect_sample.height * 1.4)  # 40% padding between lines
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
    """Main UI renderer with responsive layout"""
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Calculate responsive sizes based on screen dimensions
        # Scale factor: how much to scale relative to 1920x1080 reference
        self.scale = min(self.width / 1920, self.height / 1080)
        
        print(f"Screen: {self.width}x{self.height}, Scale factor: {self.scale:.2f}")
        
        # Initialize fonts using freetype (more stable)
        pygame.freetype.init()
        
        # Font sizes scale with screen size (based on 1920x1080 reference)
        # These are the base sizes at 1920x1080, they will scale down/up automatically
        self.font_frame_timer = pygame.freetype.SysFont(None, int(380 * self.scale))
        self.font_shot_timer = pygame.freetype.SysFont(None, int(700 * self.scale))
        self.font_button = pygame.freetype.SysFont(None, int(70 * self.scale))
        self.font_hint = pygame.freetype.SysFont(None, int(45 * self.scale))
        
        print(f"Font sizes - Frame: {int(380 * self.scale)}, Shot: {int(700 * self.scale)}, Button: {int(70 * self.scale)}")
        
        # Load logo first to calculate layout
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'SFW-Logo.png')
        self.logo_size = int(280 * self.scale)  # Responsive logo size
        try:
            self.logo = pygame.image.load(logo_path)
            # Scale logo to match button size
            self.logo = pygame.transform.smoothscale(self.logo, (self.logo_size, self.logo_size))
            print(f"Logo loaded from {logo_path}, size: {self.logo_size}x{self.logo_size}")
        except Exception as e:
            print(f"Failed to load logo: {e}")
            self.logo = None
        
        # Create buttons with responsive layout: [Start] [Logo] [Reset] - LEFT ALIGNED
        # All sizes are relative to screen dimensions for perfect scaling
        button_width = int(self.width * 0.11)    # ~11% of screen width
        button_height = int(self.height * 0.20)  # ~20% of screen height
        button_margin = int(self.width * 0.015)  # ~1.5% margin from edges
        spacing = int(self.width * 0.02)         # ~2% spacing between elements
        
        print(f"Button size: {button_width}x{button_height}, margin: {button_margin}, spacing: {spacing}")
        
        # Left-aligned layout (not centered)
        start_x = button_margin
        
        self.button_start = Button(
            start_x, button_margin,
            button_width, button_height,
            "Start\nFrame",
            scale=self.scale
        )
        
        # Logo position (between buttons)
        self.logo_x = start_x + button_width + spacing
        self.logo_y = button_margin
        
        # Reset button to the right of logo
        self.button_reset = Button(
            self.logo_x + self.logo_size + spacing, button_margin,
            button_width, button_height,
            "Reset\nFrame",
            scale=self.scale
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
            
            logo_font = pygame.freetype.SysFont(None, int(60 * self.scale))
            text_rect = logo_font.get_rect("LOGO")
            text_rect.center = (center_x, center_y)
            logo_font.render_to(self.screen, text_rect, "LOGO", config.COLOR_TEXT)
    
    def draw_led_indicators(self, timer_state):
        """Draw 5 LED circles for countdown visualization"""
        # Position: top right area, responsive sizing
        led_size = int(30 * self.scale)      # Responsive LED size
        led_spacing = int(10 * self.scale)   # Responsive spacing
        start_x = int(self.width - (450 * self.scale))
        start_y = int(100 * self.scale)
        
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
            border_width = max(1, int(2 * self.scale))
            pygame.draw.circle(self.screen, (255, 255, 255), (x + led_size//2, y), led_size//2, border_width)
        
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
        
        # Draw LED countdown indicators (5 circles, top right)
        self.draw_led_indicators(timer_state)
        
        # Draw hint text - only middle mouse button hint
        hint_middle = "Hold middle mouse button while balls rolling"
        hint_middle_rect = self.font_hint.get_rect(hint_middle)
        hint_middle_rect.midbottom = (self.width // 2, int(self.height - (40 * self.scale)))
        self.font_hint.render_to(self.screen, hint_middle_rect, hint_middle, config.COLOR_TEXT)
        
        # Define precise layout areas with clear boundary
        # Frame timer gets left 60%, Shot timer gets right 40%
        boundary = int(self.width * 0.60)  # Clear boundary at 60%
        
        # Draw frame timer (LEFT area)
        frame_time_text = timer_state.get_frame_time_str()
        frame_rect = self.font_frame_timer.get_rect(frame_time_text)
        
        # Position frame timer: centered in left area, but keep distance from boundary
        frame_x = int(self.width * 0.25)  # 25% from left
        frame_rect.center = (frame_x, self.height // 2)
            
        self.font_frame_timer.render_to(self.screen, frame_rect, frame_time_text, config.COLOR_TEXT)
        
        # Draw shot timer (RIGHT area with more room)
        shot_time_text = timer_state.get_shot_time_str()
        
        # Change color based on time remaining
        shot_color = config.COLOR_TEXT
        if timer_state.is_shot_critical():
            shot_color = config.COLOR_CRITICAL
        elif timer_state.is_shot_warning():
            shot_color = config.COLOR_WARNING
            
        shot_rect = self.font_shot_timer.get_rect(shot_time_text)
        # Position shot timer: 80% from left (center of right 40% area)
        shot_x = int(self.width * 0.80)
        shot_rect.center = (shot_x, self.height // 2)
        self.font_shot_timer.render_to(self.screen, shot_rect, shot_time_text, shot_color)
        
        # Draw "Balls Rolling" indicator when middle mouse is held
        if timer_state.balls_rolling:
            rolling_text = "BALLS ROLLING - Timer Paused"
            rolling_font = pygame.freetype.SysFont(None, int(50 * self.scale))
            rolling_rect = rolling_font.get_rect(rolling_text)
            rolling_rect.center = (self.width // 2, int(self.height // 2 + (200 * self.scale)))
            
            # Draw semi-transparent background
            padding = int(30 * self.scale)
            overlay = pygame.Surface((rolling_rect.width + padding * 2, rolling_rect.height + padding))
            overlay.set_alpha(220)
            overlay.fill((40, 40, 40))
            overlay_rect = overlay.get_rect(center=rolling_rect.center)
            self.screen.blit(overlay, overlay_rect)
            
            # Draw text
            rolling_font.render_to(self.screen, rolling_rect, rolling_text, (255, 200, 0))
        
        pygame.display.flip()
