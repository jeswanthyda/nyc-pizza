import arcade

from ui_assets.base_models import Address, Location

__all__ = ["PIZZA_SHOPS"]


class PizzaShop(Location):
    """Class representing a Pizza shop in Manhattan. Coloured in red.
    Args:
        address (Address): Address of the pizza shop
    """

    def __init__(self, address: Address):
        super().__init__(
            address=address,
            text_color=arcade.color.RED,
        )


# Add pizza shops to the list here
PIZZA_SHOPS = [
    PizzaShop(Address(8, 42, "Joe's")),
    PizzaShop(Address(6, 33, "Papa J's")),
    PizzaShop(Address(2, 86, "Tom's")),
    PizzaShop(Address(11, 120, "Dominos")),
]
