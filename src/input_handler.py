"""Input handling for mouse, keyboard, and HID devices"""
import pygame


class InputHandler:
    """Handles all input events"""
    
    def __init__(self, ui, timer_state):
        self.ui = ui
        self.timer_state = timer_state
        
    def handle_events(self):
        """Process all pygame events
        
        Returns:
            bool: False if quit event received, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Space = Start Frame
                    self.timer_state.start_frame()
                elif event.key == pygame.K_r:
                    # R = Reset Frame
                    self.timer_state.reset_frame()
                elif event.key == pygame.K_p:
                    # P = Pause Frame
                    self.timer_state.pause_frame()
                elif event.key == pygame.K_s:
                    # S = Reset Shot
                    self.timer_state.reset_shot()
                    
            # Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Middle mouse button (button 2) = balls rolling (hold to pause)
                if event.button == 2:
                    self.timer_state.set_balls_rolling(True)
                else:
                    self._handle_click(pos, event.button)
                    
            # Mouse button release
            if event.type == pygame.MOUSEBUTTONUP:
                # Release middle mouse button = balls stopped rolling
                if event.button == 2:
                    self.timer_state.set_balls_rolling(False)
                
            # Support for joystick/gamepad buttons (Bluetooth controllers)
            if event.type == pygame.JOYBUTTONDOWN:
                self._handle_joystick_button(event.button)
                
        return True
        
    def _handle_click(self, pos, button):
        """Handle mouse click at position"""
        # Only handle left clicks (button 1) for UI elements
        if button != 1:
            return
            
        # Check button clicks
        if self.ui.button_start.is_clicked(pos):
            self.timer_state.start_frame()
        elif self.ui.button_reset.is_clicked(pos):
            self.timer_state.reset_frame()
            
        # Check if frame timer was clicked (pause)
        frame_timer_rect = pygame.Rect(40, self.ui.height - 500, 600, 400)
        if frame_timer_rect.collidepoint(pos):
            self.timer_state.pause_frame()
            
        # Check if shot timer was clicked (reset shot)
        shot_timer_rect = pygame.Rect(self.ui.width - 700, self.ui.height // 2 - 200, 600, 400)
        if shot_timer_rect.collidepoint(pos):
            self.timer_state.reset_shot()
            
    def _handle_joystick_button(self, button):
        """Handle joystick/gamepad button press"""
        # Map common button indices
        # Button 0 (A/X) = Start Frame
        # Button 1 (B/Circle) = Reset Shot
        # Button 2 (X/Square) = Pause Frame
        # Button 3 (Y/Triangle) = Reset Frame
        
        if button == 0:
            self.timer_state.start_frame()
        elif button == 1:
            self.timer_state.reset_shot()
        elif button == 2:
            self.timer_state.pause_frame()
        elif button == 3:
            self.timer_state.reset_frame()
