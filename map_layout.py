"""NYC Pizza Delivery Game - Map Layout Module."""

import arcade

# Manhattan map constants
MAP_WIDTH = 800
MAP_HEIGHT = 600
MAP_OFFSET_X = 100
MAP_OFFSET_Y = 100
STREET_NUMBER_OFFSET = 50

# Street layout - Manhattan has a grid system with avenues (north-south) and streets (east-west)
AVENUES = 11  # Number of avenue blocks (vertical streets)
STREETS = 25  # Number of streets (horizontal streets)
AVENUE_WIDTH = MAP_WIDTH // (AVENUES + 1)
STREET_HEIGHT = MAP_HEIGHT // (STREETS + 1)


class Address:
    """Address of a location."""

    def __init__(
        self,
        avenue_number: int,
        street_number: int,
        avenues_spread: int = 1,
        streets_spread: int = 5,
    ):
        self.avenue_number = avenue_number
        self.street_number = street_number
        self.avenues_spread = avenues_spread
        self.streets_spread = streets_spread

    @property
    def avenue_street_address(self) -> str:
        """Get the address of the location."""
        return f"{self.avenue_number}th Ave, {self.street_number}th St"

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


class BaseLocation(arcade.Sprite):
    """Base class for all locations in the game."""

    def __init__(self, address: Address, name: str, text_color: arcade.color.Color):
        """
        Initialize a location.

        Args:
            address: Address of the location
            name (str): Name of the location
            text_color: Arcade color for the location
        """
        # Initialize arcade.Sprite first
        super().__init__()

        self.address = address
        self.name = name
        self.text_color = text_color

        self.rectangle = self.address.to_arcade_rect()

        # Set sprite properties for collision detection
        self.center_x = self.rectangle.center_x
        self.center_y = self.rectangle.center_y
        self.width = self.rectangle.width
        self.height = self.rectangle.height

    def draw(self):
        """Draw the location as a rectangle."""
        arcade.draw_rect_filled(self.rectangle, self.text_color)
        # If height is greater than width, draw the text vertically
        if self.rectangle.height > self.rectangle.width:
            arcade.draw_text(
                self.name,
                self.rectangle.center_x,
                self.rectangle.center_y,
                arcade.color.WHITE,
                12,
                align="center",
                anchor_y="center",
                anchor_x="center",
                rotation=270,
            )
        else:
            arcade.draw_text(
                self.name,
                self.rectangle.center_x,
                self.rectangle.center_y,
                arcade.color.WHITE,
                12,
                align="center",
                anchor_y="center",
                anchor_x="center",
                rotation=0,
            )

    def get_address(self) -> str:
        """Get the address of the location."""
        return self.address.avenue_street_address


class CentralPark(BaseLocation):
    """Central Park location in Manhattan."""

    def __init__(self):
        super().__init__(
            address=Address(5, 60, 3, 50),
            name="Central Park",
            text_color=arcade.color.FOREST_GREEN,
        )


class PizzaShop(BaseLocation):
    """Class representing a Pizza shop in Manhattan. Coloured in red.
    Args:
        name (str): Name of the pizza shop
        avenue_number (int): Starting avenue number
        street_number (int): Starting street number
    """

    def __init__(self, address: Address, name: str):
        super().__init__(
            address=address,
            name=name,
            text_color=arcade.color.RED,
        )


class Home(BaseLocation):
    """Home location in Manhattan. Coloured in green.
    Args:
        name (str): Name of the home
        avenue_number (int): Starting avenue number
        street_number (int): Starting street number
    """

    def __init__(
        self,
        address: Address,
        name: str | None = None,
    ):
        super().__init__(
            address=address,
            name=name or "",
            text_color=arcade.color.GREEN,
        )


def draw_manhattan_map():
    """Draw the Manhattan street grid."""
    # Draw background (city blocks)
    background_rect = arcade.LRBT(
        MAP_OFFSET_X, MAP_OFFSET_X + MAP_WIDTH, MAP_OFFSET_Y, MAP_OFFSET_Y + MAP_HEIGHT
    )
    arcade.draw_rect_filled(background_rect, arcade.color.LIGHT_GRAY)

    # Draw avenues (vertical streets)
    for i in range(AVENUES + 1):
        x = MAP_OFFSET_X + (i * AVENUE_WIDTH)
        arcade.draw_line(
            x, MAP_OFFSET_Y, x, MAP_OFFSET_Y + MAP_HEIGHT, arcade.color.DARK_GRAY, 3
        )

    # Draw streets (horizontal streets)
    for i in range(STREETS + 1):
        y = MAP_OFFSET_Y + (i * STREET_HEIGHT)
        arcade.draw_line(
            MAP_OFFSET_X, y, MAP_OFFSET_X + MAP_WIDTH, y, arcade.color.DARK_GRAY, 3
        )

    # Draw Hudson River (blue rectangle on the left)
    hudson_rect = arcade.LRBT(0, MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_Y + MAP_HEIGHT)
    arcade.draw_rect_filled(hudson_rect, arcade.color.TEAL_BLUE)

    # Draw East River (blue rectangle on the right)
    east_rect = arcade.LRBT(
        MAP_OFFSET_X + MAP_WIDTH,
        MAP_OFFSET_X + MAP_WIDTH + MAP_OFFSET_X,
        MAP_OFFSET_Y,
        MAP_OFFSET_Y + MAP_HEIGHT,
    )
    arcade.draw_rect_filled(east_rect, arcade.color.TEAL_BLUE)

    # Draw avenue numbers (along the top and bottom)
    for i in range(AVENUES + 1):
        x = MAP_OFFSET_X + (i * AVENUE_WIDTH)
        # Reverse the avenue numbering: 1st Ave on right (east), higher numbers on left (west)
        avenue_num = AVENUES + 1 - i

        # Top labels
        arcade.draw_text(
            f"{avenue_num}st Ave",
            x - 20,
            MAP_OFFSET_Y + MAP_HEIGHT + 5,
            arcade.color.BLACK,
            10,
        )

        # Bottom labels
        arcade.draw_text(
            f"{avenue_num}st Ave", x - 20, MAP_OFFSET_Y - 20, arcade.color.BLACK, 10
        )

    # Draw street numbers (along the left and right sides)
    for i in range(STREETS + 1):
        y = MAP_OFFSET_Y + (i * STREET_HEIGHT)
        # Number streets as multiples of 5 (5th, 10th, 15th, 20th, etc.)
        street_num = (i + 1) * 5

        # Left side labels
        arcade.draw_text(
            f"{street_num}th St", STREET_NUMBER_OFFSET, y - 5, arcade.color.BLACK, 10
        )

        # Right side labels
        arcade.draw_text(
            f"{street_num}th St",
            MAP_OFFSET_X + MAP_WIDTH,
            y - 5,
            arcade.color.BLACK,
            10,
        )
