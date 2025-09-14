"""NYC Pizza Delivery Game - Player Character Module.

This module contains the PlayerCharacter class that represents the pizza delivery person.
"""

import arcade

from constants import (
    DEFAULT_PLAYER_SPEED,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    PLAYER_SIZE,
)


class PlayerCharacter(arcade.Sprite):
    """Player character - Pizza Delivery Person."""

    def __init__(self):
        super().__init__()
        # Start at center of Manhattan map
        self.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.has_pizza = False

        # Movement properties
        self._speed = DEFAULT_PLAYER_SPEED
        self.change_x = 0
        self.change_y = 0
        self._current_direction = None  # Track current movement direction

        # Load the scooter image and scale it
        self.texture = arcade.load_texture("scooter.png")
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    @property
    def speed(self):
        return self._speed

    def set_speed(self, speed_value):
        """Set the player's speed to a specific value."""
        self._speed = speed_value

    def move_direction(self, direction):
        """Set movement direction. Velocity will be updated continuously based on current speed."""
        self._current_direction = direction
        self._update_velocity_from_direction()

    def stop_movement(self):
        """Stop all movement."""
        self.change_x = 0
        self.change_y = 0
        self._current_direction = None

    def _update_velocity_from_direction(self):
        """Update velocity based on current direction and speed."""
        if self._current_direction == "up":
            self.change_y = self.speed
            self.change_x = 0
        elif self._current_direction == "down":
            self.change_y = -self.speed
            self.change_x = 0
        elif self._current_direction == "left":
            self.change_x = -self.speed
            self.change_y = 0
        elif self._current_direction == "right":
            self.change_x = self.speed
            self.change_y = 0

    def update(self, delta_time=0):
        """Update the delivery person's position with velocity."""
        # Update velocity based on current direction and speed (this ensures speed changes are applied)
        if self._current_direction is not None:
            self._update_velocity_from_direction()

        # Update position based on velocity
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Keep player within Manhattan map boundaries
        min_x = MAP_OFFSET_X
        max_x = MAP_OFFSET_X + MAP_WIDTH
        min_y = MAP_OFFSET_Y
        max_y = MAP_OFFSET_Y + MAP_HEIGHT

        if self.center_x < min_x:
            self.center_x = min_x
            self.change_x = 0
        elif self.center_x > max_x:
            self.center_x = max_x
            self.change_x = 0

        if self.center_y < min_y:
            self.center_y = min_y
            self.change_y = 0
        elif self.center_y > max_y:
            self.center_y = max_y
            self.change_y = 0

    def draw(self):
        """Draw the player character and pizza indicator."""

        # Draw the player sprite
        player_list = arcade.SpriteList()
        player_list.append(self)
        player_list.draw()

        # Draw pizza indicator if player has pizza
        if self.has_pizza:
            arcade.draw_circle_filled(
                self.center_x,
                self.center_y + 30,
                8,
                arcade.color.YELLOW,
            )
