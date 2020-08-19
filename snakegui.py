"""
Snake game Visualization code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade

# --- Constants --------------------------------------------------------------------------------------------------------
SCREEN_TITLE = "Snake"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeGui(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK_OLIVE) 

        self.body = [[0,0]]
        self.Snake_Segment_Radius = 0
        
    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw snake body
        self.draw_body()

    def draw_body(self):
        try:
            for i, coordinates in enumerate( self.body ):
                color = arcade.color.WHITE_SMOKE
                if i == 0:
                    color = arcade.color.WILD_WATERMELON
                arcade.draw_circle_filled(
                    coordinates[0], coordinates[1], self.Snake_Segment_Radius, color
                )
        except:
            print("An error occured when rendering the snake body.")

    def on_key_press(self, key, modifier):
        try:
            self.Core.KeyPressed(key)
        except:
            print("An error occured with handling the key press.")

    def SetBody(self, body):
        self.body = body

    def SetSnakeSegmentRadius(self, x):
        self.Snake_Segment_Radius = x

    def GetScreenSize(self):
        return SCREEN_WIDTH, SCREEN_HEIGHT