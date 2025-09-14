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
from orders import Order
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

        # Order management
        self.current_order = None
        self.flash_timer = 0.0

        # Generate the first order immediately
        self.generate_new_order()

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

    def generate_new_order(self):
        """Generate a new order and make it the current order."""
        self.current_order = Order.generate_order()
        print(
            f"New order: Pickup from {self.current_order.pickup_location.address.name} at {self.current_order.pickup_location.address.avenue_street_address}, deliver to {self.current_order.delivery_location.address.avenue_street_address}"
        )

    def get_current_pickup_location(self) -> Location:
        """Get the current pickup location for highlighting."""
        return self.current_order.pickup_location

    def get_current_delivery_location(self) -> Location:
        """Get the current delivery location for highlighting."""
        return self.current_order.delivery_location

    def draw_order_highlights(self):
        """Draw highlighting for current order pickup and delivery locations."""
        # Check if we should show highlights (flash effect)
        should_highlight = (self.flash_timer % 1.0) < 0.5

        if should_highlight:
            # Highlight pickup location
            pickup_location = self.get_current_pickup_location()
            # Draw a bright yellow border around the pickup location
            arcade.draw_rect_outline(
                pickup_location.rectangle, arcade.color.YELLOW, border_width=4
            )

            # Highlight delivery location
            delivery_location = self.get_current_delivery_location()
            # Draw a bright cyan border around the delivery location
            arcade.draw_rect_outline(
                delivery_location.rectangle, arcade.color.CYAN, border_width=4
            )

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw Manhattan map first
        draw_manhattan_map()

        # Draw all sprites with highlighting
        for location in self.pizza_shops:
            location.draw()
        for location in self.homes:
            location.draw()
        for location in self.special_locations:
            location.draw()

        # Draw highlighting for current order locations
        self.draw_order_highlights()

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

        # Draw current order information
        # Flash the order text continuously while order is active
        should_show_order = (self.flash_timer % 1.0) < 0.5

        if should_show_order:
            order_text = f"ACTIVE ORDER: Pickup from {self.current_order.pickup_location.address.name} at {self.current_order.pickup_location.address.avenue_street_address}"
            arcade.draw_text(
                order_text, 10, SCREEN_HEIGHT - 60, arcade.color.RED, 16, bold=True
            )
            delivery_text = f"Deliver to {self.current_order.delivery_location.address.avenue_street_address}"
            arcade.draw_text(
                delivery_text,
                10,
                SCREEN_HEIGHT - 80,
                arcade.color.BLUE,
                16,
                bold=True,
            )

        # Draw instructions
        if not self.player.has_pizza:
            pickup_location = self.get_current_pickup_location()
            arcade.draw_text(
                f"CURRENT ORDER: Go to {pickup_location.address.name} (YELLOW HIGHLIGHT) and press SPACE to pick up pizza!",
                10,
                30,
                arcade.color.BLACK,
                14,
            )
        else:
            arcade.draw_text(
                "CURRENT ORDER: Go to the CYAN highlighted home and press SPACE to deliver pizza!",
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

        # Update flash timer for highlighting effects
        self.flash_timer += delta_time

    def handle_space_action(self):
        """Handle space bar action for pizza pickup and dropoff."""
        # Check for pizza pickup using distance-based collision detection
        if not self.player.has_pizza:
            # Only allow pickup from the current order's pickup location
            pickup_location = self.get_current_pickup_location()
            distance = arcade.get_distance_between_sprites(self.player, pickup_location)
            if distance < COLLISION_THRESHOLD:
                self.player.has_pizza = True
                print(f"Pizza picked up from {pickup_location.address.name}!")
                return

        # Check for pizza delivery using distance-based collision detection
        elif self.player.has_pizza:
            # Only allow delivery to the current order's delivery location
            delivery_location = self.get_current_delivery_location()
            distance = arcade.get_distance_between_sprites(
                self.player, delivery_location
            )
            if distance < COLLISION_THRESHOLD:
                self.player.has_pizza = False
                self.score += 1
                print(
                    f"Pizza delivered to {delivery_location.address.avenue_street_address}! Score: {self.score}"
                )
                # Complete the current order and immediately generate a new one
                self.current_order = None
                self.generate_new_order()
                return

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
