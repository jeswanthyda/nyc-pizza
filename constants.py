"""NYC Pizza Delivery Game - Constants Module.

This module contains all game constants including screen dimensions,
map layout, street layout, and game mechanics.
"""

# Screen and Window Constants
SCREEN_WIDTH = 1200  # Increased to accommodate sidebar
SCREEN_HEIGHT = 800
SCREEN_TITLE = "NYC Pizza Delivery - Manhattan"

# Sidebar Constants
SIDEBAR_WIDTH = 200
SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH

# Player Constants
PLAYER_SIZE = 50
DEFAULT_PLAYER_SPEED = 300  # pixels per second


# Manhattan Map Constants
MAP_WIDTH = 800
MAP_HEIGHT = 600
MAP_OFFSET_X = 100
MAP_OFFSET_Y = 100

# Street Layout - Manhattan has a grid system with avenues (north-south) and streets (east-west)
AVENUES = 11  # Number of avenue blocks (vertical streets)
STREETS = 25  # Number of streets (horizontal streets)
AVENUE_WIDTH = MAP_WIDTH // (AVENUES + 1)
STREET_HEIGHT = MAP_HEIGHT // (STREETS + 1)

# Game Mechanics Constants
GAME_DURATION = 60.0  # Total game duration in seconds
COLLISION_THRESHOLD = 40  # Distance threshold for pickup/delivery interactions

# Default Address Spread Constants
DEFAULT_AVENUES_SPREAD = 1
DEFAULT_STREETS_SPREAD = 5
