"""NYC Pizza Delivery Game - Manhattan Grid Drawing."""

import arcade

from constants import (
    AVENUE_WIDTH,
    AVENUES,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    STREET_HEIGHT,
    STREETS,
)


def draw_manhattan_grid():
    """Draw the Manhattan grid."""
    # Draw background (city blocks)
    background_rect = arcade.LRBT(
        MAP_OFFSET_X, MAP_OFFSET_X + MAP_WIDTH, MAP_OFFSET_Y, MAP_OFFSET_Y + MAP_HEIGHT
    )
    arcade.draw_rect_filled(background_rect, arcade.color.LIGHT_GRAY)

    # Draw avenues (vertical streets)
    for i in range(AVENUES + 1):
        x = MAP_OFFSET_X + (i * AVENUE_WIDTH)
        arcade.draw_line(
            x, MAP_OFFSET_Y, x, MAP_OFFSET_Y + MAP_HEIGHT, arcade.color.DARK_GRAY, 3
        )

    # Draw streets (horizontal streets)
    for i in range(STREETS + 1):
        y = MAP_OFFSET_Y + (i * STREET_HEIGHT)
        arcade.draw_line(
            MAP_OFFSET_X, y, MAP_OFFSET_X + MAP_WIDTH, y, arcade.color.DARK_GRAY, 3
        )

    # Draw Hudson River (blue rectangle on the left)
    hudson_rect = arcade.LRBT(0, MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_Y + MAP_HEIGHT)
    arcade.draw_rect_filled(hudson_rect, arcade.color.TEAL_BLUE)

    # Draw East River (blue rectangle on the right)
    east_rect = arcade.LRBT(
        MAP_OFFSET_X + MAP_WIDTH,
        MAP_OFFSET_X + MAP_WIDTH + MAP_OFFSET_X,
        MAP_OFFSET_Y,
        MAP_OFFSET_Y + MAP_HEIGHT,
    )
    arcade.draw_rect_filled(east_rect, arcade.color.TEAL_BLUE)

    # Draw avenue numbers (along the top and bottom)
    for i in range(AVENUES + 1):
        x = MAP_OFFSET_X + (i * AVENUE_WIDTH)
        # Reverse the avenue numbering: 1st Ave on right (east), higher numbers on left (west)
        avenue_num = AVENUES + 1 - i

        # Top labels
        arcade.draw_text(
            f"{avenue_num}st Ave",
            x - 20,
            MAP_OFFSET_Y + MAP_HEIGHT + 5,
            arcade.color.BLACK,
            10,
        )

        # Bottom labels
        arcade.draw_text(
            f"{avenue_num}st Ave", x - 20, MAP_OFFSET_Y - 20, arcade.color.BLACK, 10
        )

    # Draw street numbers (along the left and right sides)
    for i in range(STREETS + 1):
        y = MAP_OFFSET_Y + (i * STREET_HEIGHT)
        # Number streets as multiples of 5 (5th, 10th, 15th, 20th, etc.)
        street_num = (i + 1) * 5

        # Left side labels
        arcade.draw_text(
            f"{street_num}th St", MAP_OFFSET_X - 50, y - 5, arcade.color.BLACK, 10
        )

        # Right side labels
        arcade.draw_text(
            f"{street_num}th St",
            MAP_OFFSET_X + MAP_WIDTH,
            y - 5,
            arcade.color.BLACK,
            10,
        )
