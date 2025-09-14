import arcade

from map_locations.base_models import Address, Location

__all__ = ["SUBWAYS"]


class Subway(Location):
    """Class representing a Subway in Manhattan.
    Args:
        address (Address): Address of the subway
    """

    def __init__(self, address: Address):
        super().__init__(address=address)
        # Load the subway image texture
        self.subway_texture = arcade.load_texture("images/subway.png")

    def draw(self):
        """Draw the subway using the subway.png image."""
        # Draw the subway image
        arcade.draw_texture_rect(self.subway_texture, self.arcade_rect, pixelated=True)


# Add subways to the list here
SUBWAYS = [
    Subway(Address(9, 86)),
    Subway(Address(1, 40)),
    Subway(Address(9, 52)),
]
