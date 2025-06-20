# UI Components for the Pygame Wrapper
import math

import pygame

# Slider Constants
SLIDER_MIN = 1
SLIDER_MAX = 7
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 30
TICK_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (255, 255, 100)
WHITE = (255, 255, 255)
KNOB_COLOR = (180, 180, 180)


class DiscreteSlider:
    """
    A discrete slider UI component for selecting an integer value within a specified range.
    Attributes:
        x (int): The x-coordinate of the slider.
        y (int): The y-coordinate of the slider.
        min_val (int): The minimum value of the slider.
        max_val (int): The maximum value of the slider.
        value (int): The current value of the slider.
        dragging (bool): Indicates if the slider knob is being dragged.
    Methods:
        draw(screen, font): Draws the slider on the given screen with labels and ticks.
        is_over(pos): Checks if a position is over the slider knob or bar.
        update_value(pos): Updates the slider value based on a given position.
    """

    def __init__(self, x, y, min_val=SLIDER_MIN, max_val=SLIDER_MAX, value=3):
        self.x = x
        self.y = y
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.dragging = False

    def draw(self, screen, font):
        """
        Draws the slider, its knob, tick marks, and label on the given Pygame screen.
        Args:
            screen: The Pygame surface to draw on.
            font: The Pygame font object used for rendering text.
        """
        # Modern rounded slider bar
        bar_rect = pygame.Rect(self.x, self.y + SLIDER_HEIGHT // 2 - 4, SLIDER_WIDTH, 8)
        pygame.draw.rect(screen, WHITE, bar_rect, border_radius=8)

        # Slider knob
        knob_x = (
            self.x
            + (self.value - self.min_val) / (self.max_val - self.min_val) * SLIDER_WIDTH
        )
        pygame.draw.circle(
            screen, KNOB_COLOR, (int(knob_x), self.y + SLIDER_HEIGHT // 2), 12
        )

        # Modern rounded ticks
        for i in range(self.min_val, self.max_val + 1):
            tick_x = (
                self.x
                + (i - self.min_val) / (self.max_val - self.min_val) * SLIDER_WIDTH
            )
            tick_rect = pygame.Rect(tick_x - 2, self.y + SLIDER_HEIGHT // 2 - 8, 4, 16)
            pygame.draw.rect(screen, TICK_COLOR, tick_rect, border_radius=2)
            # Highlight the label for the current value
            if i == self.value:
                highlight_font = pygame.font.SysFont("segoi", 26)
                num_text = highlight_font.render(str(i), True, HIGHLIGHT_COLOR)
            else:
                num_text = font.render(str(i), True, WHITE)
            screen.blit(num_text, (tick_x - 5, self.y + SLIDER_HEIGHT + 5))
        label_text = font.render("Quantity of control points", True, WHITE)
        screen.blit(
            label_text, (self.x + SLIDER_WIDTH + 20, self.y + SLIDER_HEIGHT // 2 - 8)
        )

    def is_over(self, pos):
        """
        Check if a given position is over the slider knob or bar.
        Args:
            pos (tuple): The (x, y) position to check.
        Returns:
            bool: True if the position is over the slider knob or bar, False otherwise.
        """
        knob_x = (
            self.x
            + (self.value - self.min_val) / (self.max_val - self.min_val) * SLIDER_WIDTH
        )
        return math.hypot(
            pos[0] - knob_x, pos[1] - (self.y + SLIDER_HEIGHT // 2)
        ) <= 12 or (
            self.x <= pos[0] <= self.x + SLIDER_WIDTH
            and abs(pos[1] - (self.y + SLIDER_HEIGHT // 2)) <= 10
        )

    def update_value(self, pos):
        """
        Update the slider's value based on the given position.
        Args:
            pos (tuple): The (x, y) position to update the value from.
        """

        rel_x = pos[0] - self.x
        t = rel_x / SLIDER_WIDTH
        t = max(0, min(1, t))
        self.value = round(self.min_val + (self.max_val - self.min_val) * t)
