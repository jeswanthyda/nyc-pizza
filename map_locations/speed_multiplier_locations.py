import arcade

from map_locations.base_models import Address, SpeedMultiplierLocation

__all__ = ["SPEED_MULTIPLIER_LOCATIONS"]


# Add Speed Multiplier locations to the list here
SPEED_MULTIPLIER_LOCATIONS = [
    SpeedMultiplierLocation(
        address=Address(5, 60, "Central Park", 3, 50),
        speed_multiplier=2,
        block_color=arcade.color.FOREST_GREEN,
    ),
    SpeedMultiplierLocation(
        address=Address(6, 35, "Times Square", 2, 15),
        speed_multiplier=0.25,
        block_color=arcade.color.PINK,
    ),
]
