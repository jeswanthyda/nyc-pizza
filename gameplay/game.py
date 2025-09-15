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
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    SIDEBAR_X,
)
from gameplay.game_state_manager import GameState, GameStateManager
from gameplay.orders import Order
from gameplay.player import PlayerCharacter
from gameplay.score_tracker import ScoreTracker
from logging_utils import get_logger
from map_locations import (
    HOMES,
    PIZZA_SHOPS,
    SPEED_MULTIPLIER_LOCATIONS,
    SUBWAYS,
    Location,
)
from static_drawings import (
    draw_final_score,
    draw_game_instructions_dialog,
    draw_leaderboard_dialog,
    draw_manhattan_grid,
    draw_name_input_dialog,
)

# Initialize logger at module level
logger = get_logger(__name__)


class PizzaDeliveryGame(arcade.Window):
    """Main game class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        # Initialize score tracker
        self.score_tracker = ScoreTracker()

        # Initialize game state manager
        self.game_state_manager = GameStateManager(self)

        # Initialize game objects
        self._player = PlayerCharacter()
        self._pizza_shops = PIZZA_SHOPS
        self._homes = HOMES
        self._speed_multipler_locations = SPEED_MULTIPLIER_LOCATIONS
        self._subways = SUBWAYS

        # Order management
        self.current_order = None
        self.flash_timer = 0.0

        # Game timer (1 minute = 60 seconds)
        self.game_timer = 0.0
        self.game_duration = GAME_DURATION

    @property
    def player(self) -> arcade.Sprite:
        """Get the player character."""
        return self._player

    @property
    def player_name(self) -> str:
        """Get the player name."""
        return self.game_state_manager.player_name

    @property
    def pizza_shops(self) -> Iterable[Location]:
        """Get the pizza shops."""
        return self._pizza_shops

    @property
    def homes(self) -> Iterable[Location]:
        """Get the homes."""
        return self._homes

    @property
    def speed_multiplier_locations(self) -> Iterable[Location]:
        """Get the speed multiplier locations."""
        return self._speed_multipler_locations

    @property
    def subways(self) -> Iterable[Location]:
        """Get the subways."""
        return self._subways

    def get_player_speed_multiplier(self):
        """Get the speed multiplier based on player's current location in speed multiplier locations."""
        for location in self._speed_multipler_locations:
            # Check if player sprite collides with location sprite
            if arcade.check_for_collision(self.player, location):
                return location.player_speed_multiplier

        # Default multiplier if not in any speed multiplier location
        return 1.0

    def update_player_speed(self):
        """Update player speed based on current location."""
        multiplier = self.get_player_speed_multiplier()
        new_speed = DEFAULT_PLAYER_SPEED * multiplier
        self.player.set_speed(new_speed)
        # Note: The player's update() method will automatically recalculate velocity
        # based on the new speed if the player is currently moving

    def log_final_score(self):
        """Log the final score with player name."""
        logger.info("=== GAME OVER ===")
        logger.info(f"Player: {self.player_name}")
        logger.info(f"Earned: ${self.score_tracker.earned}")
        logger.info(f"Spent: ${self.score_tracker.spent}")
        logger.info(f"Net Income: ${self.score_tracker.score}")
        logger.info(f"Subway Usage: {self.score_tracker.subway_usage_count} times")
        logger.info("================")

    def generate_new_order(self):
        """Generate a new order and make it the current order."""
        self.current_order = Order.generate_order()
        logger.info(
            f"New order: Pickup from {self.current_order.pickup_location.name} at {self.current_order.pickup_location.avenue_street_address}, deliver to {self.current_order.delivery_location.avenue_street_address}"
        )

    def get_current_destination_location(self, is_pickup: bool = True) -> Location:
        """Get the current pickup or delivery location for highlighting."""
        return (
            self.current_order.pickup_location
            if is_pickup
            else self.current_order.delivery_location
        )

    def draw_order_highlights(self):
        """Draw highlighting for current order pickup and delivery locations."""
        # Don't draw highlights if there's no current order
        if self.current_order is None:
            return

        # Check if we should show highlights (flash effect)
        should_highlight = (self.flash_timer % 1.0) < 0.5

        if should_highlight:
            # Use single color for highlighting
            highlight_color = arcade.color.MAGENTA

            if not self.player.has_pizza:
                # Player doesn't have pizza - highlight pickup location only
                location = self.get_current_destination_location(is_pickup=True)
                arcade.draw_rect_outline(
                    location.arcade_rect, highlight_color, border_width=8
                )
            else:
                # Player has pizza - highlight delivery location only
                location = self.get_current_destination_location(is_pickup=False)
                arcade.draw_rect_outline(
                    location.arcade_rect, highlight_color, border_width=8
                )

    def _draw_sidebar_background(self):
        """Draw the sidebar background and border."""
        sidebar_rect = arcade.LRBT(SIDEBAR_X, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_rect_filled(sidebar_rect, arcade.color.LIGHT_BLUE)
        arcade.draw_rect_outline(sidebar_rect, arcade.color.BLACK, border_width=2)

    def _draw_sidebar_text(
        self, text: str, x: int, y: int, color, size: int = 14, bold: bool = False
    ) -> int:
        """Draw text in sidebar and return new y position."""
        arcade.draw_text(text, x, y, color, size, bold=bold)
        return y - (25 if bold else 20)

    def draw_game_screen(self):
        """Draw the normal game screen."""
        # Draw Manhattan map first
        draw_manhattan_grid()

        # Draw all sprites with highlighting
        for location in self.pizza_shops:
            location.draw()
        for location in self.homes:
            location.draw()
        for location in self.speed_multiplier_locations:
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

    def draw_sidebar(self):
        """Draw the sidebar with game information."""
        self._draw_sidebar_background()

        # Sidebar text positioning
        sidebar_text_x = SIDEBAR_X + 10
        current_y = SCREEN_HEIGHT - 30

        # Draw player and financial information
        current_y = self._draw_sidebar_text(
            f"Player: {self.player_name}",
            sidebar_text_x,
            current_y,
            arcade.color.BLACK,
            14,
            bold=True,
        )
        current_y = self._draw_sidebar_text(
            f"Earned: ${self.score_tracker.earned}",
            sidebar_text_x,
            current_y,
            arcade.color.GREEN,
        )
        current_y = self._draw_sidebar_text(
            f"Spent: ${self.score_tracker.spent}",
            sidebar_text_x,
            current_y,
            arcade.color.RED,
        )
        current_y = self._draw_sidebar_text(
            f"Net Income: ${self.score_tracker.score}",
            sidebar_text_x,
            current_y,
            arcade.color.BLUE,
            16,
            bold=True,
        )
        current_y -= 5  # Extra spacing

        # Draw timer
        remaining_time = max(0, self.game_duration - self.game_timer)
        timer_color = arcade.color.RED if remaining_time < 10 else arcade.color.BLACK
        current_y = self._draw_sidebar_text(
            f"Time: {remaining_time:.1f}s", sidebar_text_x, current_y, timer_color, 16
        )
        current_y -= 5  # Extra spacing

        # Draw current order information
        if self.current_order is not None:
            current_y = self.current_order.draw_order_info(
                sidebar_text_x, current_y, self.flash_timer
            )

        # Draw controls
        current_y = MAP_OFFSET_Y
        current_y = self._draw_sidebar_text(
            "Controls:", sidebar_text_x, current_y, arcade.color.BLACK, 12, bold=True
        )

        control_texts = [
            "WASD/Arrow Keys to move",
            "SPACE to pickup/deliver",
            "SPACE at subway to teleport",
            "I to show/hide instructions",
        ]

        for text in control_texts:
            current_y = self._draw_sidebar_text(
                text, sidebar_text_x, current_y, arcade.color.BLACK, 10
            )
            current_y += 5  # Less spacing for controls

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Always draw the game screen first
        self.draw_game_screen()

        # Draw state-specific overlays
        if self.game_state_manager.game_state == GameState.NAME_INPUT:
            draw_name_input_dialog(self.game_state_manager.name_input_text)
        elif self.game_state_manager.game_state == GameState.SHOWING_INSTRUCTIONS:
            draw_game_instructions_dialog()
        elif self.game_state_manager.game_state == GameState.GAME_OVER:
            draw_final_score(
                self.player_name,
                self.score_tracker.earned,
                self.score_tracker.spent,
                self.score_tracker.score,
            )
        elif self.game_state_manager.game_state == GameState.ACTIVE_WITH_OVERLAY:
            draw_game_instructions_dialog(is_overlay=True)
        elif self.game_state_manager.game_state == GameState.SHOWING_LEADERBOARD:
            draw_leaderboard_dialog(
                self.game_state_manager.leaderboard_data, self.player_name
            )

    def on_update(self, delta_time):
        """Movement and game logic."""
        if self.game_state_manager.game_state == GameState.ACTIVE:
            # Update player speed based on speed multiplier locations
            self.update_player_speed()

            self.player.update(delta_time)
            # Update flash timer for highlighting effects
            self.flash_timer += delta_time

            # Update game timer
            self.game_timer += delta_time

            # Check if time is up
            if self.game_timer >= self.game_duration:
                self.game_state_manager.end_game()

    def handle_space_action(self):
        """Handle space bar action for pizza pickup, dropoff, and subway teleportation."""

        # Check for pizza pickup using distance-based collision detection
        if not self.player.has_pizza:
            # Only allow pickup from the current order's pickup location
            location = self.get_current_destination_location(is_pickup=True)
            distance = arcade.get_distance_between_sprites(self.player, location)
            if distance < COLLISION_THRESHOLD:
                self.player.has_pizza = True
                logger.info(f"Pizza picked up from {location.name}!")
                return

        # Check for pizza delivery using distance-based collision detection
        elif self.player.has_pizza:
            # Only allow delivery to the current order's delivery location
            location = self.get_current_destination_location(is_pickup=False)
            distance = arcade.get_distance_between_sprites(self.player, location)
            if distance < COLLISION_THRESHOLD:
                self.player.has_pizza = False
                self.score_tracker.earn_money(10)  # +$10 per pizza delivery
                logger.info(
                    f"Pizza delivered to {location.avenue_street_address}! Earned: ${self.score_tracker.earned}, Net: ${self.score_tracker.score}"
                )
                # Complete the current order and immediately generate a new one
                self.current_order = None
                self.generate_new_order()
                return

        # Check for subway interaction at last
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
            logger.warning(
                "No active order - can't determine destination for subway teleportation!"
            )
            return
        destination = self.get_current_destination_location(
            is_pickup=not self.player.has_pizza
        )
        closest_subway = self.find_closest_subway_to_destination(destination)

        # Teleport player to the closest subway near the destination
        self.player.center_x = closest_subway.center_x
        self.player.center_y = closest_subway.center_y

        # Deduct $1 for subway usage
        self.score_tracker.use_subway()

        logger.info(
            f"Teleported to subway at {closest_subway.avenue_street_address} (closest to destination)! Spent: ${self.score_tracker.spent}, Net: ${self.score_tracker.score}"
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # Common keys that work in all states
        if key == arcade.key.ESCAPE:
            self.game_state_manager.session_manager.cleanup()
            arcade.close_window()
            return

        # State-specific key handling
        if self.game_state_manager.is_game_over:
            self._handle_game_over_key(key)
        elif self.game_state_manager.game_state == GameState.SHOWING_LEADERBOARD:
            self._handle_leaderboard_key(key)
        elif not self.game_state_manager.is_game_active:
            self._handle_menu_key(key)
        else:
            self._handle_game_key(key)

    def _handle_game_over_key(self, key):
        """Handle keys when game is over."""
        if key == arcade.key.R:
            self.game_state_manager.restart_game()
        elif key == arcade.key.L:
            self.game_state_manager.show_leaderboard()

    def _handle_leaderboard_key(self, key):
        """Handle keys when showing leaderboard."""
        if key == arcade.key.L:
            self.game_state_manager.hide_leaderboard()

    def _handle_menu_key(self, key):
        """Handle keys in menu states."""
        if self.game_state_manager.game_state == GameState.SHOWING_INSTRUCTIONS:
            if key == arcade.key.ENTER:
                self.game_state_manager.start_game_from_instructions()
        elif self.game_state_manager.game_state == GameState.NAME_INPUT:
            if key == arcade.key.ENTER:
                self.game_state_manager.complete_name_input()
            elif key == arcade.key.BACKSPACE:
                if self.game_state_manager.name_input_text:
                    self.game_state_manager.name_input_text = (
                        self.game_state_manager.name_input_text[:-1]
                    )
            else:
                # Add character to input text (only letters, numbers, and spaces)
                char = chr(key) if 32 <= key <= 126 else ""
                if (
                    char and len(self.game_state_manager.name_input_text) < 20
                ):  # Limit name length
                    self.game_state_manager.name_input_text += char

    def _handle_game_key(self, key):
        """Handle keys during active gameplay."""
        if key == arcade.key.I:
            self.game_state_manager.toggle_instructions_overlay()
        elif key == arcade.key.ESCAPE:
            self.log_final_score()
        # Only allow movement and actions if not showing instructions overlay
        elif self.game_state_manager.game_state == GameState.ACTIVE:
            self._handle_movement_key(key)

    def _handle_movement_key(self, key):
        """Handle movement and action keys."""
        movement_map = {
            arcade.key.UP: "up",
            arcade.key.W: "up",
            arcade.key.DOWN: "down",
            arcade.key.S: "down",
            arcade.key.LEFT: "left",
            arcade.key.A: "left",
            arcade.key.RIGHT: "right",
            arcade.key.D: "right",
        }

        if key in movement_map:
            self.player.move_direction(movement_map[key])
        elif key == arcade.key.SPACE:
            self.handle_space_action()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Stop movement when key is released (only during active gameplay)
        if self.game_state_manager.game_state == GameState.ACTIVE:
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
