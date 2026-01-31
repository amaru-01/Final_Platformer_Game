"""
Level data - Definitions for all game levels

This module contains the LEVELS list which defines all playable levels.
Each level is a dictionary containing:
- name: Display name of the level
- player_start: (x, y) starting position for the player
- ground_segments: List of (start_x, end_x, y) tuples for ground tiles
- platforms: List of (x, y) tuples for platform positions
- coins: List of (x, y) tuples for coin positions
- goal_position: (x, y) position of the exit flag
- enemies: List of enemy dictionaries with patrol behavior
- hazards: List of hazard dictionaries (lava/water)
- kill_plane_y: Y coordinate below which player dies
"""

from config import KILL_PLANE_Y

# List of all game levels, ordered by difficulty
LEVELS = [
    {
        # Level 1: Easy tutorial level
        "name": "Forest Path",
        "player_start": (100, 200),  # Starting position (x, y)
        # Ground segments: (start_x, end_x, y) - creates continuous ground tiles
        "ground_segments": [
            (0, 300, 100),
            (400, 700, 100),
            (800, 1000, 100),
        ],
        # Platforms: (x, y) - individual platform positions
        "platforms": [
            (200, 150),
            (500, 200),
            (600, 250),
            (900, 200),
        ],
        # Coins: (x, y) - collectible coin positions
        "coins": [
            (250, 220),
            (350, 220),
            (550, 270),
            (650, 320),
            (950, 270),
        ],
        "goal_position": (950, 270),  # Exit flag position
        # Enemies: List of enemy patrol configurations
        "enemies": [
            {
                "position": (300, 170),  # Starting position
                "patrol_min_x": 250,  # Left patrol boundary
                "patrol_max_x": 350,  # Right patrol boundary
                "speed": 2.0,  # Movement speed
            },
        ],
        "hazards": [],  # No hazards in first level
        "kill_plane_y": KILL_PLANE_Y,  # Death plane Y coordinate
    },
    {
        # Level 2: Medium difficulty with vertical progression
        "name": "Mountain Climb",
        "player_start": (100, 150),
        # Ascending ground segments creating a mountain path
        "ground_segments": [
            (0, 200, 100),
            (300, 500, 150),
            (600, 800, 200),
            (850, 1000, 250),
        ],
        # Platforms creating vertical climbing challenge
        "platforms": [
            (250, 200),
            (450, 250),
            (550, 300),
            (750, 350),
            (900, 400),
        ],
        # Coins placed along the climbing path
        "coins": [
            (150, 170),
            (350, 320),
            (450, 370),
            (600, 370),
            (650, 420),
            (800, 470),
            (950, 520),
        ],
        "goal_position": (950, 520),  # Goal at the top
        # Two enemies patrolling different sections
        "enemies": [
            {
                "position": (400, 220),
                "patrol_min_x": 350,
                "patrol_max_x": 450,
                "speed": 2.5,
            },
            {
                "position": (700, 270),
                "patrol_min_x": 650,
                "patrol_max_x": 750,
                "speed": 2.5,
            },
        ],
        # Lava hazard in gap between ground segments
        "hazards": [
            {
                "type": "lava",
                "position": (250, 75),  # Positioned in gap between first and second ground segments
                "width": 150,
            },
        ],
        "kill_plane_y": KILL_PLANE_Y,
    },
    {
        # Level 3: Hard difficulty with multiple hazards and enemies
        "name": "Volcano Challenge",
        "player_start": (100, 200),
        # Varied ground heights creating challenging jumps
        "ground_segments": [
            (0, 150, 100),
            (200, 350, 150),
            (400, 550, 200),
            (600, 750, 150),
            (800, 1000, 200),
        ],
        # Platforms requiring precise jumping
        "platforms": [
            (300, 250),
            (500, 300),
            (700, 250),
            (850, 300),
        ],
        # More coins to collect
        "coins": [
            (120, 270),
            (250, 320),
            (350, 370),
            (450, 420),
            (550, 420),
            (650, 320),
            (750, 370),
            (900, 420),
        ],
        "goal_position": (950, 420),
        # Three faster enemies
        "enemies": [
            {
                "position": (250, 220),
                "patrol_min_x": 200,
                "patrol_max_x": 300,
                "speed": 3.0,  # Faster than previous levels
            },
            {
                "position": (450, 270),
                "patrol_min_x": 400,
                "patrol_max_x": 500,
                "speed": 3.0,
            },
            {
                "position": (650, 220),
                "patrol_min_x": 600,
                "patrol_max_x": 700,
                "speed": 3.0,
            },
        ],
        # Multiple hazards in gaps between platforms
        "hazards": [
            {
                "type": "lava",
                "position": (175, 75),  # Gap between first ground segment and first platform
                "width": 100,
            },
            {
                "type": "water",
                "position": (375, 75),  # Gap between second ground segment and second platform
                "width": 150,
            },
            {
                "type": "lava",
                "position": (775, 75),  # Gap between fourth ground segment and last platform
                "width": 200,
            },
        ],
        "kill_plane_y": KILL_PLANE_Y,
    },
]
