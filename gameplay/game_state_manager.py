from enum import Enum

from constants import (
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
)

# Import ScoreTracker from main module
from gameplay.score_tracker import ScoreTracker
from gameplay.session_manager import SessionManager
from logging_utils import get_logger

# Initialize logger at module level
logger = get_logger(__name__)


class GameState(Enum):
    """Enum representing the current state of the game."""

    NAME_INPUT = "name_input"
    SHOWING_INSTRUCTIONS = "showing_instructions"
    ACTIVE = "active"
    ACTIVE_WITH_OVERLAY = "active_with_overlay"
    SHOWING_LEADERBOARD = "showing_leaderboard"
    GAME_OVER = "game_over"


class GameStateManager:
    """Class responsible for managing game state transitions."""

    def __init__(self, game):
        """Initialize with reference to the main game instance."""
        self.game = game
        self._game_state = GameState.NAME_INPUT
        self.name_input_text = ""
        self._player_name = ""
        self.leaderboard_data = []

        # Initialize session manager
        self.session_manager = SessionManager()

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
    def player_name(self) -> str:
        return self._player_name

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._game_state == GameState.GAME_OVER

    def complete_name_input(self):
        """Complete the name input and show instructions."""
        self._player_name = (
            self.name_input_text.strip()
            if self.name_input_text.strip()
            else "Voldemort"
        )
        self._game_state = GameState.SHOWING_INSTRUCTIONS
        logger.info(f"Welcome, {self.player_name}! Showing game instructions...")

    def start_game_from_instructions(self):
        """Start the game after showing instructions."""
        self._game_state = GameState.ACTIVE
        self.game.game_timer = 0.0  # Reset timer

        # Create a new session in the database
        self.session_manager.create_session(
            self.player_name,
            self.game.score_tracker.earned,
            self.game.score_tracker.spent,
        )

        # Start the game by generating a new order
        self.game.generate_new_order()
        logger.info(f"Let's start delivering pizzas, {self.player_name}!")

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
        self.session_manager.update_session(
            self.game.score_tracker.earned, self.game.score_tracker.spent
        )

        self.game.log_final_score()

    def restart_game(self):
        """Restart the game with the same player name."""
        # Reset game state
        self._game_state = GameState.SHOWING_INSTRUCTIONS
        self.game.score_tracker = ScoreTracker()
        self.game.game_timer = 0.0
        self.game.current_order = None
        self.game.flash_timer = 0.0
        self.game.session_manager.reset_session()  # Reset session ID for new game

        # Reset player position and state
        self.game.player.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.game.player.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.game.player.has_pizza = False
        self.game.player.stop_movement()

        logger.info(f"Game restarted for {self.player_name}! Showing instructions...")

    def show_leaderboard(self):
        """Show the leaderboard overlay."""
        if self.session_manager.api_client:
            try:
                self.leaderboard_data = self.session_manager.api_client.get_leaderboard(
                    limit=10
                )
                self._game_state = GameState.SHOWING_LEADERBOARD
                logger.info("Showing leaderboard")
            except Exception as e:
                logger.error(f"Failed to load leaderboard: {e}")
                # Show empty leaderboard if API fails
                self.leaderboard_data = []
                self._game_state = GameState.SHOWING_LEADERBOARD
        else:
            logger.warning("API client not available - showing empty leaderboard")
            self.leaderboard_data = []
            self._game_state = GameState.SHOWING_LEADERBOARD

    def hide_leaderboard(self):
        """Hide the leaderboard and return to previous state."""
        if self._game_state == GameState.SHOWING_LEADERBOARD:
            # Return to game over state (since leaderboard is only shown from game over now)
            self._game_state = GameState.GAME_OVER
            logger.info("Leaderboard hidden")
