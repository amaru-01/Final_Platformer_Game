"""
Player Sprite with gender selection support

This module defines the PlayerSprite class which handles:
- Character gender selection (male/female)
- Animation states (idle, walk, jump)
- Sprite flipping based on movement direction
"""

import arcade
from config import *


class PlayerSprite(arcade.Sprite):
    """
    Player character sprite with animation support.
    
    Supports both male and female character models with:
    - Idle animation
    - Walking animation (8 frames)
    - Jumping animation
    - Automatic sprite flipping based on movement direction
    """
    
    def __init__(self, gender="female"):
        """
        Initialize the player sprite.
        
        Args:
            gender (str): "male" or "female" to select character model
        """
        super().__init__(scale=CHARACTER_SCALING)
        
        # Load textures based on selected gender
        if gender == "male":
            self.idle_texture = arcade.load_texture(PLAYER_MALE_IDLE)
            self.jump_texture = arcade.load_texture(PLAYER_MALE_JUMP)
            self.walk_textures = [arcade.load_texture(path) for path in PLAYER_MALE_WALK]
        else:
            self.idle_texture = arcade.load_texture(PLAYER_FEMALE_IDLE)
            self.jump_texture = arcade.load_texture(PLAYER_FEMALE_JUMP)
            self.walk_textures = [arcade.load_texture(path) for path in PLAYER_FEMALE_WALK]

        # Initialize animation state
        self.texture = self.idle_texture
        self.facing_right = True
        self.cur_walk_frame = 0
        self._frame_time = 0.0

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Update player animation based on current state.
        
        Handles:
        - Direction detection (left/right)
        - Jump animation
        - Walk animation cycling
        - Idle state
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        # Determine facing direction based on horizontal movement
        if self.change_x < 0:
            self.facing_right = False
        elif self.change_x > 0:
            self.facing_right = True

        # Check if player is jumping (has significant vertical velocity)
        is_jumping = self.change_y > 1 or self.change_y < -1
        # Check if player is moving horizontally
        is_moving = abs(self.change_x) > 0.1

        # Show jump texture when jumping
        if is_jumping:
            self.texture = self.jump_texture
            self.flip_h = not self.facing_right
            return

        # Handle walking animation
        if is_moving:
            self._frame_time += delta_time
            # Advance to next frame when animation rate is exceeded
            if self._frame_time > ANIMATION_RATE:
                self._frame_time = 0
                self.cur_walk_frame = (self.cur_walk_frame + 1) % len(self.walk_textures)
            self.texture = self.walk_textures[self.cur_walk_frame]
            self.flip_h = not self.facing_right
        else:
            # Show idle texture when not moving
            self.texture = self.idle_texture
            self.flip_h = not self.facing_right
            self.cur_walk_frame = 0
            self._frame_time = 0