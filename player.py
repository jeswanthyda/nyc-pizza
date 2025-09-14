"""NYC Pizza Delivery Game - Player Character Module.

This module contains the PlayerCharacter class that represents the pizza delivery person.
"""

import arcade

from constants import (
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    PLAYER_SIZE,
    PLAYER_SPEED,
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
        self.speed = PLAYER_SPEED
        self.change_x = 0
        self.change_y = 0

        # Load the scooter image and scale it
        self.texture = arcade.load_texture("scooter.png")
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    def move_direction(self, direction):
        """Set movement velocity in the specified direction."""
        if direction == "up":
            self.change_y = self.speed
            self.change_x = 0
        elif direction == "down":
            self.change_y = -self.speed
            self.change_x = 0
        elif direction == "left":
            self.change_x = -self.speed
            self.change_y = 0
        elif direction == "right":
            self.change_x = self.speed
            self.change_y = 0

    def stop_movement(self):
        """Stop all movement."""
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time=0):
        """Update the delivery person's position with velocity."""
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
