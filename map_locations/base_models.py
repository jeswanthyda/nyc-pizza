from abc import ABC, abstractmethod
from dataclasses import dataclass

import arcade

from constants import (
    AVENUE_WIDTH,
    AVENUES,
    DEFAULT_AVENUES_SPREAD,
    DEFAULT_STREETS_SPREAD,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    STREET_HEIGHT,
)


@dataclass
class Address:
    """Address of a location."""

    avenue_number: int
    street_number: int
    name: str | None = None
    avenues_spread: int = DEFAULT_AVENUES_SPREAD
    streets_spread: int = DEFAULT_STREETS_SPREAD


class Location(arcade.Sprite, ABC):
    """Base class for all locations in the game."""

    def __init__(self, address: Address):
        """
        Initialize a location.

        Args:
            address: Address of the location
        """
        # Initialize arcade.Sprite first
        super().__init__()

        self.address = address

        self._arcade_rect: arcade.Rect | None = None

        # Set sprite properties for collision detection
        self.center_x = self.arcade_rect.center_x
        self.center_y = self.arcade_rect.center_y
        self.width = self.arcade_rect.width
        self.height = self.arcade_rect.height

    @property
    def avenue_street_address(self) -> str:
        """Get the avenue/street address of the location."""
        return f"{self.address.avenue_number}Av, {self.address.street_number}St"

    @property
    def name(self) -> str:
        """Get the name of the location."""
        return self.address.name or self.avenue_street_address

    @property
    def arcade_rect(self) -> arcade.Rect:
        """Get the arcade rectangle for the location.

        Convert avenue/street numbers to arcade.Rect.

        Returns:
            arcade.Rect: Rectangle object to be rendered by arcade.
        """
        if self._arcade_rect is None:
            right = (
                MAP_OFFSET_X + (AVENUES + 1 - self.address.avenue_number) * AVENUE_WIDTH
            )
            left = right - (self.address.avenues_spread) * AVENUE_WIDTH
            bottom = (
                MAP_OFFSET_Y + (self.address.street_number // 5 - 1) * STREET_HEIGHT
            )
            top = bottom + (self.address.streets_spread // 5) * STREET_HEIGHT

            self._arcade_rect = arcade.LRBT(left, right, bottom, top)

        return self._arcade_rect

    @abstractmethod
    def draw(self):
        """Draw the location as a rectangle."""
        raise NotImplementedError("Subclasses must implement this method")
