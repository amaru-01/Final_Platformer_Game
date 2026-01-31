"""
Main Game View 

This module defines the GameView class which handles:
- Level setup and rendering
- Player movement and physics
- Collision detection (coins, enemies, hazards, goal)
- Health and scoring system
- Level progression
- Sound effects and background music
"""

import arcade
from config import *
from src.sprites.player import PlayerSprite
from src.sprites.enemy import EnemySprite
from src.sprites.hazards import LavaHazard, WaterHazard
from src.levels.level_data import LEVELS


class GameView(arcade.View):
    """
    Main game view that handles all gameplay mechanics.
    
    Manages player movement, collisions, level progression,
    and game state (health, score, etc.).
    """
    
    def __init__(self, gender="female"):
        """
        Initialize the game view.
        
        Args:
            gender (str): "male" or "female" character selection
        """
        super().__init__()
        
        # Character selection
        self.gender = gender
        
        # Scene and physics
        self.scene = arcade.Scene()  # Container for all sprites
        self.player = None  # Player sprite
        self.physics_engine = None  # Physics engine for platformer mechanics
        
        # Game state
        self.level_index = 0  # Current level (0-indexed)
        self.score = 0  # Coins collected
        self.health = PLAYER_MAX_HEALTH  # Player health (hearts)
        self.total_coins = 0  # Total coins in current level
        self.level_name = ""  # Current level name
        self.invuln_timer = 0.0  # Invulnerability timer after taking damage
        
        # Sound effects and music
        self.coin_sound = None
        self.jump_sound = None
        self.hit_sound = None
        self.win_sound = None
        self.lose_sound = None
        self.music_player = None  # Background music player
        
        # Input state
        self.move_left = False
        self.move_right = False

    def setup(self, level_index: int = 0):
        """
        Set up a level with all sprites and game objects.
        
        Creates the scene, places all level elements (ground, platforms,
        coins, enemies, hazards, goal), and initializes the physics engine.
        
        Args:
            level_index (int): Index of the level to load (0-based)
        """
        self.level_index = level_index
        
        # Create new scene with sprite lists
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)  # Spatial hash for collision optimization
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("Goal")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Hazards")

        # Load level data
        level = LEVELS[level_index]
        self.level_name = level["name"]

        # Create and position player
        self.player = PlayerSprite(self.gender)
        self.player.center_x, self.player.center_y = level["player_start"]
        self.scene.add_sprite("Player", self.player)

        # Create ground segments (continuous ground tiles)
        for start_x, end_x, y in level["ground_segments"]:
            for x in range(start_x, end_x, 64):  # 64 pixel tile spacing
                ground = arcade.Sprite(GROUND_TEXTURE, TILE_SCALING)
                ground.center_x = x
                ground.center_y = y
                self.scene.add_sprite("Walls", ground)

        # Create platforms (individual platform tiles)
        for x, y in level["platforms"]:
            platform = arcade.Sprite(PLATFORM_TEXTURE, TILE_SCALING)
            platform.center_x = x
            platform.center_y = y
            self.scene.add_sprite("Walls", platform)

        # Create coins (collectibles)
        for x, y in level["coins"]:
            coin = arcade.Sprite(COIN_TEXTURE, COIN_SCALING)
            coin.center_x = x
            coin.center_y = y
            self.scene.add_sprite("Coins", coin)
        self.total_coins = len(level["coins"])

        # Create goal flag (exit point)
        goal = arcade.Sprite(FLAG_TEXTURE, TILE_SCALING * 1.5)
        goal.center_x, goal.center_y = level["goal_position"]
        self.scene.add_sprite("Goal", goal)

        # Create enemies with patrol behavior
        for enemy_spec in level["enemies"]:
            enemy = EnemySprite(enemy_spec)
            self.scene.add_sprite("Enemies", enemy)
        
        # Create hazards (lava and water)
        for hazard_spec in level.get("hazards", []):
            if hazard_spec["type"] == "lava":
                hazard = LavaHazard(hazard_spec["position"], hazard_spec["width"])
            else:
                hazard = WaterHazard(hazard_spec["position"], hazard_spec["width"])
            self.scene.add_sprite("Hazards", hazard)

        # Initialize physics engine for platformer mechanics
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.scene["Walls"],
            gravity_constant=GRAVITY,
        )

        # Reset game state only on first level
        self.score = 0 if level_index == 0 else self.score
        self.health = PLAYER_MAX_HEALTH if level_index == 0 else self.health
        self.invuln_timer = 0.0
        
        # Load sound effects (only once)
        if self.coin_sound is None:
            try:
                self.coin_sound = arcade.load_sound(COIN_SOUND)
                self.jump_sound = arcade.load_sound(JUMP_SOUND)
                self.hit_sound = arcade.load_sound(HIT_SOUND)
                self.win_sound = arcade.load_sound(WIN_SOUND)
                self.lose_sound = arcade.load_sound(LOSE_SOUND)
            except:
                pass  # Silently fail if sounds can't be loaded
        
        # Start background music (only on first level)
        if level_index == 0 and self.music_player is None:
            try:
                music = arcade.load_sound(BACKGROUND_MUSIC, streaming=True)
                self.music_player = arcade.play_sound(music, volume=0.3, loop=True)
            except:
                pass  # Silently fail if music can't be loaded

    def on_draw(self):
        self.clear()
        self.scene.draw()
        
        self._draw_hud()

    def _draw_hud(self):
        hud_y = SCREEN_HEIGHT - 40
        
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, hud_y, SCREEN_HEIGHT,
            (40, 40, 60, 230)
        )
        
        heart_x = 20
        for i in range(PLAYER_MAX_HEALTH):
            if i < self.health:
                color = arcade.color.RED
                symbol = "❤️"
            else:
                color = (100, 100, 100)
                symbol = "🖤"
            
            arcade.draw_text(
                symbol,
                heart_x + i * 40,
                hud_y + 8,
                color,
                font_size=24,
            )
        
        coin_x = 200
        arcade.draw_text(
            f"🪙 {self.score}/{self.total_coins}",
            coin_x,
            hud_y + 10,
            arcade.color.YELLOW,
            font_size=20,
            bold=True,
        )
        
        level_x = SCREEN_WIDTH - 250
        arcade.draw_text(
            f"📍 Level: {self.level_name}",
            level_x,
            hud_y + 10,
            arcade.color.WHITE,
            font_size=18,
        )

    def _handle_input(self):
        if not self.player:
            return
        dx = 0
        if self.move_left:
            dx -= PLAYER_MOVE_SPEED
        if self.move_right:
            dx += PLAYER_MOVE_SPEED
        self.player.change_x = dx

    def _check_coin_collisions(self):
        if not self.player:
            return
        
        coins_hit = arcade.check_for_collision_with_list(
            self.player, self.scene["Coins"]
        )
        
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
            
            if self.coin_sound:
                try:
                    arcade.play_sound(self.coin_sound, volume=0.5)
                except:
                    pass

    def _check_enemy_collisions(self, delta_time: float):
        if not self.player:
            return
        
        self.invuln_timer = max(0.0, self.invuln_timer - delta_time)
        
        if self.invuln_timer > 0:
            return
        
        hits = arcade.check_for_collision_with_list(self.player, self.scene["Enemies"])
        
        if hits:
            self.health -= 1
            self.invuln_timer = 1.0
            
            self.player.change_y = PLAYER_JUMP_SPEED / 2
            self.player.change_x *= -1
            
            if self.hit_sound:
                try:
                    arcade.play_sound(self.hit_sound, volume=0.7)
                except:
                    pass
    
    def _check_hazard_collisions(self, delta_time: float):
        if not self.player or self.invuln_timer > 0:
            return
        
        hazards_hit = arcade.check_for_collision_with_list(
            self.player, self.scene["Hazards"]
        )
        
        if hazards_hit:
            self.health -= 1
            self.invuln_timer = 1.0
            
            self.player.change_y = PLAYER_JUMP_SPEED / 1.5
            
            if self.hit_sound:
                try:
                    arcade.play_sound(self.hit_sound, volume=0.7)
                except:
                    pass

    def _check_goal(self):
        if not self.player:
            return False
        
        goal_list = self.scene["Goal"]
        if goal_list and arcade.check_for_collision(self.player, goal_list[0]):
            if self.score >= self.total_coins:
                return True
        return False

    def _check_lose(self):
        if not self.player:
            return True
        
        if self.health <= 0:
            return True
        
        level = LEVELS[self.level_index]
        if self.player.center_y < level.get("kill_plane_y", KILL_PLANE_Y):
            return True
        
        return False

    def on_update(self, delta_time: float):
        if not self.physics_engine or not self.player:
            return

        self._handle_input()
        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.scene["Enemies"].update()
        # Update hazard animations individually
        for hazard in self.scene["Hazards"]:
            hazard.update_animation(delta_time)
        
        self._check_coin_collisions()
        self._check_enemy_collisions(delta_time)
        self._check_hazard_collisions(delta_time)

        if self._check_lose():
            from src.views.game_over_view import GameOverView
            if self.music_player:
                try:
                    arcade.stop_sound(self.music_player)
                except:
                    pass
            if self.lose_sound:
                try:
                    arcade.play_sound(self.lose_sound, volume=0.8)
                except:
                    pass
            game_over = GameOverView(False, self.score, self.level_name)
            self.window.show_view(game_over)
            return

        if self._check_goal():
            from src.views.game_over_view import GameOverView
            if self.win_sound:
                try:
                    arcade.play_sound(self.win_sound, volume=0.8)
                except:
                    pass
            
            if self.level_index + 1 < len(LEVELS):
                self.level_index += 1
                self.setup(level_index=self.level_index)
            else:
                if self.music_player:
                    try:
                        arcade.stop_sound(self.music_player)
                    except:
                        pass
                game_over = GameOverView(True, self.score, self.level_name)
                self.window.show_view(game_over)

    def on_key_press(self, key, modifiers):
        if not self.player or not self.physics_engine:
            return

        if key in (arcade.key.A, arcade.key.LEFT):
            self.move_left = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.move_right = True
        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                if self.jump_sound:
                    try:
                        arcade.play_sound(self.jump_sound, volume=0.4)
                    except:
                        pass

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.move_left = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.move_right = False