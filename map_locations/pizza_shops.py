import arcade

from map_locations.base_models import Address, PizzaShop

__all__ = ["PIZZA_SHOPS"]


# Add pizza shops to the list here
PIZZA_SHOPS = [
    PizzaShop(
        Address(8, 42, "Joe's"), arcade.load_texture("images/pizza_shops/joes.png")
    ),
    PizzaShop(
        Address(6, 33, "Papa J's"), arcade.load_texture("images/pizza_shops/papajs.png")
    ),
    PizzaShop(
        Address(2, 86, "2Bro's"), arcade.load_texture("images/pizza_shops/2bros.png")
    ),
    PizzaShop(
        Address(11, 120, "Joe's"), arcade.load_texture("images/pizza_shops/joes.png")
    ),
    PizzaShop(
        Address(1, 18, "Papa J's"), arcade.load_texture("images/pizza_shops/papajs.png")
    ),
]
