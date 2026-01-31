"""
Hazard sprites - Lava and Water that damage the player

This module defines hazard sprites that damage the player on contact.
Hazards have animated effects to make them visually distinct.
"""

import arcade
from config import LAVA_TEXTURE, WATER_TEXTURE, HAZARD_SCALING


class LavaHazard(arcade.Sprite):
    """
    Lava hazard that damages the player on contact.
    
    Features a pulsing alpha animation to create a glowing effect.
    """
    
    def __init__(self, position, width=128):
        """
        Initialize the lava hazard.
        
        Args:
            position (tuple): (x, y) coordinates for hazard position
            width (int): Width of the hazard sprite
        """
        super().__init__(LAVA_TEXTURE, scale=HAZARD_SCALING)
        self.center_x, self.center_y = position
        self.width = width
        self.time = 0.0
        self.base_y = position[1]
        
    def update_animation(self, delta_time: float):
        """
        Update lava animation with pulsing alpha effect.
        
        Creates a glowing effect by oscillating the alpha value
        between 200 and 255.
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        self.time += delta_time
        # Pulse alpha between 200 and 255 for glowing effect
        self.alpha = int(200 + 55 * abs(int(self.time * 4) % 2))


class WaterHazard(arcade.Sprite):
    """
    Water hazard that damages the player on contact.
    
    Features a vertical bobbing animation to simulate water movement.
    """
    
    def __init__(self, position, width=128):
        """
        Initialize the water hazard.
        
        Args:
            position (tuple): (x, y) coordinates for hazard position
            width (int): Width of the hazard sprite
        """
        super().__init__(WATER_TEXTURE, scale=HAZARD_SCALING)
        self.center_x, self.center_y = position
        self.width = width
        self.time = 0.0
        self.base_y = position[1]
        
    def update_animation(self, delta_time: float):
        """
        Update water animation with vertical bobbing effect.
        
        Creates a wave-like motion by oscillating the y position
        up and down from the base position.
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        self.time += delta_time
        # Create bobbing effect by offsetting y position
        offset = int(3 * (self.time * 2) % 2)
        self.center_y = self.base_y + offset