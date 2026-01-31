"""
Animated Game Over Screen with particle effects

This module defines the GameOverView class which displays:
- Win/lose screen with different color schemes
- Animated particle effects
- Game statistics (level name, coins collected)
- Pulsing title text
- Return to menu option
"""

import arcade
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverView(arcade.View):
    """
    Game over screen displayed when player wins or loses.
    
    Features animated particles, gradient background, and displays
    game statistics. Player can return to start menu.
    """
    
    def __init__(self, did_win: bool, score: int, level_name: str):
        """
        Initialize the game over view.
        
        Args:
            did_win (bool): True if player won, False if lost
            score (int): Number of coins collected
            level_name (str): Name of the level that was completed/failed
        """
        super().__init__()
        self.did_win = did_win
        self.score = score
        self.level_name = level_name
        self.time = 0.0  # Time accumulator for animations
        self.particles = []  # List of particle dictionaries
        
        # Create 50 random particles for visual effects
        for _ in range(50):
            max_life = random.uniform(1.0, 3.0)
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.randint(-50, 50),  # Horizontal velocity
                'vy': random.randint(-50, 50),  # Vertical velocity
                'life': max_life,  # Start with full life
                'max_life': max_life,  # Maximum lifetime
                'size': random.randint(2, 6)  # Particle size
            })

    def on_show(self):
        """
        Called when this view is shown.
        Sets background color based on win/lose state.
        """
        if self.did_win:
            arcade.set_background_color((20, 20, 60))  # Dark blue for victory
        else:
            arcade.set_background_color((60, 20, 20))  # Dark red for defeat

    def on_draw(self):
        self.clear()
        
        if self.did_win:
            colors = [(40, 20, 80), (30, 15, 70), (20, 10, 60), (10, 5, 50)]
        else:
            colors = [(80, 30, 30), (70, 25, 25), (60, 20, 20), (50, 15, 15)]
        
        for i in range(4):
            y = SCREEN_HEIGHT - i * (SCREEN_HEIGHT / 4)
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, y - SCREEN_HEIGHT / 4, y, colors[i]
            )
        
        for p in self.particles:
            # Clamp alpha to valid range (0-255)
            life_ratio = max(0.0, min(1.0, p['life'] / p['max_life'] if p['max_life'] > 0 else 0.0))
            alpha = int(life_ratio * 255)
            alpha = max(0, min(255, alpha))  # Ensure alpha is in valid range
            if self.did_win:
                color = (255, 255, 0, alpha)
            else:
                color = (255, 100, 0, alpha)
            arcade.draw_circle_filled(p['x'], p['y'], p['size'], color)
        
        title = "🎉 VICTORY! 🎉" if self.did_win else "💔 GAME OVER 💔"
        title_color = arcade.color.GOLD if self.did_win else arcade.color.RED
        
        pulse = 1.0 + 0.1 * abs(int(self.time * 4) % 2)
        shadow_size = int(48 * pulse) + 2
        
        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2 + 4,
            SCREEN_HEIGHT * 0.65 - 4,
            (0, 0, 0, 150),
            font_size=shadow_size,
            anchor_x="center",
            bold=True,
        )
        
        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.65,
            title_color,
            font_size=int(48 * pulse),
            anchor_x="center",
            bold=True,
        )
        
        if self.did_win:
            message = "You collected all coins and reached the goal!"
            msg_color = arcade.color.YELLOW
        else:
            message = "Better luck next time, adventurer!"
            msg_color = arcade.color.ORANGE
        
        arcade.draw_text(
            message,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.55,
            msg_color,
            font_size=20,
            anchor_x="center",
            italic=True,
        )
        
        box_y = SCREEN_HEIGHT * 0.4
        box_width = 500
        box_height = 120
        
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH / 2 - box_width / 2,
            SCREEN_WIDTH / 2 + box_width / 2,
            box_y - box_height / 2,
            box_y + box_height / 2,
            (255, 255, 255, 200)
        )
        
        arcade.draw_lrbt_rectangle_outline(
            SCREEN_WIDTH / 2 - box_width / 2,
            SCREEN_WIDTH / 2 + box_width / 2,
            box_y - box_height / 2,
            box_y + box_height / 2,
            title_color,
            4
        )
        
        arcade.draw_text(
            f"📍 Level: {self.level_name}",
            SCREEN_WIDTH / 2,
            box_y + 30,
            arcade.color.BLACK,
            font_size=22,
            anchor_x="center",
            bold=True,
        )
        
        arcade.draw_text(
            f"🪙 Coins Collected: {self.score}",
            SCREEN_WIDTH / 2,
            box_y - 10,
            arcade.color.ORANGE,
            font_size=20,
            anchor_x="center",
            bold=True,
        )
        
        if int(self.time * 2) % 2:
            arcade.draw_text(
                "Press ENTER to return to menu",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT * 0.2,
                arcade.color.WHITE,
                font_size=22,
                anchor_x="center",
                bold=True,
            )
        
        if self.did_win:
            for i in range(4):
                star_x = SCREEN_WIDTH / 2 + random.randint(-200, 200)
                star_y = SCREEN_HEIGHT * 0.8 + random.randint(-50, 50)
                star_size = 3 + int(self.time * 10) % 3
                arcade.draw_text(
                    "⭐",
                    star_x,
                    star_y,
                    arcade.color.YELLOW,
                    font_size=star_size * 10,
                )

    def on_update(self, delta_time: float):
        self.time += delta_time
        
        for p in self.particles:
            p['x'] += p['vx'] * delta_time
            p['y'] += p['vy'] * delta_time
            p['life'] -= delta_time
            
            if p['life'] <= 0:
                p['x'] = random.randint(0, SCREEN_WIDTH)
                p['y'] = random.randint(0, SCREEN_HEIGHT)
                p['max_life'] = random.uniform(1.0, 3.0)
                p['life'] = p['max_life']  # Start with full life
            
            if p['x'] < 0 or p['x'] > SCREEN_WIDTH:
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > SCREEN_HEIGHT:
                p['vy'] *= -1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from src.views.start_view import StartView
            start_view = StartView()
            self.window.show_view(start_view)