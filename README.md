# 🍕 NYC-PIZZA-DELIVERY

You play as a pizza delivery driver racing against the clock to pick up pizzas from shops and deliver them to customers at their homes.

Your mission? Deliver as many pizzas as possible in **1min**.


## 🎮 Gameplay

* Each game session lasts **1min**.
* Orders appear with:
  * A **pickup location** (pizza shop).
  * A **delivery location** (home).
* Drive along NYC’s streets and avenues to complete the delivery.
* Each successful delivery increases your score by **+$10 USD**.
* Each subway use costs you **-$1 USD**.
* At the end of the session, your **total USD score is stored in database**.

**Objective:** Deliver as many pizzas as possible before time runs out.

## 🎹 Controls

* **Arrow Keys / WASD** → Move delivery driver
* **Space** → Pick up / Drop pizza / teleport at subway to a nearest subway to destination
* **Esc** → Quit game



## 🗺 Features

* **NYC Map Grid** – Pizza shops, homes, streets and avenues.
* **1min Sessions** – Short, replayable gameplay loops.
* **USD Scoring System** – +$10 USD per successful delivery, -$1 USD per subway use.
* **Local Score Logging** – Saves your final USD score at the end of each session.

## 🚀 How to Run

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd nyc-pizza
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

### Running the Game

The NYC Pizza game consists of two components that need to be running:

1. **Start the backend server:**
   ```bash
   make run_backend_server
   ```
   This will start the FastAPI server on `http://localhost:8000`

2. **In a new terminal, start the game:**
   ```bash
   make run_game
   ```

### Game Requirements

- **Backend must be running**: The game client requires the FastAPI backend server to be running for session management and score tracking
- **Two terminals needed**: One for the backend server, one for the game client
- **Default ports**: Backend runs on port 8000, game client connects to it

### Troubleshooting

- **"Connection refused" errors**: Make sure the backend server is running before starting the game
- **Import errors**: Ensure all dependencies are installed with `make install`
- **Python version**: Make sure you're using Python 3.13 or higher



## 🛠 Tech Stack

- **Arcade** - For 2D game development in python.
- **FastAPI** - Application layer sitting infront of database for db operations during game.
- **SQLite** - Lightweight, serverless database engine for persistent storage of game sessions and scores.
- **Pydantic** - Data validation and settings management using Python type annotations.
- **uv** - Fast Python package and project manager for dependency management and virtual environments.



#### 📁 Project Structure

```
nyc-pizza/
├── backend/                    # Backend API and database
│   ├── client.py              # FastAPI client
│   ├── server/                # FastAPI server components
│   │   ├── fastapi_server.py  # Main FastAPI application
│   │   ├── schemas.py         # Pydantic data models
│   │   └── sessions_handler.py # Session management
│   └── db/                    # Database layer
│       ├── connection.py      # Database connection setup
│       ├── models.py          # Schema models
│       ├── migrations/        # Database migrations
│       └── nyc_pizza.db       # SQLite database file
├── gameplay/                  # Core game logic
│   ├── game.py               # Main game class
│   ├── game_state_manager.py # Game state management
│   ├── orders.py             # Order generation and handling
│   ├── player.py             # Player character logic
│   ├── score_tracker.py      # Scoring system
│   └── session_manager.py    # Game session management
├── map_locations/            # Map and location definitions
│   ├── base_models.py        # Base location models
│   ├── homes.py              # Home delivery locations
│   ├── pizza_shops.py        # Pizza shop pickup locations
│   ├── subways.py            # Subway station locations
│   └── speed_multiplier_locations.py # Speed boost locations
├── static_drawings/          # UI components and dialogs
│   ├── final_score_dialog.py # End game score display
│   ├── game_instructions_dialog.py # Game instructions
│   ├── leaderboard_dialog.py # High scores display
│   ├── manhattan_grid.py     # NYC map grid rendering
│   └── name_input_dialog.py  # Player name input
├── images/                   # Game assets
│   ├── home.png             # Home location icon
│   ├── scooter.png          # Delivery scooter
│   ├── subway.png           # Subway station icon
│   └── pizza_shops/         # Pizza shop logos
│       ├── 2bros.png
│       ├── joes.png
│       └── papajs.png
├── constants.py              # Game configuration constants
├── logging_utils.py          # Logging utilities
├── run_backend.py           # Backend server entry point
├── run_game.py              # Game client entry point
└── pyproject.toml           # Python project configuration
```

