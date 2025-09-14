"""Game instructions dialog for the NYC Pizza Delivery Game."""

import arcade

from constants import GAME_DURATION, SCREEN_HEIGHT, SCREEN_WIDTH


def draw_game_instructions_dialog(is_overlay=False):
    """Draw the game instructions dialog box overlay."""
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
        "Game Instructions",
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 40,
        arcade.color.BLACK,
        24,
        bold=True,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw time limit information
    if is_overlay:
        time_text = "Game is PAUSED"
    else:
        time_text = f"You have {GAME_DURATION} seconds to earn as much USD as possible!"

    arcade.draw_text(
        time_text,
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 80,
        arcade.color.RED,
        16,
        bold=True,
        anchor_x="center",
        anchor_y="center",
    )

    # Instructions content
    instructions = [
        "HOW TO PLAY:",
        "",
        "1. Pick up pizzas from highlighted YELLOW locations",
        "2. Deliver them to highlighted CYAN locations",
        "3. Use subways (blue stations) to teleport quickly",
        "4. Each successful delivery earns you +$10 USD",
        "5. Each subway use costs you -$1 USD",
        "",
        "CONTROLS:",
        "• WASD or Arrow Keys: Move your character",
        "• SPACE: Pick up pizza or deliver it",
        "• SPACE at subway: Teleport to nearest destination",
        "",
        "TIPS:",
        "• Subways teleport you to the station closest to your destination",
        "• Watch the timer - when it hits 0, the game ends!",
        "• Complete as many deliveries as possible to earn more USD!",
    ]

    # Draw instructions text
    current_y = dialog_y + dialog_height - 120
    for instruction in instructions:
        if (
            instruction == "HOW TO PLAY:"
            or instruction == "CONTROLS:"
            or instruction == "TIPS:"
        ):
            # Make headers bold
            arcade.draw_text(
                instruction,
                dialog_x + 20,
                current_y,
                arcade.color.BLACK,
                14,
                bold=True,
            )
        elif instruction == "":
            # Empty line for spacing
            pass
        else:
            # Regular instruction text
            arcade.draw_text(
                instruction,
                dialog_x + 20,
                current_y,
                arcade.color.BLACK,
                12,
            )
        current_y -= 18

    # Draw start instruction
    if is_overlay:
        instruction_text = "Press 'i' to hide instructions"
    else:
        instruction_text = "Press ENTER to start the game!"

    arcade.draw_text(
        instruction_text,
        dialog_x + dialog_width // 2,
        dialog_y + 10,
        arcade.color.BLUE,
        16,
        bold=True,
        anchor_x="center",
        anchor_y="bottom",
    )
