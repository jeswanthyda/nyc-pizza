"""Final score dialog for the NYC Pizza Delivery Game."""

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_final_score(player_name: str, score: int):
    """Draw the final score screen overlay."""
    # Dialog box dimensions and positioning
    dialog_width = 500
    dialog_height = 300
    dialog_x = SCREEN_WIDTH // 2 - dialog_width // 2
    dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2

    # Draw semi-transparent overlay background
    overlay_rect = arcade.LRBT(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    arcade.draw_rect_filled(overlay_rect, (0, 0, 0, 128))  # Semi-transparent black

    # Draw dialog box background
    dialog_rect = arcade.LRBT(
        dialog_x, dialog_x + dialog_width, dialog_y, dialog_y + dialog_height
    )
    arcade.draw_rect_filled(dialog_rect, arcade.color.WHITE)

    # Draw dialog box border
    arcade.draw_rect_outline(
        dialog_rect,
        arcade.color.BLACK,
        border_width=3,
    )

    # Draw title
    arcade.draw_text(
        "GAME OVER!",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 60,
        arcade.color.RED,
        32,
        anchor_x="center",
        anchor_y="center",
        bold=True,
    )

    # Draw player name
    arcade.draw_text(
        f"Player: {player_name}",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 120,
        arcade.color.BLACK,
        20,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw final score
    arcade.draw_text(
        f"Final Score: {score}",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 160,
        arcade.color.BLUE,
        24,
        anchor_x="center",
        anchor_y="center",
        bold=True,
    )

    # Draw time message
    arcade.draw_text(
        "Time's up!",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 200,
        arcade.color.GRAY,
        16,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw instructions
    arcade.draw_text(
        "Press R to restart or ESC to exit",
        dialog_x + dialog_width // 2,
        dialog_y + 30,
        arcade.color.BLACK,
        14,
        anchor_x="center",
        anchor_y="center",
    )
