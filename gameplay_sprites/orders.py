"""NYC Pizza Delivery Game - Orders Module.

This module contains the order system with pickup and delivery addresses.
"""

import random

import arcade

from map_locations import HOMES, PIZZA_SHOPS, Location


class Order(arcade.Sprite):
    """Represents a pizza delivery order as a sprite."""

    def __init__(self, pickup_location: Location, delivery_location: Location):
        """
        Initialize an order.

        Args:
            pickup_location: Location to pick up pizza from
            delivery_location: Location to deliver pizza to
        """
        # Initialize arcade.Sprite first
        super().__init__()

        self.pickup_location = pickup_location
        self.delivery_location = delivery_location

        # Set sprite properties (invisible sprite for drawing purposes)
        self.center_x = 0
        self.center_y = 0
        self.width = 0
        self.height = 0

    @classmethod
    def generate_order(cls) -> "Order":
        """Generate a random order."""
        pickup_location = random.choice(PIZZA_SHOPS)
        delivery_location = random.choice(HOMES)
        return cls(pickup_location=pickup_location, delivery_location=delivery_location)

    def draw_order_info(self, x: int, y: int, flash_timer: float) -> int:
        """
        Draw the order information and return the next y position.

        Args:
            x: X position to draw at
            y: Y position to start drawing at
            flash_timer: Timer for flashing colors

        Returns:
            Next y position after drawing
        """
        current_y = y

        # Always show order, but alternate colors based on flash_timer
        order_text = "ACTIVE ORDER:"
        arcade.draw_text(order_text, x, current_y, arcade.color.BLACK, 14, bold=True)

        should_use_alt_color = (flash_timer % 1.0) < 0.5
        pickup_color = arcade.color.RED if should_use_alt_color else arcade.color.ORANGE
        delivery_color = (
            arcade.color.BLUE if should_use_alt_color else arcade.color.CYAN
        )

        current_y -= 20

        pickup_text = f"Pickup from {self.pickup_location.address.name}"
        arcade.draw_text(pickup_text, x, current_y, pickup_color, 12)
        current_y -= 15

        pickup_address = f"at {self.pickup_location.address.avenue_street_address}"
        arcade.draw_text(pickup_address, x, current_y, pickup_color, 12)
        current_y -= 20

        delivery_text = (
            f"Deliver to {self.delivery_location.address.avenue_street_address}"
        )
        arcade.draw_text(
            delivery_text,
            x,
            current_y,
            delivery_color,
            12,
            bold=True,
        )

        return current_y
