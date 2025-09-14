"""NYC Pizza Delivery Game - Main entry point."""

from typing import Iterable

import arcade

from constants import (
    COLLISION_THRESHOLD,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    PLAYER_SIZE,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
)
from map_layout import (
    draw_manhattan_map,
)
from ui_assets.base_models import Location
from ui_assets.homes import HOMES
from ui_assets.pizza_shops import PIZZA_SHOPS
from ui_assets.special_locations import SPECIAL_LOCATIONS


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


class PizzaDeliveryGame(arcade.Window):
    """Main game class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        # Game objects
        self.score = 0

        self._player = None
        self._pizza_shops = None
        self._homes = None
        self._special_locations = None

    @property
    def player(self) -> arcade.Sprite:
        """Setup the player."""
        if self._player is None:
            self._player = PlayerCharacter()
        return self._player

    @property
    def pizza_shops(self) -> Iterable[Location]:
        """Setup the pizza shops."""
        if self._pizza_shops is None:
            self._pizza_shops = PIZZA_SHOPS
        return self._pizza_shops

    @property
    def homes(self) -> Iterable[Location]:
        """Setup the homes."""
        if self._homes is None:
            self._homes = HOMES
        return self._homes

    @property
    def special_locations(self) -> Iterable[Location]:
        """Setup the special locations."""
        if self._special_locations is None:
            self._special_locations = SPECIAL_LOCATIONS
        return self._special_locations

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw Manhattan map first
        draw_manhattan_map()

        # Draw all sprites
        for location in self.pizza_shops:
            location.draw()
        for location in self.homes:
            location.draw()
        for location in self.special_locations:
            location.draw()

        # Draw player character
        player_list = arcade.SpriteList()
        player_list.append(self.player)
        player_list.draw()

        # Draw UI
        arcade.draw_text(
            f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16
        )

        # Draw map labels
        arcade.draw_text(
            "Manhattan Pizza Delivery",
            MAP_OFFSET_X,
            MAP_OFFSET_Y + MAP_HEIGHT + 20,
            arcade.color.BLACK,
            20,
        )

        # Draw instructions
        if not self.player.has_pizza:
            arcade.draw_text(
                "Go to Joe's Pizza or Papa's Pizza (RED) and press SPACE to pick up pizza!",
                10,
                30,
                arcade.color.BLACK,
                14,
            )
        else:
            arcade.draw_text(
                "Go to GREEN home and press SPACE to deliver pizza!",
                10,
                30,
                arcade.color.BLACK,
                14,
            )

        # Draw controls
        arcade.draw_text(
            "Controls: WASD/Arrow Keys to move, SPACE to pickup/deliver",
            10,
            10,
            arcade.color.BLACK,
            12,
        )

        # Draw pizza indicator
        if self.player.has_pizza:
            arcade.draw_circle_filled(
                self.player.center_x,
                self.player.center_y + 30,
                8,
                arcade.color.YELLOW,
            )

    def on_update(self, delta_time):
        """Movement and game logic."""
        self.player.update(delta_time)

    def handle_space_action(self):
        """Handle space bar action for pizza pickup and dropoff."""
        # Check for pizza pickup using distance-based collision detection
        if not self.player.has_pizza:
            # Check distance to any pizza shop
            for pizza_shop in self.pizza_shops:
                distance = arcade.get_distance_between_sprites(self.player, pizza_shop)
                if distance < COLLISION_THRESHOLD:
                    self.player.has_pizza = True
                    print(f"Pizza picked up from {pizza_shop.address.name}!")
                    break

        # Check for pizza delivery using distance-based collision detection
        elif self.player.has_pizza:
            # Check distance to any home
            for home in self.homes:
                distance = arcade.get_distance_between_sprites(self.player, home)
                if distance < COLLISION_THRESHOLD:
                    self.player.has_pizza = False
                    self.score += 1
                    print(
                        f"Pizza delivered to {home.address.name}! Score: {self.score}"
                    )
                    break

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.move_direction("up")
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.move_direction("down")
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_direction("left")
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_direction("right")
        elif key == arcade.key.SPACE:
            self.handle_space_action()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Stop movement when key is released
        if (
            key == arcade.key.UP
            or key == arcade.key.W
            or key == arcade.key.DOWN
            or key == arcade.key.S
            or key == arcade.key.LEFT
            or key == arcade.key.A
            or key == arcade.key.RIGHT
            or key == arcade.key.D
        ):
            self.player.stop_movement()


def main():
    """Main function."""
    PizzaDeliveryGame()
    arcade.run()


if __name__ == "__main__":
    main()
