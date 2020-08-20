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
SCREEN_HEADER = 50

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeGui(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEADER, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK_OLIVE) 

        self.body = [[0,0]]
        self.score = 0
        self.moves = 0
        self.Snake_Segment_Radius = 0
        self.dead = False
        
    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw horizontal line
        arcade.draw_line( 0, SCREEN_HEIGHT+1, SCREEN_WIDTH, SCREEN_HEIGHT+1, arcade.color.DUTCH_WHITE, 2 )

        # Draw text fields
        arcade.draw_text("Score = " + str(self.score), 10, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)
        arcade.draw_text("Num moves = " + str(self.moves), 10+SCREEN_WIDTH/2, SCREEN_HEIGHT + SCREEN_HEADER/4, arcade.color.WHITE_SMOKE, 24)

        self.FlagDead()

        # Draw snake body
        self.draw_body()

    def draw_body(self):
        try:
            for i, coordinates in enumerate( self.body ):
                color = arcade.color.WHITE_SMOKE
                if i == 0:
                    color = arcade.color.WILD_WATERMELON
                arcade.draw_circle_filled(
                    coordinates[0]*self.Snake_Segment_Radius, coordinates[1]*self.Snake_Segment_Radius, self.Snake_Segment_Radius, color
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

    def SetCore(self, core):
        self.Core = core

    def SetScore(self, score):
        self.score = score

    def SetMoves(self, moves):
        self.moves = moves

    def SetDead(self):
        self.dead = False if self.dead else True

    def GetScreenSize(self):
        return SCREEN_WIDTH, SCREEN_HEIGHT

    def FlagDead(self):
        if self.dead:
            arcade.draw_text("YOU DIED!", 0, SCREEN_HEIGHT/2, arcade.color.WHITE_SMOKE, 72, width=SCREEN_WIDTH, align="center")