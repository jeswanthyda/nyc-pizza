import arcade

from ui_assets.base_models import Address, Location

__all__ = ["PIZZA_SHOPS"]


class PizzaShop(Location):
    """Class representing a Pizza shop in Manhattan. Coloured in red.
    Args:
        address (Address): Address of the pizza shop
    """

    def __init__(self, address: Address, logo_texture: arcade.Texture):
        super().__init__(
            address=address,
            text_color=arcade.color.RED,
        )
        self.logo_texture = logo_texture

    def draw(self):
        """Draw the pizza shop using the logo texture."""
        arcade.draw_texture_rect(self.logo_texture, self.arcade_rect, pixelated=True)


# Add pizza shops to the list here
PIZZA_SHOPS = [
    PizzaShop(Address(8, 42, "Joe's"), arcade.load_texture("joes.png")),
    PizzaShop(Address(6, 33, "Papa J's"), arcade.load_texture("papajs.png")),
    PizzaShop(Address(2, 86, "2Bro's"), arcade.load_texture("2bros.png")),
    PizzaShop(Address(11, 120, "Joe's"), arcade.load_texture("joes.png")),
]
