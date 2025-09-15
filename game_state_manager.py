from enum import Enum

from constants import (
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
)
from logging_utils import get_logger

# Initialize logger at module level
logger = get_logger(__name__)


class GameState(Enum):
    """Enum representing the current state of the game."""

    NAME_INPUT = "name_input"
    SHOWING_INSTRUCTIONS = "showing_instructions"
    ACTIVE = "active"
    ACTIVE_WITH_OVERLAY = "active_with_overlay"
    GAME_OVER = "game_over"


class GameStateManager:
    """Class responsible for managing game state transitions."""

    def __init__(self, game):
        """Initialize with reference to the main game instance."""
        self.game = game
        self._game_state = GameState.NAME_INPUT

    @property
    def game_state(self):
        return self._game_state

    @property
    def is_game_active(self) -> bool:
        """Check if the game is active."""
        return self._game_state in [
            GameState.ACTIVE,
            GameState.ACTIVE_WITH_OVERLAY,
        ]

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._game_state == GameState.GAME_OVER

    def complete_name_input(self):
        """Complete the name input and show instructions."""
        self.game.player_name = (
            self.game.name_input_text.strip()
            if self.game.name_input_text.strip()
            else "Voldemort"
        )
        self._game_state = GameState.SHOWING_INSTRUCTIONS
        logger.info(f"Welcome, {self.game.player_name}! Showing game instructions...")

    def start_game_from_instructions(self):
        """Start the game after showing instructions."""
        self._game_state = GameState.ACTIVE
        self.game.game_timer = 0.0  # Reset timer

        # Create a new session in the database
        self.game.session_manager.create_session(
            self.game.player_name, self.game.earned, self.game.spent
        )

        # Start the game by generating a new order
        self.game.generate_new_order()
        logger.info(f"Let's start delivering pizzas, {self.game.player_name}!")

    def toggle_instructions_overlay(self):
        """Toggle the instructions overlay during gameplay."""
        if self._game_state == GameState.ACTIVE_WITH_OVERLAY:
            self._game_state = GameState.ACTIVE
            logger.info("Instructions hidden")
        else:
            self._game_state = GameState.ACTIVE_WITH_OVERLAY
            # Stop player movement when showing instructions
            self.game.player.stop_movement()
            logger.info("Instructions shown - press 'i' again to hide")

    def end_game(self):
        """End the game and show final score."""
        self._game_state = GameState.GAME_OVER

        # Update the session with final scores
        self.game.session_manager.update_session(self.game.earned, self.game.spent)

        self.game.log_final_score()

    def restart_game(self):
        """Restart the game with the same player name."""
        # Reset game state
        self._game_state = GameState.SHOWING_INSTRUCTIONS
        self.game.score = 0
        self.game.earned = 0
        self.game.spent = 0
        self.game.subway_usage_count = 0
        self.game.game_timer = 0.0
        self.game.current_order = None
        self.game.flash_timer = 0.0
        self.game.session_manager.reset_session()  # Reset session ID for new game

        # Reset player position and state
        self.game.player.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.game.player.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.game.player.has_pizza = False
        self.game.player.stop_movement()

        logger.info(
            f"Game restarted for {self.game.player_name}! Showing instructions..."
        )
