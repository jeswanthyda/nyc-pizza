"""Name input dialog for the NYC Pizza Delivery Game."""

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_name_input_dialog(name_input_text: str):
    """Draw the name input dialog box overlay."""
    # Dialog box dimensions and positioning
    dialog_width = 400
    dialog_height = 250
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
    title_text = "NYC Pizza Delivery Game"
    arcade.draw_text(
        title_text,
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 50,
        arcade.color.BLACK,
        24,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw instruction
    instruction_text = "Type your name:"
    arcade.draw_text(
        instruction_text,
        dialog_x + dialog_width // 2,
        dialog_y + dialog_height - 100,
        arcade.color.BLACK,
        18,
        anchor_x="center",
        anchor_y="center",
    )

    # Draw input field background
    input_width = 300
    input_height = 40
    input_x = dialog_x + dialog_width // 2 - input_width // 2
    input_y = dialog_y + dialog_height // 2 - 40

    input_rect = arcade.LRBT(
        input_x, input_x + input_width, input_y, input_y + input_height
    )
    arcade.draw_rect_filled(input_rect, arcade.color.LIGHT_GRAY)
    arcade.draw_rect_outline(
        input_rect,
        arcade.color.BLACK,
        border_width=2,
    )

    # Draw current input text
    display_text = name_input_text
    text_color = arcade.color.BLACK

    arcade.draw_text(
        display_text,
        input_x + 10,
        input_y + input_height // 2,
        text_color,
        16,
        anchor_y="center",
    )

    # Draw instructions
    arcade.draw_text(
        "Press ENTER to start",
        dialog_x + dialog_width // 2,
        dialog_y + 30,
        arcade.color.BLACK,
        14,
        anchor_x="center",
        anchor_y="center",
    )
