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


class Address:
    """Address of a location."""

    def __init__(
        self,
        avenue_number: int,
        street_number: int,
        name: str | None = None,
        avenues_spread: int = DEFAULT_AVENUES_SPREAD,
        streets_spread: int = DEFAULT_STREETS_SPREAD,
    ):
        self.avenue_number = avenue_number
        self.street_number = street_number
        self.name = name
        self.avenues_spread = avenues_spread
        self.streets_spread = streets_spread

    @property
    def avenue_street_address(self) -> str:
        """Get the address of the location."""
        return f"{self.avenue_number}Av, {self.street_number}St"

    def to_arcade_rect(self) -> arcade.Rect:
        """
        Convert avenue/street numbers to arcade.Rect.

        Returns:
            arcade.Rect: Rectangle object to be rendered by arcade.
        """
        right = MAP_OFFSET_X + (AVENUES + 1 - self.avenue_number) * AVENUE_WIDTH
        left = right - (self.avenues_spread) * AVENUE_WIDTH
        bottom = MAP_OFFSET_Y + (self.street_number // 5 - 1) * STREET_HEIGHT
        top = bottom + (self.streets_spread // 5) * STREET_HEIGHT

        return arcade.LRBT(left, right, bottom, top)


class Location(arcade.Sprite):
    """Base class for all locations in the game."""

    def __init__(self, address: Address, text_color: arcade.color.Color):
        """
        Initialize a location.

        Args:
            address: Address of the location
            text_color: Arcade color for the location
        """
        # Initialize arcade.Sprite first
        super().__init__()

        self.address = address
        self.text_color = text_color

        self.rectangle = self.address.to_arcade_rect()

        # Set sprite properties for collision detection
        self.center_x = self.rectangle.center_x
        self.center_y = self.rectangle.center_y
        self.width = self.rectangle.width
        self.height = self.rectangle.height

    @property
    def avenue_street_address(self) -> str:
        """Get the avenue/street address of the location."""
        return self.address.avenue_street_address

    @property
    def arcade_rect(self) -> arcade.Rect:
        return self.rectangle

    def draw(self):
        """Draw the location as a rectangle."""
        arcade.draw_rect_filled(self.rectangle, self.text_color)
        # If height is greater than width, draw the text vertically
        arcade.draw_text(
            self.address.name or self.address.avenue_street_address,
            self.rectangle.center_x,
            self.rectangle.center_y,
            arcade.color.WHITE,
            12,
            align="center",
            anchor_y="center",
            anchor_x="center",
            rotation=270 if self.rectangle.height > self.rectangle.width else 0,
        )
