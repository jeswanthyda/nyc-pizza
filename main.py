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
    SIDEBAR_X,
)
from map_layout import (
    draw_manhattan_map,
)
from orders import Order
from ui_assets.base_models import Location
from ui_assets.final_score_dialog import draw_final_score
from ui_assets.homes import HOMES
from ui_assets.name_input_dialog import draw_name_input_dialog
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
        self.player_name = ""
        self._is_game_active = False
        self.name_input_text = ""

        self._player = None
        self._pizza_shops = None
        self._homes = None
        self._special_locations = None

        # Order management
        self.current_order = None
        self.flash_timer = 0.0

        # Game timer (1 minute = 60 seconds)
        self.game_timer = 0.0
        self.game_duration = 60.0  # 1 minute in seconds
        self._is_game_over = False
        self._is_restart = False

    def complete_name_input(self):
        """Complete the name input and start the game."""
        self.player_name = (
            self.name_input_text.strip() if self.name_input_text.strip() else "Player"
        )
        self._is_game_active = True
        self._is_game_over = False
        self._is_restart = False
        self.game_timer = 0.0  # Reset timer

        # Start the game by generating a new order
        self.generate_new_order()
        print(f"Welcome, {self.player_name}! Let's start delivering pizzas!")

    def end_game(self):
        """End the game and show final score."""
        self._is_game_over = True
        self.log_final_score()

    def restart_game(self):
        """Restart the game and ask for player name again."""
        # Reset game state
        self._is_game_over = False
        self._is_game_active = False
        self._is_restart = True
        self.score = 0
        self.game_timer = 0.0
        self.current_order = None
        self.flash_timer = 0.0

        # Reset player position and state
        self.player.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.player.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.player.has_pizza = False
        self.player.stop_movement()

        # Clear name input to show the name input dialog again
        self.name_input_text = ""

        print("Game restarted! Please enter your name to start a new game.")

    def log_final_score(self):
        """Log the final score with player name."""
        print("\n=== GAME OVER ===")
        print(f"Player: {self.player_name}")
        print(f"Final Score: {self.score}")
        print("================\n")

    @property
    def is_game_active(self) -> bool:
        """Check if the game is active."""
        return self._is_game_active and not self._is_game_over

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._is_game_over

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
        # Don't draw highlights if there's no current order
        if self.current_order is None:
            return

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

    def draw_sidebar(self):
        """Draw the sidebar with game information."""
        # Draw sidebar background
        sidebar_rect = arcade.LRBT(SIDEBAR_X, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_rect_filled(
            sidebar_rect,
            arcade.color.LIGHT_BLUE,
        )

        # Draw sidebar border
        arcade.draw_rect_outline(
            sidebar_rect,
            arcade.color.BLACK,
            border_width=2,
        )

        # Sidebar text positioning
        sidebar_text_x = SIDEBAR_X + 10
        current_y = SCREEN_HEIGHT - 30

        # Draw player name
        arcade.draw_text(
            f"Player: {self.player_name}",
            sidebar_text_x,
            current_y,
            arcade.color.BLACK,
            14,
            bold=True,
        )
        current_y -= 25

        # Draw score
        arcade.draw_text(
            f"Score: {self.score}", sidebar_text_x, current_y, arcade.color.BLACK, 16
        )
        current_y -= 30

        # Draw timer
        remaining_time = max(0, self.game_duration - self.game_timer)
        timer_color = arcade.color.RED if remaining_time < 10 else arcade.color.BLACK
        arcade.draw_text(
            f"Time: {remaining_time:.1f}s", sidebar_text_x, current_y, timer_color, 16
        )
        current_y -= 30

        # Draw current order information
        if self.current_order is not None:
            # Always show order, but alternate colors based on flash_timer
            order_text = "ACTIVE ORDER:"
            arcade.draw_text(
                order_text, sidebar_text_x, current_y, arcade.color.BLACK, 14, bold=True
            )

            should_use_alt_color = (self.flash_timer % 1.0) < 0.5
            pickup_color = (
                arcade.color.RED if should_use_alt_color else arcade.color.ORANGE
            )
            delivery_color = (
                arcade.color.BLUE if should_use_alt_color else arcade.color.CYAN
            )

            current_y -= 20

            pickup_text = (
                f"Pickup from {self.current_order.pickup_location.address.name}"
            )
            arcade.draw_text(pickup_text, sidebar_text_x, current_y, pickup_color, 12)
            current_y -= 15

            pickup_address = (
                f"at {self.current_order.pickup_location.address.avenue_street_address}"
            )
            arcade.draw_text(
                pickup_address, sidebar_text_x, current_y, pickup_color, 12
            )
            current_y -= 20

            delivery_text = f"Deliver to {self.current_order.delivery_location.address.avenue_street_address}"
            arcade.draw_text(
                delivery_text,
                sidebar_text_x,
                current_y,
                delivery_color,
                12,
                bold=True,
            )
        else:
            # Show waiting message when no order is active
            order_text = "WAITING FOR ORDER..."
            arcade.draw_text(
                order_text, sidebar_text_x, current_y, arcade.color.GRAY, 14, bold=True
            )

        # Draw controls
        current_y = MAP_OFFSET_Y
        arcade.draw_text(
            "Controls:", sidebar_text_x, current_y, arcade.color.BLACK, 12, bold=True
        )
        current_y -= 20

        arcade.draw_text(
            "WASD/Arrow Keys to move",
            sidebar_text_x,
            current_y,
            arcade.color.BLACK,
            10,
        )
        current_y -= 15

        arcade.draw_text(
            "SPACE to pickup/deliver",
            sidebar_text_x,
            current_y,
            arcade.color.BLACK,
            10,
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Always draw the game screen first
        self.draw_game_screen()

        # If game is not active, draw the name input dialog on top
        if not self.is_game_active and not self.is_game_over:
            draw_name_input_dialog(self.name_input_text, self._is_restart)
        # If game is over, draw the final score screen
        elif self.is_game_over:
            draw_final_score(self.player_name, self.score)

    def draw_game_screen(self):
        """Draw the normal game screen."""
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

        # Draw sidebar
        self.draw_sidebar()

        # Draw map labels
        arcade.draw_text(
            "Manhattan Pizza Delivery",
            MAP_OFFSET_X,
            MAP_OFFSET_Y + MAP_HEIGHT + 20,
            arcade.color.BLACK,
            20,
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
        if self.is_game_active:
            self.player.update(delta_time)
            # Update flash timer for highlighting effects
            self.flash_timer += delta_time

            # Update game timer
            self.game_timer += delta_time

            # Check if time is up
            if self.game_timer >= self.game_duration:
                self.end_game()

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
        if self.is_game_over:
            # Handle game over screen
            if key == arcade.key.ESCAPE:
                arcade.close_window()
            elif key == arcade.key.R:
                self.restart_game()
        elif not self.is_game_active:
            # Handle name input
            if key == arcade.key.ENTER:
                self.complete_name_input()
            elif key == arcade.key.BACKSPACE:
                if self.name_input_text:
                    self.name_input_text = self.name_input_text[:-1]
            elif key == arcade.key.ESCAPE:
                arcade.close_window()
            else:
                # Add character to input text (only letters, numbers, and spaces)
                char = chr(key) if 32 <= key <= 126 else ""
                if char and len(self.name_input_text) < 20:  # Limit name length
                    self.name_input_text += char
        else:
            # Handle game controls
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
                self.log_final_score()
                arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Stop movement when key is released (only during game, not name input)
        if self.is_game_active:
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
