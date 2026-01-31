"""
Game Configuration - All constants and resource paths

This module contains all game configuration constants including:
- Screen dimensions and title
- Physics constants (gravity, speeds)
- Sprite scaling factors
- Resource paths for textures and sounds
"""

# Screen configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Arcade Platformer - Enhanced Edition"

# Physics constants
GRAVITY = 1.0  # Gravity force applied to player
PLAYER_MOVE_SPEED = 5.0  # Horizontal movement speed
PLAYER_JUMP_SPEED = 20.0  # Vertical jump velocity
PLAYER_MAX_HEALTH = 3  # Maximum number of hearts
KILL_PLANE_Y = -200  # Y coordinate below which player dies

# Animation settings
ANIMATION_RATE = 0.12  # Time between animation frames (seconds)

# Sprite scaling factors
CHARACTER_SCALING = 1.0  # Player character size multiplier
TILE_SCALING = 0.5  # Ground and platform tiles size multiplier
COIN_SCALING = 0.5  # Coin collectible size multiplier
ENEMY_SCALING = 0.6  # Enemy sprite size multiplier
HAZARD_SCALING = 0.5  # Lava and water hazard size multiplier

# Player character texture paths (male)
PLAYER_MALE_IDLE = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
PLAYER_MALE_JUMP = ":resources:images/animated_characters/male_adventurer/maleAdventurer_jump.png"
PLAYER_MALE_WALK = [
    f":resources:images/animated_characters/male_adventurer/maleAdventurer_walk{i}.png"
    for i in range(8)
]

# Player character texture paths (female)
PLAYER_FEMALE_IDLE = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
PLAYER_FEMALE_JUMP = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_jump.png"
PLAYER_FEMALE_WALK = [
    f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{i}.png"
    for i in range(8)
]

# Game object texture paths
COIN_TEXTURE = ":resources:images/items/coinGold.png"
GROUND_TEXTURE = ":resources:images/tiles/grassMid.png"
PLATFORM_TEXTURE = ":resources:images/tiles/boxCrate_double.png"
ENEMY_TEXTURE = ":resources:images/enemies/slimePurple.png"
LAVA_TEXTURE = ":resources:images/tiles/lava.png"
WATER_TEXTURE = ":resources:images/tiles/water.png"
FLAG_TEXTURE = ":resources:images/tiles/signExit.png"

# Sound effect paths
COIN_SOUND = ":resources:sounds/coin1.wav"
JUMP_SOUND = ":resources:sounds/jump3.wav"
HIT_SOUND = ":resources:sounds/hurt1.wav"
WIN_SOUND = ":resources:sounds/upgrade1.wav"
LOSE_SOUND = ":resources:sounds/gameover1.wav"
BACKGROUND_MUSIC = ":resources:music/funkyrobot.mp3"