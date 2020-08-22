"""
Snake game Core code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
import enum

# --- Constants --------------------------------------------------------------------------------------------------------
SNAKE_LENGTH = 3

# --- Class ------------------------------------------------------------------------------------------------------------
class Direction(enum.Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeCore():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.score = 0
        self.numMoves = 0

        self.body = self.GenerateBody()

    # Getters
    def GetScore(self):
        return self.score
    
    def GetNumMoves(self):
        return self.numMoves

    def GetBody(self):
        return self.body

    def GenerateBody(self):
        body = []
        while len(body) < SNAKE_LENGTH:
            x = int( self.width / 2  - len(body) )
            y = int( self.height / 2 )
            coor = [x, y]
            body.append(coor)
        return body