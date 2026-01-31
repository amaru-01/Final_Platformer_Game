"""
This module defines the StartView class which displays:
- Animated background with gradient colors
- Floating particle effects
- Game title with shadow effect
- Instructions and controls
- Pulsing start prompt
"""

import arcade
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class StartView(arcade.View):
    """
    Start menu view with animated background and particle effects.
    
    Displays game title, instructions, and waits for user input
    to proceed to character selection.
    """
    
    def __init__(self):
        """Initialize the start view with particle effects."""
        super().__init__()
        self.time = 0.0  # Time accumulator for animations
        self.particles = []  # List of particle dictionaries for visual effects
        
        # Create 20 random particles for background animation
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': 20 + random.randint(0, 30),  # Random upward speed
                'size': 2 + random.randint(0, 3)  # Random particle size
            })

    def on_show(self):
        """Called when this view is shown. Sets the background color."""
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        """
        Draw the start menu screen.
        
        Renders:
        - Gradient background (5 layers of blue shades)
        - Floating particles
        - Game title with animated shadow
        - Instructions box
        - Pulsing start prompt
        - Decorative corner elements
        """
        self.clear()
        
        # Draw gradient background (5 horizontal bands)
        for i in range(5):
            y = SCREEN_HEIGHT - i * (SCREEN_HEIGHT / 5)
            height = SCREEN_HEIGHT / 5
            colors = [
                (135, 206, 250),  # Light sky blue
                (100, 180, 255),  # Medium sky blue
                (70, 150, 255),   # Sky blue
                (50, 120, 255),   # Deep sky blue
                (30, 90, 255)     # Darker blue
            ]
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, y - height, y, colors[i]
            )
        
        # Draw floating particles
        for p in self.particles:
            arcade.draw_circle_filled(p['x'], p['y'], p['size'], 
                                     (255, 255, 255, 150))
        
        # Draw game title with animated shadow effect
        title_y = SCREEN_HEIGHT * 0.7
        
        # Animated shadow offset for depth effect
        shadow_offset = 4 + abs(int(self.time * 2) % 3)
        arcade.draw_text(
            "PLATFORMER ADVENTURE",
            SCREEN_WIDTH / 2 + shadow_offset,
            title_y - shadow_offset,
            (0, 0, 0, 100),  # Semi-transparent black shadow
            font_size=54,
            anchor_x="center",
            bold=True,
        )
        
        # Main title text
        arcade.draw_text(
            "PLATFORMER ADVENTURE",
            SCREEN_WIDTH / 2,
            title_y,
            arcade.color.YELLOW,
            font_size=54,
            anchor_x="center",
            bold=True,
        )
        
        # Subtitle
        arcade.draw_text(
            "Enhanced Edition",
            SCREEN_WIDTH / 2,
            title_y - 60,
            arcade.color.ORANGE,
            font_size=24,
            anchor_x="center",
            italic=True,
        )
        
        # Draw instructions box
        box_y = SCREEN_HEIGHT * 0.4
        box_width = 600
        box_height = 200
        
        # White semi-transparent background box
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH / 2 - box_width / 2,
            SCREEN_WIDTH / 2 + box_width / 2,
            box_y - box_height / 2,
            box_y + box_height / 2,
            (255, 255, 255, 220)
        )
        
        # Orange border around box
        arcade.draw_lrbt_rectangle_outline(
            SCREEN_WIDTH / 2 - box_width / 2,
            SCREEN_WIDTH / 2 + box_width / 2,
            box_y - box_height / 2,
            box_y + box_height / 2,
            arcade.color.ORANGE,
            4
        )
        
        # Instruction text lines
        instructions = [
            ("🎮 CONTROLS 🎮", arcade.color.ORANGE, 20, True),
            ("Arrow Keys / WASD - Move", arcade.color.BLACK, 16, False),
            ("Space - Jump", arcade.color.BLACK, 16, False),
            ("", arcade.color.BLACK, 16, False),
            ("🎯 OBJECTIVE 🎯", arcade.color.ORANGE, 20, True),
            ("Collect all coins 🪙 and reach the flag 🚩", arcade.color.BLACK, 16, False),
            ("Avoid enemies and hazards - 3 hits max! ❤️", arcade.color.RED, 16, False),
        ]
        
        # Draw each instruction line
        y_offset = box_y + 70
        for line, color, size, bold in instructions:
            arcade.draw_text(
                line,
                SCREEN_WIDTH / 2,
                y_offset,
                color,
                font_size=size,
                anchor_x="center",
                bold=bold,
            )
            y_offset -= 26
        
        # Pulsing start prompt with glow effect
        pulse = abs(int(self.time * 3) % 2)
        if pulse:
            glow_size = 26 + int(self.time * 5) % 4
            arcade.draw_text(
                "Press ENTER or SPACE to Start",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT * 0.15,
                arcade.color.WHITE,
                font_size=glow_size,
                anchor_x="center",
                bold=True,
            )
        
        # Main start prompt text
        arcade.draw_text(
            "Press ENTER or SPACE to Start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.15,
            arcade.color.YELLOW,
            font_size=24,
            anchor_x="center",
            bold=True,
        )
        
        # Decorative orange corners
        corner_size = 40
        arcade.draw_lrbt_rectangle_filled(
            0, corner_size, SCREEN_HEIGHT - corner_size, SCREEN_HEIGHT, 
            arcade.color.ORANGE
        )
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - corner_size, SCREEN_WIDTH, 
            SCREEN_HEIGHT - corner_size, SCREEN_HEIGHT, 
            arcade.color.ORANGE
        )
        arcade.draw_lrbt_rectangle_filled(
            0, corner_size, 0, corner_size, arcade.color.ORANGE
        )
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - corner_size, SCREEN_WIDTH, 0, corner_size, 
            arcade.color.ORANGE
        )

    def on_update(self, delta_time: float):
        """
        Update animation state and particle positions.
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        self.time += delta_time
        
        # Update particle positions (move upward)
        for p in self.particles:
            p['y'] += p['speed'] * delta_time
            # Reset particle to bottom when it goes off screen
            if p['y'] > SCREEN_HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, SCREEN_WIDTH)

    def on_key_press(self, key, modifiers):
        """
        Handle key press events.
        
        Transitions to character selection screen when ENTER or SPACE is pressed.
        
        Args:
            key: The key that was pressed
            modifiers: Key modifiers (shift, ctrl, etc.)
        """
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            # Import here to avoid circular import
            from src.views.character_select import CharacterSelectView
            char_select = CharacterSelectView()
            self.window.show_view(char_select)