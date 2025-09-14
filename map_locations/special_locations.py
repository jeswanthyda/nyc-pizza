import arcade

from map_locations.base_models import Address, Location

__all__ = ["SPECIAL_LOCATIONS"]


class CentralPark(Location):
    """Central Park location in Manhattan."""

    def __init__(self):
        super().__init__(
            address=Address(5, 60, "Central Park", 3, 50),
        )

    @property
    def player_speed_multiplier(self):
        return 2

    def draw(self):
        arcade.draw_rect_filled(self.arcade_rect, arcade.color.FOREST_GREEN)
        # If height is greater than width, draw the text vertically
        arcade.draw_text(
            self.address.name or self.avenue_street_address,
            self.arcade_rect.center_x,
            self.arcade_rect.center_y,
            arcade.color.BLACK,
            12,
            align="center",
            anchor_y="center",
            anchor_x="center",
            rotation=270 if self.arcade_rect.height > self.arcade_rect.width else 0,
        )


class TimesSquare(Location):
    """Times Square location in Manhattan."""

    def __init__(self):
        super().__init__(address=Address(6, 35, "Times Square", 2, 15))

    @property
    def player_speed_multiplier(self):
        return 0.25

    def draw(self):
        arcade.draw_rect_filled(self.arcade_rect, arcade.color.PINK)
        arcade.draw_text(
            self.address.name or self.avenue_street_address,
            self.arcade_rect.center_x,
            self.arcade_rect.center_y,
            arcade.color.BLACK,
            12,
            align="center",
            anchor_y="center",
            anchor_x="center",
            rotation=270 if self.arcade_rect.height > self.arcade_rect.width else 0,
        )


# Add special locations to the list here
SPECIAL_LOCATIONS = [
    CentralPark(),
    TimesSquare(),
]
