"""NYC Pizza Delivery Game - Main entry point."""

from typing import Iterable

import arcade

from constants import (
    COLLISION_THRESHOLD,
    DEFAULT_PLAYER_SPEED,
    GAME_DURATION,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    SIDEBAR_X,
)
from map_layout import (
    draw_manhattan_map,
)
from orders import Order
from player import PlayerCharacter
from ui_assets.base_models import Location
from ui_assets.final_score_dialog import draw_final_score
from ui_assets.game_instructions_dialog import draw_game_instructions_dialog
from ui_assets.homes import HOMES
from ui_assets.name_input_dialog import draw_name_input_dialog
from ui_assets.pizza_shops import PIZZA_SHOPS
from ui_assets.special_locations import SPECIAL_LOCATIONS
from ui_assets.subways import SUBWAYS


class PizzaDeliveryGame(arcade.Window):
    """Main game class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        # Game objects
        self.score = 0  # Net income (earned - spent)
        self.earned = 0  # Money earned from pizza deliveries
        self.spent = 0  # Money spent on subway usage
        self.subway_usage_count = 0  # Track subway usage for cost calculation
        self.player_name = ""
        self._is_game_active = False
        self._show_instructions = False
        self._show_instructions_overlay = False
        self.name_input_text = ""

        # Initialize game objects
        self._player = PlayerCharacter()
        self._pizza_shops = PIZZA_SHOPS
        self._homes = HOMES
        self._special_locations = SPECIAL_LOCATIONS
        self._subways = SUBWAYS

        # Order management
        self.current_order = None
        self.flash_timer = 0.0

        # Game timer (1 minute = 60 seconds)
        self.game_timer = 0.0
        self.game_duration = GAME_DURATION
        self._is_game_over = False

    def complete_name_input(self):
        """Complete the name input and show instructions."""
        self.player_name = (
            self.name_input_text.strip() if self.name_input_text.strip() else "Player"
        )
        self._show_instructions = True
        print(f"Welcome, {self.player_name}! Showing game instructions...")

    def start_game_from_instructions(self):
        """Start the game after showing instructions."""
        self._show_instructions = False
        self._is_game_active = True
        self._is_game_over = False
        self.game_timer = 0.0  # Reset timer

        # Start the game by generating a new order
        self.generate_new_order()
        print(f"Let's start delivering pizzas, {self.player_name}!")

    def toggle_instructions_overlay(self):
        """Toggle the instructions overlay during gameplay."""
        self._show_instructions_overlay = not self._show_instructions_overlay
        if self._show_instructions_overlay:
            # Stop player movement when showing instructions
            self.player.stop_movement()
            print("Instructions shown - press 'i' again to hide")
        else:
            print("Instructions hidden")

    def get_player_speed_multiplier(self):
        """Get the speed multiplier based on player's current location in special locations."""
        for location in self._special_locations:
            # Check if player sprite collides with location sprite
            if arcade.check_for_collision(self.player, location):
                return location.player_speed_multiplier

        # Default multiplier if not in any special location
        return 1.0

    def update_player_speed(self):
        """Update player speed based on current location."""
        multiplier = self.get_player_speed_multiplier()
        new_speed = DEFAULT_PLAYER_SPEED * multiplier
        self.player.set_speed(new_speed)
        # Note: The player's update() method will automatically recalculate velocity
        # based on the new speed if the player is currently moving

    def end_game(self):
        """End the game and show final score."""
        self._is_game_over = True
        self.log_final_score()

    def restart_game(self):
        """Restart the game with the same player name."""
        # Reset game state
        self._is_game_over = False
        self._is_game_active = False
        self._show_instructions = False
        self._show_instructions_overlay = False
        self.score = 0
        self.earned = 0
        self.spent = 0
        self.subway_usage_count = 0
        self.game_timer = 0.0
        self.current_order = None
        self.flash_timer = 0.0

        # Reset player position and state
        self.player.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.player.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.player.has_pizza = False
        self.player.stop_movement()

        # Go directly to showing instructions
        self._show_instructions = True

        print(f"Game restarted for {self.player_name}! Showing instructions...")

    def log_final_score(self):
        """Log the final score with player name."""
        print("\n=== GAME OVER ===")
        print(f"Player: {self.player_name}")
        print(f"Earned: ${self.earned} USD")
        print(f"Spent: ${self.spent} USD")
        print(f"Net Income: ${self.score} USD")
        print(f"Subway Usage: {self.subway_usage_count} times")
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
        """Get the player character."""
        return self._player

    @property
    def pizza_shops(self) -> Iterable[Location]:
        """Get the pizza shops."""
        return self._pizza_shops

    @property
    def homes(self) -> Iterable[Location]:
        """Get the homes."""
        return self._homes

    @property
    def special_locations(self) -> Iterable[Location]:
        """Get the special locations."""
        return self._special_locations

    @property
    def subways(self) -> Iterable[Location]:
        """Get the subways."""
        return self._subways

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

        # Draw financial information
        arcade.draw_text(
            f"Earned: ${self.earned} USD",
            sidebar_text_x,
            current_y,
            arcade.color.GREEN,
            14,
        )
        current_y -= 20

        arcade.draw_text(
            f"Spent: ${self.spent} USD",
            sidebar_text_x,
            current_y,
            arcade.color.RED,
            14,
        )
        current_y -= 20

        arcade.draw_text(
            f"Net Income: ${self.score} USD",
            sidebar_text_x,
            current_y,
            arcade.color.BLUE,
            16,
            bold=True,
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
            current_y = self.current_order.draw_order_info(
                sidebar_text_x, current_y, self.flash_timer
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
        current_y -= 15

        arcade.draw_text(
            "SPACE at subway to teleport",
            sidebar_text_x,
            current_y,
            arcade.color.BLACK,
            10,
        )
        current_y -= 15

        arcade.draw_text(
            "I to show/hide instructions",
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
        if (
            not self.is_game_active
            and not self.is_game_over
            and not self._show_instructions
        ):
            draw_name_input_dialog(self.name_input_text)
        # If showing instructions, draw the instructions dialog
        elif self._show_instructions:
            draw_game_instructions_dialog()
        # If game is over, draw the final score screen
        elif self.is_game_over:
            draw_final_score(self.player_name, self.earned, self.spent, self.score)

        # If showing instructions overlay during active gameplay, draw it on top
        if self._show_instructions_overlay and self.is_game_active:
            draw_game_instructions_dialog(is_overlay=True)

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
        for location in self.subways:
            location.draw()

        # Draw highlighting for current order locations
        self.draw_order_highlights()

        # Draw player character
        self.player.draw()

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

    def on_update(self, delta_time):
        """Movement and game logic."""
        if self.is_game_active:
            # Only update game logic if instructions overlay is not shown
            if not self._show_instructions_overlay:
                # Update player speed based on special locations
                self.update_player_speed()

                self.player.update(delta_time)
                # Update flash timer for highlighting effects
                self.flash_timer += delta_time

                # Update game timer
                self.game_timer += delta_time

                # Check if time is up
                if self.game_timer >= self.game_duration:
                    self.end_game()

    def handle_space_action(self):
        """Handle space bar action for pizza pickup, dropoff, and subway teleportation."""

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
                self.earned += 10  # +10 USD per pizza delivery
                self.score = self.earned - self.spent  # Update net income
                print(
                    f"Pizza delivered to {delivery_location.address.avenue_street_address}! Earned: ${self.earned}, Net: ${self.score} USD"
                )
                # Complete the current order and immediately generate a new one
                self.current_order = None
                self.generate_new_order()
                return

        # Check for subway interaction first (available at any time)
        for subway in self.subways:
            distance = arcade.get_distance_between_sprites(self.player, subway)
            if distance < COLLISION_THRESHOLD:
                self.handle_subway_teleportation()
                return

    def find_closest_subway_to_destination(
        self, destination: Location
    ) -> Location | None:
        """Find the subway station closest to the given destination."""

        min_distance = float("inf")
        closest_subway = None

        for subway in self.subways:
            distance = arcade.get_distance_between_sprites(subway, destination)
            if distance < min_distance:
                min_distance = distance
                closest_subway = subway

        return closest_subway

    def handle_subway_teleportation(self):
        """Handle subway teleportation to the closest subway near the destination."""
        if self.current_order is None:
            print(
                "No active order - can't determine destination for subway teleportation!"
            )
            return
        if self.player.has_pizza:
            destination = self.get_current_delivery_location()
        else:
            destination = self.get_current_pickup_location()
        closest_subway = self.find_closest_subway_to_destination(destination)

        # Teleport player to the closest subway near the destination
        self.player.center_x = closest_subway.center_x
        self.player.center_y = closest_subway.center_y

        # Deduct 1 USD for subway usage
        self.spent += 1
        self.score = self.earned - self.spent  # Update net income
        self.subway_usage_count += 1

        print(
            f"Teleported to subway at {closest_subway.address.avenue_street_address} (closest to destination)! Spent: ${self.spent}, Net: ${self.score} USD"
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if self.is_game_over:
            self._handle_game_over_keys(key)
        elif not self.is_game_active:
            self._handle_menu_keys(key)
        else:
            self._handle_game_keys(key)

    def _handle_game_over_keys(self, key):
        """Handle keys when game is over."""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.R:
            self.restart_game()

    def _handle_menu_keys(self, key):
        """Handle keys in menu states."""
        if self._show_instructions:
            if key == arcade.key.ENTER:
                self.start_game_from_instructions()
            elif key == arcade.key.ESCAPE:
                arcade.close_window()
        else:
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

    def _handle_game_keys(self, key):
        """Handle keys during active gameplay."""
        if key == arcade.key.I:
            self.toggle_instructions_overlay()
        elif key == arcade.key.ESCAPE:
            self.log_final_score()
            arcade.close_window()
        # Only allow movement and actions if instructions overlay is not shown
        elif not self._show_instructions_overlay:
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

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Stop movement when key is released (only during game, not name input, and not when instructions are shown)
        if self.is_game_active and not self._show_instructions_overlay:
            movement_keys = [
                arcade.key.UP,
                arcade.key.W,
                arcade.key.DOWN,
                arcade.key.S,
                arcade.key.LEFT,
                arcade.key.A,
                arcade.key.RIGHT,
                arcade.key.D,
            ]
            if key in movement_keys:
                self.player.stop_movement()


def main():
    """Main function."""
    PizzaDeliveryGame()
    arcade.run()


if __name__ == "__main__":
    main()
