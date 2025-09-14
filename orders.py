"""NYC Pizza Delivery Game - Orders Module.

This module contains the order system with pickup and delivery addresses.
"""

import random
from dataclasses import dataclass

from ui_assets.base_models import Location
from ui_assets.homes import HOMES
from ui_assets.pizza_shops import PIZZA_SHOPS


@dataclass
class Order:
    """Represents a pizza delivery order."""

    pickup_location: Location
    delivery_location: Location

    @classmethod
    def generate_order(cls) -> "Order":
        """Generate a random order."""
        pickup_location = random.choice(PIZZA_SHOPS)
        delivery_location = random.choice(HOMES)
        return cls(pickup_location=pickup_location, delivery_location=delivery_location)
