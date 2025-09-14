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


class PizzaShop(Location):
    """Class representing a Pizza shop in Manhattan. Coloured in red.
    Args:
        address (Address): Address of the pizza shop
    """

    def __init__(self, address: Address, logo_texture: arcade.Texture):
        super().__init__(address=address)
        self.logo_texture = logo_texture

    def draw(self):
        """Draw the pizza shop using the logo texture."""
        arcade.draw_texture_rect(self.logo_texture, self.arcade_rect, pixelated=True)


class Subway(Location):
    """Class representing a Subway in Manhattan.
    Args:
        address (Address): Address of the subway
    """

    def __init__(self, address: Address):
        super().__init__(address=address)
        # Load the subway image texture
        self.subway_texture = arcade.load_texture("images/subway.png")

    def draw(self):
        """Draw the subway using the subway.png image."""
        # Draw the subway image
        arcade.draw_texture_rect(self.subway_texture, self.arcade_rect, pixelated=True)


class Home(Location):
    """Home location in Manhattan. Coloured in green.
    Args:
        address (Address): Address of the home
    """

    def __init__(self, address: Address):
        super().__init__(address=address)
        self.home_texture = arcade.load_texture("images/home.png")

    def draw(self):
        """Draw the home using the home texture."""
        arcade.draw_texture_rect(self.home_texture, self.arcade_rect, pixelated=True)


class SpeedMultiplierLocation(Location):
    """Base class for locations that have a speed multiplier."""

    def __init__(
        self,
        address: Address,
        speed_multiplier: float = 1.0,
        block_color: arcade.color.Color = arcade.color.LIGHT_APRICOT,
    ):
        super().__init__(address=address)
        self.speed_multiplier = speed_multiplier
        self.block_color = block_color

    @property
    def player_speed_multiplier(self):
        return self.speed_multiplier

    def draw(self):
        arcade.draw_rect_filled(self.arcade_rect, self.block_color)
        arcade.draw_text(
            self.address.name or self.avenue_street_address,
            self.arcade_rect.center_x,
            self.arcade_rect.center_y,
            arcade.color.BLACK,
            12,
            align="center",
            anchor_y="center",
            anchor_x="center",
            rotation=270 if self.arcade_rect.height > self.arcade_rect.width else 0,
        )
