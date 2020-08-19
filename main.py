"""
This is the main file that runs the snake game.

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
import snakegui
import snakecore

# --- Main -------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    gui = snakegui.SnakeGui()
    core = snakecore.SnakeCore(gui)
    arcade.run()