"""
This is the main file that runs the snake game.
This file also hosts the visual code for the snake game.

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
import snakecore

# --- Constants --------------------------------------------------------------------------------------------------------
SCREEN_TITLE = "Snake"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_HEADER = 50
SNAKE_SEGMENT_RADIUS = 10

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeGui(arcade.Window):
    def __init__(self):
        # Initialize the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEADER, SCREEN_TITLE)
        arcade.set_background_color( arcade.color.BLACK_OLIVE )

        # Initialize the game core
        GridWidth, GridHeight = self.CalcGrid()
        self.Core = snakecore.SnakeCore(GridWidth, GridHeight)

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw split line between header and playing field
        arcade.draw_line( 0,SCREEN_HEIGHT+1, SCREEN_WIDTH, SCREEN_HEIGHT+1, arcade.color.DUTCH_WHITE, 2)

        # Draw text fields
        try:
            score =  self.Core.GetScore()
            numMoves = self.Core.GetNumMoves()
        except:
            score = "..."
            numMoves = "..."
        arcade.draw_text("Score = " + str(score), 10, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)
        arcade.draw_text("Num moves = " + str(numMoves), 10+SCREEN_WIDTH/2, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)

        # Draw text if the game is paused or the player is dead
        try:
            dead = self.Core.GetDead()
            paused = self.Core.GetPaused()
        except:
            dead = False
            paused = False
        if dead:
            arcade.draw_text("YOU DIED!", 0, SCREEN_HEIGHT/2, arcade.color.WHITE_SMOKE, 72, width=SCREEN_WIDTH, align="center")
        elif paused:
            arcade.draw_text("GAME PAUSED!", 0, SCREEN_HEIGHT/2, arcade.color.WHITE_SMOKE, 72, width=SCREEN_WIDTH, align="center")

        # Draw snake body
        self.draw_body()

        # Draw food
        self.draw_food()

    def on_key_press(self, key, modifier):
        try:
            self.Core.KeyPressed(key)
        except:
            print("An Error occured with handling the key press.")

    def CalcGrid(self):
        width = ( SCREEN_WIDTH / SNAKE_SEGMENT_RADIUS ) - 1
        height = ( SCREEN_HEIGHT / SNAKE_SEGMENT_RADIUS ) - 1
        return width, height

    def draw_body(self):
        try:
            body = self.Core.GetBody()
        except:
            body = [[0,0]]
        for i, coor in enumerate( body ):
            color = arcade.color.WHITE_SMOKE
            if i == 0:
                color = arcade.color.GRANNY_SMITH_APPLE
            arcade.draw_circle_filled(
                coor[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                coor[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                SNAKE_SEGMENT_RADIUS / 2,
                color
            )

    def draw_food(self):
        try:
            food = self.Core.GetFood()
        except:
            food = None
        if not food == None:
            arcade.draw_circle_filled(
                food[0] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                food[1] * SNAKE_SEGMENT_RADIUS + SNAKE_SEGMENT_RADIUS / 2,
                SNAKE_SEGMENT_RADIUS / 2,
                arcade.color.WILD_WATERMELON
            )

# --- Main ------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    gui = SnakeGui()
    arcade.run()