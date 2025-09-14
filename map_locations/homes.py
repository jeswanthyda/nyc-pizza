import arcade

from map_locations.base_models import Address, Location

__all__ = ["HOMES"]


class Home(Location):
    """Home location in Manhattan. Coloured in green.
    Args:
        address (Address): Address of the home
    """

    def __init__(self, address: Address):
        super().__init__(address=address)
        self.home_texture = arcade.load_texture("images/home.png")

    def draw(self):
        """Draw the home using the home texture."""
        arcade.draw_texture_rect(self.home_texture, self.arcade_rect, pixelated=True)


# Add homes to the list here
HOMES = [
    Home(Address(8, 8)),
    Home(Address(1, 15)),
    Home(Address(2, 120)),
    Home(Address(5, 23)),
    Home(Address(7, 32)),
    Home(Address(10, 45)),
    Home(Address(10, 18)),
    Home(Address(4, 55)),
    Home(Address(11, 65)),
]
