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
    PizzaShop(Address(3, 6, "Joe's")),
    PizzaShop(Address(7, 12, "Papa J's")),
    PizzaShop(Address(10, 15, "Tom's")),
    PizzaShop(Address(6, 20, "Dominos")),
]
