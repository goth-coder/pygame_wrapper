import sys
import time

import pygame

# Settings
WIDTH, HEIGHT = 800, 600
TOP_PANEL_HEIGHT = 90

# Colors Constants
SKY_BLUE = (135, 206, 235)
BACKGROUND_COLOR = SKY_BLUE
WHITE = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 60)
PANEL_COLOR = (50, 50, 50)
INSTRUCTION_COLOR = (220, 220, 220)
PAUSED_STATE_COLOR = (200, 80, 80)
BUTTON_HOVER_COLOR = (210, 210, 210)
BUTTON_BASE_COLOR = (190, 190, 190)
BUTTON_BORDER_COLOR = (80, 80, 80)
BUTTON_TEXT_COLOR = (30, 30, 30)
BUTTON_SHADOW_COLOR = (60, 60, 60, 120)


def lerp_color(c1, c2, t):
    """
    Linearly interpolates between two colors.
    Args:
        c1 (tuple): The starting color as a tuple of RGB or RGBA values.
        c2 (tuple): The ending color as a tuple of RGB or RGBA values.
        t (float): Interpolation factor between 0.0 and 1.0.
    Returns:
        tuple: The interpolated color.
    """
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


class UIButton:
    """Button class for the UI."""

    def __init__(self, rect, text, font, on_click=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.hover_progress = 0.0  # 0 = not hovered, 1 = fully hovered
        self.last_update = time.time()

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update_hover(self):
        now = time.time()
        dt = min(now - self.last_update, 0.05)  # Clamp for safety
        self.last_update = now
        target = 1.0 if self.is_hovered() else 0.0
        speed = 8.0  # Animation speed (higher = faster)
        self.hover_progress += (target - self.hover_progress) * min(1, speed * dt)

    def draw(self, surface):
        self.update_hover()
        # Animate color
        color = lerp_color(BUTTON_BASE_COLOR, BUTTON_HOVER_COLOR, self.hover_progress)
        # Drop shadow
        shadow_rect = self.rect.move(4, 4)
        shadow_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surf, BUTTON_SHADOW_COLOR, shadow_surf.get_rect(), border_radius=12
        )
        surface.blit(shadow_surf, shadow_rect.topleft)
        # Button face
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(
            surface, BUTTON_BORDER_COLOR, self.rect, width=2, border_radius=12
        )
        text_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """
        Handles mouse button down events and triggers the `on_click` callback if the object is hovered.
        Args:
            event: The pygame event to handle.
        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.is_hovered()
        ):
            # Trigger the on_click callback if set
            if self.on_click:
                self.on_click()
            return True
        return False


class Simulation:
    """
    Simulation class using pygame.
    This class encapsulates the main logic and user interface for the simulation,
    including event handling, physics updates, UI controls, and rendering. It manages
    the game state, user interactions, and draws all visual elements to the screen.

    Usage:
    Instantiate the Simulation class and call the `run()` method to start the simulation.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Window Title")
        self.clock = pygame.time.Clock()

        # Font settings
        self.font = pygame.font.SysFont(None, 22)  # Main font for UI
        self.font_small = pygame.font.SysFont(None, 18)  # Smaller for instructions

        self.paused = False
        self.last_p_state = False  # Track previous pause state for toggle

        self.setup_simulation()

    def reset_simulation(self):
        """
        Reset the simulation to its initial state.
        (Reset dynamic state)
        """
        self.setup_simulation()

    def setup_simulation(self):
        """
        Initializes static objects in the simulation environment.
        """
        self.setup_ui()

    def setup_ui(self):
        """Create UI buttons and interface elements."""
        button_y = (TOP_PANEL_HEIGHT - 30) // 2
        self.pause_button = UIButton(
            (80, button_y, 80, 30), "Pause", self.font, self.toggle_pause
        )  # Pause button
        self.reset_button = UIButton(
            (170, button_y, 80, 30), "Restart", self.font, self.reset_simulation
        )  # Restart button

    def handle_events(self):
        """
        Handles all pygame events, including mouse actions and button interactions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.rect.collidepoint(event.pos):
                    self.reset_simulation()
                elif self.pause_button.rect.collidepoint(event.pos):
                    self.toggle_pause()

    def toggle_pause(self):
        """Toggle the paused state."""
        self.paused = not self.paused
        # Update button text based on pause state
        self.pause_button.text = "Resume" if self.paused else "Pause"

    def game_logic(self):
        """
        Add specific logic for the game, such as physics or game rules.
        """

        def logic_1():
            pass

        def logic_2():
            pass

    def draw(self):
        """
        Render the terrain, control points, and UI elements to the screen.
        """
        self.screen.fill(BACKGROUND_COLOR)  # Fill background

        if self.paused:
            "something"
        else:
            "something else"

        self._draw_ui()  # Draw UI elements
        self._draw_static_objects()  # Draw static objects like bumpers and flippers

        pygame.display.flip()

    def _draw_static_objects(self):
        """
        Draws all static objects in the simulation, such as bumpers and flippers.
        """
        # Placeholder for drawing static objects
        # This method should be implemented to draw bumpers, flippers, etc.
        pass

    def _draw_ui(self):
        """
        Draws the top UI panel, including the pause button, reset button, and instructions.
        """
        # Top panel shadow/depth effect
        shadow = pygame.Surface((WIDTH, 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW_COLOR, shadow.get_rect(), border_radius=8)
        self.screen.blit(shadow, (0, TOP_PANEL_HEIGHT - 6))

        # Top panel
        pygame.draw.rect(
            self.screen, PANEL_COLOR, (0, 0, WIDTH, TOP_PANEL_HEIGHT), border_radius=0
        )
        self.pause_button.draw(self.screen)
        self.reset_button.draw(self.screen)

        # Instruction text
        instruction_text = self.font_small.render(
            "Hold SPACE to launch!" if not self.paused else "Simulation paused",
            True,
            INSTRUCTION_COLOR if not self.paused else PAUSED_STATE_COLOR,
        )
        instruction_rect = instruction_text.get_rect()
        instruction_rect.topleft = (
            self.pause_button.rect.x + 5,
            TOP_PANEL_HEIGHT - 20,
        )
        self.screen.blit(instruction_text, instruction_rect)

    def run(self):
        """Main loop that handles events, updates the display, and maintains a fixed frame rate."""
        while True:
            self.handle_events()  # Handle events
            self.draw()  # Render the simulation
            self.clock.tick(60)


if __name__ == "__main__":
    Simulation().run()
