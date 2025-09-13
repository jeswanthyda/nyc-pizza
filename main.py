"""NYC Pizza Delivery Game - Main entry point."""

import arcade

from map_layout import (
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    Address,
    CentralPark,
    Home,
    PizzaShop,
    draw_manhattan_map,
)

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "NYC Pizza Delivery - Manhattan"


# Player constants
PLAYER_SIZE = 50

# Location constants
PIZZA_SHOP_SIZE = 30
HOME_SIZE = 30


class PlayerCharacter(arcade.Sprite):
    """Player character - Pizza Delivery Person."""

    def __init__(self):
        super().__init__()
        # Start at center of Manhattan map
        self.center_x = MAP_OFFSET_X + MAP_WIDTH // 2
        self.center_y = MAP_OFFSET_Y + MAP_HEIGHT // 2
        self.has_pizza = False

        # Movement properties
        self.speed = 300  # pixels per second
        self.change_x = 0
        self.change_y = 0

        # Load the scooter image and scale it
        self.texture = arcade.load_texture("scooter.png")
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    def move_direction(self, direction):
        """Set movement velocity in the specified direction."""
        if direction == "up":
            self.change_y = self.speed
            self.change_x = 0
        elif direction == "down":
            self.change_y = -self.speed
            self.change_x = 0
        elif direction == "left":
            self.change_x = -self.speed
            self.change_y = 0
        elif direction == "right":
            self.change_x = self.speed
            self.change_y = 0

    def stop_movement(self):
        """Stop all movement."""
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time=0):
        """Update the delivery person's position with velocity."""
        # Update position based on velocity
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Keep player within Manhattan map boundaries
        min_x = MAP_OFFSET_X
        max_x = MAP_OFFSET_X + MAP_WIDTH
        min_y = MAP_OFFSET_Y
        max_y = MAP_OFFSET_Y + MAP_HEIGHT

        if self.center_x < min_x:
            self.center_x = min_x
            self.change_x = 0
        elif self.center_x > max_x:
            self.center_x = max_x
            self.change_x = 0

        if self.center_y < min_y:
            self.center_y = min_y
            self.change_y = 0
        elif self.center_y > max_y:
            self.center_y = max_y
            self.change_y = 0


class PizzaDeliveryGame(arcade.Window):
    """Main game class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        # Game objects
        self.player_character = None
        self.joes_pizza = None
        self.home = None
        self.score = 0

        # Sprite lists
        self.player_list = None
        self.location_list = None

    def _setup_pizza_shops(self):
        """Setup the pizza shops."""
        self.joes_pizza = PizzaShop(Address(3, 6), "Joe's Pizza")
        self.location_list.append(self.joes_pizza)

    def _setup_homes(self):
        """Setup the homes."""
        self.home = Home(Address(8, 8), "Home")
        self.location_list.append(self.home)

    def setup(self):
        """Set up the game variables."""
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.location_list = arcade.SpriteList()

        # Create delivery boy
        self.player_character = PlayerCharacter()
        self.player_list.append(self.player_character)

        self._setup_pizza_shops()
        self._setup_homes()

        # Create Central Park location
        self.central_park = CentralPark()
        self.location_list.append(self.central_park)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw Manhattan map first
        draw_manhattan_map()

        # Draw all sprites
        for location in self.location_list:
            location.draw()

        # Draw home with custom text
        self.home.draw()

        self.player_list.draw()

        # Draw UI
        arcade.draw_text(
            f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16
        )

        # Draw map labels
        arcade.draw_text(
            "Manhattan Pizza Delivery",
            MAP_OFFSET_X,
            MAP_OFFSET_Y + MAP_HEIGHT + 20,
            arcade.color.BLACK,
            20,
        )

        # Draw instructions
        if not self.player_character.has_pizza:
            arcade.draw_text(
                "Go to Joe's Pizza (RED) and press SPACE to pick up pizza!",
                10,
                30,
                arcade.color.BLACK,
                14,
            )
        else:
            arcade.draw_text(
                "Go to GREEN home and press SPACE to deliver pizza!",
                10,
                30,
                arcade.color.BLACK,
                14,
            )

        # Draw controls
        arcade.draw_text(
            "Controls: WASD/Arrow Keys to move, SPACE to pickup/deliver",
            10,
            10,
            arcade.color.BLACK,
            12,
        )

        # Draw pizza indicator
        if self.player_character.has_pizza:
            arcade.draw_circle_filled(
                self.player_character.center_x,
                self.player_character.center_y + 30,
                8,
                arcade.color.YELLOW,
            )

    def on_update(self, delta_time):
        """Movement and game logic."""
        self.player_list.update()

    def handle_space_action(self):
        """Handle space bar action for pizza pickup and dropoff."""
        # Check for pizza pickup using distance-based collision detection
        if not self.player_character.has_pizza:
            distance = arcade.get_distance_between_sprites(
                self.player_character, self.joes_pizza
            )
            if distance < 40:  # Collision threshold
                self.player_character.has_pizza = True
                print("Pizza picked up from Joe's Pizza!")

        # Check for pizza delivery using distance-based collision detection
        elif self.player_character.has_pizza:
            distance = arcade.get_distance_between_sprites(
                self.player_character, self.home
            )
            if distance < 40:  # Collision threshold
                self.player_character.has_pizza = False
                self.score += 1
                print(f"Pizza delivered! Score: {self.score}")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_character.move_direction("up")
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_character.move_direction("down")
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_character.move_direction("left")
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_character.move_direction("right")
        elif key == arcade.key.SPACE:
            self.handle_space_action()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Stop movement when key is released
        if (
            key == arcade.key.UP
            or key == arcade.key.W
            or key == arcade.key.DOWN
            or key == arcade.key.S
            or key == arcade.key.LEFT
            or key == arcade.key.A
            or key == arcade.key.RIGHT
            or key == arcade.key.D
        ):
            self.player_character.stop_movement()


def main():
    """Main function."""
    game = PizzaDeliveryGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
