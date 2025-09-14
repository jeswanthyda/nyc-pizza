import arcade

from ui_assets.base_models import Address, Location

__all__ = ["HOMES"]


class Home(Location):
    """Home location in Manhattan. Coloured in green.
    Args:
        address (Address): Address of the home
    """

    def __init__(
        self,
        address: Address,
    ):
        super().__init__(
            address=address,
            text_color=arcade.color.GREEN,
        )


# Add homes to the list here
HOMES = [
    Home(Address(8, 8)),
    Home(Address(2, 15)),
    Home(Address(9, 20)),
    Home(Address(1, 10)),
    Home(Address(6, 25)),
    Home(Address(4, 5)),
    Home(Address(10, 18)),
    Home(Address(5, 12)),
    Home(Address(3, 22)),
]
