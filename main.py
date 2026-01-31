"""
This module initializes and runs the platformer game.
It creates the main window and displays the start menu.
"""

import arcade
from src.views.start_view import StartView
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """
    Main entry point for the game.
    Creates the game window and starts the game loop.
    """
    # Create the game window with fixed size
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    
    # Create and show the start menu view
    start_view = StartView()
    window.show_view(start_view)
    
    # Start the game loop
    arcade.run()


if __name__ == "__main__":
    main()