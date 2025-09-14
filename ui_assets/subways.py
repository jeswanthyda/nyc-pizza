import arcade

from ui_assets.base_models import Address, Location

__all__ = ["SUBWAYS"]


class Subway(Location):
    """Class representing a Subway in Manhattan.
    Args:
        address (Address): Address of the subway
    """

    def __init__(self, address: Address):
        super().__init__(
            address=address,
            text_color=arcade.color.BLUE,
        )


# Add subways to the list here
SUBWAYS = [
    Subway(Address(9, 86, "1")),
    Subway(Address(1, 40, "2")),
    Subway(Address(9, 52, "3")),
]
