"""
Character Selection Screen - Choose Male or Female Adventurer

This module defines the CharacterSelectView class which allows players
to choose between male and female character models before starting the game.
"""

import arcade
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_MALE_IDLE, PLAYER_FEMALE_IDLE
)


class CharacterSelectView(arcade.View):
    """
    Character selection screen with visual character previews.
    
    Players can use arrow keys to select between male and female characters,
    then press ENTER or SPACE to confirm and start the game.
    """
    
    def __init__(self):
        """Initialize the character selection view."""
        super().__init__()
        self.selected = 0  # 0 = male, 1 = female
        self.time = 0.0  # Time accumulator for animations
        
        # Load character preview textures
        self.male_texture = arcade.load_texture(PLAYER_MALE_IDLE)
        self.female_texture = arcade.load_texture(PLAYER_FEMALE_IDLE)

    def on_show(self):
        """Called when this view is shown. Sets the background color."""
        arcade.set_background_color((50, 50, 100))  # Dark blue-purple

    def on_draw(self):
        """
        Draw the character selection screen.
        
        Renders:
        - Gradient background
        - Title text
        - Two character selection boxes (male/female)
        - Glowing selection indicator
        - Character preview sprites
        - Instructions
        """
        self.clear()
        
        # Draw gradient background (4 horizontal bands)
        for i in range(4):
            y = SCREEN_HEIGHT - i * (SCREEN_HEIGHT / 4)
            colors = [
                (80, 60, 120),   # Light purple
                (70, 50, 110),   # Medium purple
                (60, 40, 100),   # Purple
                (50, 30, 90)     # Dark purple
            ]
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, y - SCREEN_HEIGHT / 4, y, colors[i]
            )
        
        # Title text
        arcade.draw_text(
            "SELECT YOUR CHARACTER",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.85,
            arcade.color.YELLOW,
            font_size=42,
            anchor_x="center",
            bold=True,
        )
        
        # Character positions
        male_x = SCREEN_WIDTH * 0.3
        female_x = SCREEN_WIDTH * 0.7
        char_y = SCREEN_HEIGHT * 0.5
        
        # Draw glowing selection indicator for male character
        if self.selected == 0:
            glow = 10 + abs(int(self.time * 8) % 10)  # Pulsing glow effect
            arcade.draw_circle_filled(male_x, char_y, 120 + glow, 
                                     (255, 255, 0, 50))  # Yellow glow
            arcade.draw_circle_outline(male_x, char_y, 130, 
                                      arcade.color.YELLOW, 5)
        
        # Male character box
        arcade.draw_lrbt_rectangle_filled(
            male_x - 100, male_x + 100, char_y - 100, char_y + 100,
            (255, 255, 255, 200)  # White semi-transparent background
        )
        arcade.draw_lrbt_rectangle_outline(
            male_x - 100, male_x + 100, char_y - 100, char_y + 100,
            arcade.color.YELLOW if self.selected == 0 else arcade.color.WHITE,
            3
        )
        
        # Draw male character texture using a temporary sprite
        male_sprite = arcade.Sprite()
        male_sprite.texture = self.male_texture
        male_sprite.scale = 3.0
        male_sprite.center_x = male_x
        male_sprite.center_y = char_y
        temp_list = arcade.SpriteList()
        temp_list.append(male_sprite)
        temp_list.draw()
        
        # Male label
        arcade.draw_text(
            "MALE",
            male_x,
            char_y - 150,
            arcade.color.YELLOW if self.selected == 0 else arcade.color.WHITE,
            font_size=28,
            anchor_x="center",
            bold=True,
        )
        
        # Draw glowing selection indicator for female character
        if self.selected == 1:
            glow = 10 + abs(int(self.time * 8) % 10)  # Pulsing glow effect
            arcade.draw_circle_filled(female_x, char_y, 120 + glow, 
                                     (255, 0, 255, 50))  # Pink glow
            arcade.draw_circle_outline(female_x, char_y, 130, 
                                      arcade.color.PINK, 5)
        
        # Female character box
        arcade.draw_lrbt_rectangle_filled(
            female_x - 100, female_x + 100, char_y - 100, char_y + 100,
            (255, 255, 255, 200)  # White semi-transparent background
        )
        arcade.draw_lrbt_rectangle_outline(
            female_x - 100, female_x + 100, char_y - 100, char_y + 100,
            arcade.color.PINK if self.selected == 1 else arcade.color.WHITE,
            3
        )
        
        # Draw female character texture using a temporary sprite
        female_sprite = arcade.Sprite()
        female_sprite.texture = self.female_texture
        female_sprite.scale = 3.0
        female_sprite.center_x = female_x
        female_sprite.center_y = char_y
        temp_list = arcade.SpriteList()
        temp_list.append(female_sprite)
        temp_list.draw()
        
        # Female label
        arcade.draw_text(
            "FEMALE",
            female_x,
            char_y - 150,
            arcade.color.PINK if self.selected == 1 else arcade.color.WHITE,
            font_size=28,
            anchor_x="center",
            bold=True,
        )
        
        # Instructions
        arcade.draw_text(
            "Use LEFT/RIGHT arrows to select",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.2,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )
        
        arcade.draw_text(
            "Press ENTER or SPACE to confirm",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.15,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center",
            bold=True,
        )

    def on_update(self, delta_time: float):
        """
        Update animation state.
        
        Args:
            delta_time (float): Time elapsed since last frame
        """
        self.time += delta_time

    def on_key_press(self, key, modifiers):
        """
        Handle key press events.
        
        LEFT/A selects male, RIGHT/D selects female.
        ENTER/SPACE confirms selection and starts the game.
        
        Args:
            key: The key that was pressed
            modifiers: Key modifiers (shift, ctrl, etc.)
        """
        if key in (arcade.key.LEFT, arcade.key.A):
            self.selected = 0  # Select male
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.selected = 1  # Select female
        elif key in (arcade.key.ENTER, arcade.key.SPACE):
            # Import here to avoid circular import
            from src.views.game_view import GameView
            gender = "male" if self.selected == 0 else "female"
            game_view = GameView(gender)
            game_view.setup(level_index=0)
            self.window.show_view(game_view)