"""Leaderboard dialog for the NYC Pizza Delivery Game."""

from typing import List, Optional

import arcade

from backend.db.models import Session
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_leaderboard_dialog(
    leaderboard: List[Session], current_player_name: Optional[str] = None
):
    """Draw the leaderboard screen overlay."""
    # Dialog box dimensions and positioning
    dialog_width = 600
    dialog_height = 500
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
        "🏆 LEADERBOARD 🏆",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 50,
        arcade.color.GOLD,
        28,
        anchor_x="center",
        anchor_y="center",
        bold=True,
    )

    # Draw column headers
    header_y = dialog_y + dialog_height - 100
    arcade.draw_text(
        "Rank",
        dialog_x + 30,
        header_y,
        arcade.color.BLACK,
        16,
        anchor_x="left",
        anchor_y="center",
        bold=True,
    )
    arcade.draw_text(
        "Player",
        dialog_x + 100,
        header_y,
        arcade.color.BLACK,
        16,
        anchor_x="left",
        anchor_y="center",
        bold=True,
    )
    arcade.draw_text(
        "Net Income",
        dialog_x + 350,
        header_y,
        arcade.color.BLACK,
        16,
        anchor_x="left",
        anchor_y="center",
        bold=True,
    )
    arcade.draw_text(
        "Date",
        dialog_x + 480,
        header_y,
        arcade.color.BLACK,
        16,
        anchor_x="left",
        anchor_y="center",
        bold=True,
    )

    # Draw separator line
    line_y = header_y - 15
    arcade.draw_line(
        dialog_x + 20,
        line_y,
        dialog_x + dialog_width - 20,
        line_y,
        arcade.color.BLACK,
        2,
    )

    # Draw leaderboard entries
    entry_y = header_y - 40
    for i, session in enumerate(leaderboard[:10]):  # Show top 10
        rank = i + 1

        # Highlight current player's entry
        text_color = (
            arcade.color.BLUE
            if current_player_name and session.player_name == current_player_name
            else arcade.color.BLACK
        )
        if rank <= 3:
            # Special colors for top 3
            if rank == 1:
                text_color = arcade.color.GOLD
            elif rank == 2:
                text_color = arcade.color.SILVER
            elif rank == 3:
                text_color = arcade.color.COPPER

        # Draw rank
        rank_text = f"{rank}."
        if rank == 1:
            rank_text = "🥇"
        elif rank == 2:
            rank_text = "🥈"
        elif rank == 3:
            rank_text = "🥉"

        arcade.draw_text(
            rank_text,
            dialog_x + 30,
            entry_y,
            text_color,
            14,
            anchor_x="left",
            anchor_y="center",
            bold=rank <= 3,
        )

        # Draw player name (truncate if too long)
        player_name = session.player_name
        if len(player_name) > 15:
            player_name = player_name[:12] + "..."
        arcade.draw_text(
            player_name,
            dialog_x + 100,
            entry_y,
            text_color,
            14,
            anchor_x="left",
            anchor_y="center",
        )

        # Draw net income
        income_color = (
            arcade.color.GREEN if session.net_income >= 0 else arcade.color.RED
        )
        arcade.draw_text(
            f"${session.net_income:.0f}",
            dialog_x + 350,
            entry_y,
            income_color,
            14,
            anchor_x="left",
            anchor_y="center",
            bold=True,
        )

        # Draw date (format: MM/DD)
        if session.timestamp:
            date_str = session.timestamp.strftime("%m/%d")
        else:
            date_str = "N/A"
        arcade.draw_text(
            date_str,
            dialog_x + 480,
            entry_y,
            text_color,
            12,
            anchor_x="left",
            anchor_y="center",
        )

        entry_y -= 25

    # Draw instructions
    arcade.draw_text(
        "Press L to close leaderboard",
        dialog_x + dialog_width // 2,
        dialog_y + 20,
        arcade.color.BLACK,
        14,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw current player's best score if available
    if current_player_name:
        current_player_sessions = [
            s for s in leaderboard if s.player_name == current_player_name
        ]
        if current_player_sessions:
            best_session = max(current_player_sessions, key=lambda s: s.net_income)
            current_rank = next(
                (
                    i + 1
                    for i, s in enumerate(leaderboard)
                    if s.session_id == best_session.session_id
                ),
                None,
            )

            if current_rank:
                arcade.draw_text(
                    f"Your best: Rank #{current_rank} (${best_session.net_income:.0f})",
                    dialog_x + dialog_width // 2,
                    dialog_y + 50,
                    arcade.color.BLUE,
                    14,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True,
                )
