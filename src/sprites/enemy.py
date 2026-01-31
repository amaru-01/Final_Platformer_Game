"""
Patrolling enemy sprite

This module defines the EnemySprite class which handles:
- Enemy positioning and movement
- Patrol behavior (moving back and forth between boundaries)
"""

import arcade
from config import ENEMY_TEXTURE, ENEMY_SCALING


class EnemySprite(arcade.Sprite):
    """
    Enemy sprite that patrols between two x-coordinates.
    
    The enemy moves horizontally back and forth, reversing direction
    when it reaches the patrol boundaries.
    """
    
    def __init__(self, spec):
        """
        Initialize the enemy sprite.
        
        Args:
            spec (dict): Dictionary containing:
                - "position": (x, y) tuple for starting position
                - "patrol_min_x": Left boundary of patrol area
                - "patrol_max_x": Right boundary of patrol area
                - "speed": Horizontal movement speed
        """
        super().__init__(ENEMY_TEXTURE, scale=ENEMY_SCALING)
        self.center_x, self.center_y = spec["position"]
        self.patrol_min_x = spec["patrol_min_x"]
        self.patrol_max_x = spec["patrol_max_x"]
        self.change_x = spec["speed"]

    def update(self, delta_time: float = 1 / 60):
        """
        Update enemy position and handle patrol boundaries.
        
        Moves the enemy horizontally and reverses direction when
        it reaches the patrol boundaries.
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        # Move enemy horizontally
        self.center_x += self.change_x
        
        # Reverse direction if enemy reaches left boundary
        if self.center_x < self.patrol_min_x:
            self.center_x = self.patrol_min_x
            self.change_x *= -1
        # Reverse direction if enemy reaches right boundary
        elif self.center_x > self.patrol_max_x:
            self.center_x = self.patrol_max_x
            self.change_x *= -1