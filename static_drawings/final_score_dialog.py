"""Final score dialog for the NYC Pizza Delivery Game."""

from typing import List, Optional

import arcade

from backend.db.models import Session
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_final_score(
    player_name: str,
    earned: int,
    spent: int,
    score: int,
    leaderboard: Optional[List[Session]] = None,
    show_leaderboard: bool = False,
):
    """Draw the final score screen overlay."""
    # Dialog box dimensions and positioning
    if show_leaderboard and leaderboard:
        dialog_width = 700
        dialog_height = 500
    else:
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

    # Draw financial breakdown
    arcade.draw_text(
        f"Earned: ${earned}",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 150,
        arcade.color.GREEN,
        18,
        anchor_x="center",
        anchor_y="center",
    )

    arcade.draw_text(
        f"Spent: ${spent}",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 175,
        arcade.color.RED,
        18,
        anchor_x="center",
        anchor_y="center",
    )

    arcade.draw_text(
        f"Net Income: ${score}",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 200,
        arcade.color.BLUE,
        24,
        anchor_x="center",
        anchor_y="center",
        bold=True,
    )

    # Draw leaderboard if requested
    if show_leaderboard and leaderboard:
        _draw_mini_leaderboard(
            dialog_x, dialog_y, dialog_width, dialog_height, leaderboard, player_name
        )

    # Draw instructions
    if show_leaderboard:
        instruction_text = (
            "Press L to hide leaderboard | Press R to restart | ESC to exit"
        )
    else:
        instruction_text = (
            "Press L to show leaderboard | Press R to restart | ESC to exit"
        )

    arcade.draw_text(
        instruction_text,
        dialog_x + dialog_width // 2,
        dialog_y + 30,
        arcade.color.BLACK,
        14,
        anchor_x="center",
        anchor_y="center",
    )


def _draw_mini_leaderboard(
    dialog_x: int,
    dialog_y: int,
    dialog_width: int,
    dialog_height: int,
    leaderboard: List[Session],
    current_player_name: str,
):
    """Draw a mini leaderboard in the final score dialog."""
    # Leaderboard section
    leaderboard_x = dialog_x + 20
    leaderboard_y = dialog_y + dialog_height - 280
    leaderboard_width = dialog_width - 40
    leaderboard_height = 200

    # Draw leaderboard background
    leaderboard_rect = arcade.LRBT(
        leaderboard_x,
        leaderboard_x + leaderboard_width,
        leaderboard_y,
        leaderboard_y + leaderboard_height,
    )
    arcade.draw_rect_filled(leaderboard_rect, (240, 240, 240))  # Light gray background
    arcade.draw_rect_outline(leaderboard_rect, arcade.color.BLACK, border_width=2)

    # Draw leaderboard title
    arcade.draw_text(
        "🏆 TOP SCORES 🏆",
        leaderboard_x + leaderboard_width // 2,
        leaderboard_y + leaderboard_height - 20,
        arcade.color.BLACK,
        16,
        anchor_x="center",
        anchor_y="center",
        bold=True,
    )

    # Draw column headers
    header_y = leaderboard_y + leaderboard_height - 45
    arcade.draw_text(
        "Rank", leaderboard_x + 10, header_y, arcade.color.BLACK, 12, bold=True
    )
    arcade.draw_text(
        "Player", leaderboard_x + 60, header_y, arcade.color.BLACK, 12, bold=True
    )
    arcade.draw_text(
        "Score", leaderboard_x + 200, header_y, arcade.color.BLACK, 12, bold=True
    )

    # Draw separator line
    arcade.draw_line(
        leaderboard_x + 10,
        header_y - 8,
        leaderboard_x + leaderboard_width - 10,
        header_y - 8,
        arcade.color.BLACK,
        1,
    )

    # Draw leaderboard entries (top 5)
    entry_y = header_y - 25
    for i, session in enumerate(leaderboard[:5]):
        rank = i + 1

        # Highlight current player's entry
        text_color = (
            arcade.color.BLUE
            if current_player_name and session.player_name == current_player_name
            else arcade.color.BLACK
        )

        # Special styling for top 3
        if rank == 1:
            rank_text = "🥇"
        elif rank == 2:
            rank_text = "🥈"
        elif rank == 3:
            rank_text = "🥉"
        else:
            rank_text = f"{rank}."

        # Draw rank
        arcade.draw_text(
            rank_text,
            leaderboard_x + 10,
            entry_y,
            text_color,
            12,
            bold=rank <= 3,
        )

        # Draw player name (truncate if too long)
        player_name = session.player_name
        if len(player_name) > 12:
            player_name = player_name[:9] + "..."
        arcade.draw_text(
            player_name,
            leaderboard_x + 60,
            entry_y,
            text_color,
            12,
        )

        # Draw score
        income_color = (
            arcade.color.GREEN if session.net_income >= 0 else arcade.color.RED
        )
        arcade.draw_text(
            f"${session.net_income:.0f}",
            leaderboard_x + 200,
            entry_y,
            income_color,
            12,
            bold=True,
        )

        entry_y -= 20
