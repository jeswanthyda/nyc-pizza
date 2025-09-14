import arcade

from ui_assets.base_models import Address, Location

__all__ = ["SPECIAL_LOCATIONS"]


class CentralPark(Location):
    """Central Park location in Manhattan."""

    def __init__(self):
        super().__init__(
            address=Address(5, 60, "Central Park", 3, 50),
            text_color=arcade.color.FOREST_GREEN,
        )


# Add special locations to the list here
SPECIAL_LOCATIONS = [
    CentralPark(),
]
