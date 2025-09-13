"""NYC Pizza Delivery Game - Orders Module.

This module contains the order system with pickup and delivery addresses.
"""

from dataclasses import dataclass
from typing import List

from map_layout import Address


@dataclass
class Order:
    """Represents a pizza delivery order."""

    pickup_address: Address
    delivery_address: Address


# Sample orders for the NYC Pizza Delivery Game
ORDERS: List[Order] = [
    Order(
        pickup_address=Address(3, 6, "Joe's Pizza"),  # Joe's Pizza
        delivery_address=Address(8, 8),  # Home
    ),
    Order(
        pickup_address=Address(7, 12, "Papa's Pizza"),  # Papa's Pizza
        delivery_address=Address(2, 15),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(9, 20),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(1, 10),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(6, 25),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(4, 5),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(10, 18),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(5, 12),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(3, 22),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(8, 3),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(7, 16),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(2, 8),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(9, 14),
    ),
    Order(
        pickup_address=Address(7, 12),  # Papa's Pizza
        delivery_address=Address(6, 7),
    ),
    Order(
        pickup_address=Address(3, 6),  # Joe's Pizza
        delivery_address=Address(4, 19),
    ),
]
