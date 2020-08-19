"""
Snake game Core code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade

# --- Constants --------------------------------------------------------------------------------------------------------
SNAKE_SEGMENT_RADIUS = 5
SNAKE_SEGMENT_SPACING = SNAKE_SEGMENT_RADIUS * 4/3

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeCore():
    def __init__(self, Gui):
        self.Gui = Gui
        self.width, self.height = self.Gui.GetScreenSize()
        self.bodyLength = 3
        self.body = self.GenerateBody()
        self.UpdateGui()

    def GenerateBody(self):
        body = []
        while len(body) < self.bodyLength:
            coor = [self.width/2 - len(body)*SNAKE_SEGMENT_SPACING, self.height/2]
            body.append(coor)
        return body
        
    def UpdateGui(self):
        self.Gui.SetBody(self.body)
        self.Gui.SetSnakeSegmentRadius(SNAKE_SEGMENT_RADIUS)
