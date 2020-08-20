"""
Snake game Core code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
from enum import Enum

# --- Constants --------------------------------------------------------------------------------------------------------
SNAKE_SEGMENT_RADIUS = 5

# --- Class ------------------------------------------------------------------------------------------------------------
class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeCore():
    def __init__(self, Gui):
        self.Gui = Gui
        self.Gui.SetCore(self)
        self.width, self.height = self.Gui.GetScreenSize()
        self.CalcGrid()

        self.bodyLength = 3
        self.body = self.GenerateBody()
        self.direction = Direction.Right

        self.score = 0
        self.moves = 0

        self.UpdateGui()
        arcade.schedule( self.move, 1/20 )
        self.paused = False
        self.dead = False
        

    def CalcGrid(self):
        self.width = self.width / SNAKE_SEGMENT_RADIUS
        self.height = self.height / SNAKE_SEGMENT_RADIUS

    def GenerateBody(self):
        body = []
        while len(body) < self.bodyLength:
            coor = [self.width/2 - len(body), self.height/2]
            body.append(coor)
        return body
        
    def UpdateGui(self):
        self.Gui.SetBody(self.body)
        self.Gui.SetScore(self.score)
        self.Gui.SetMoves(self.moves)
        self.Gui.SetSnakeSegmentRadius(SNAKE_SEGMENT_RADIUS)

    def move(self, time):
        if not self.paused and not self.dead:
            new_body = []
            if self.direction == Direction.Right:
                new_body.append( [ self.body[0][0]+1, self.body[0][1] ] )
            elif self.direction == Direction.Left:
                new_body.append( [ self.body[0][0]-1, self.body[0][1] ] )
            elif self.direction == Direction.Up:
                new_body.append( [ self.body[0][0], self.body[0][1]+1 ] )
            elif self.direction == Direction.Down:
                new_body.append( [ self.body[0][0], self.body[0][1]-1 ] )

            for i, _ in enumerate( self.body ):
                if not i == 0:
                    new_body.append( self.body[i-1] )

            if new_body[0][0] <= 0 or new_body [0][0] >= self.width:
                new_body = self.body
                self.YouDied()

            if new_body[0][1] <= 0 or new_body [0][1] >= self.height:
                new_body = self.body
                self.YouDied()

            self.moves += 1

            self.body = new_body
        self.UpdateGui()

    def KeyPressed(self, key):
        if key == arcade.key.UP and not self.direction == Direction.Down:
            self.direction = Direction.Up
        elif key == arcade.key.DOWN and not self.direction == Direction.Up:
            self.direction = Direction.Down
        elif key == arcade.key.RIGHT and not self.direction == Direction.Left:
            self.direction = Direction.Right
        elif key == arcade.key.LEFT and not self.direction == Direction.Right:
            self.direction = Direction.Left

        if key == arcade.key.P:
            self.paused = False if self.paused else True

        if key == arcade.key.ENTER:
            self.score = 0
            self.moves = 0
            self.body = self.GenerateBody()
            self.direction = Direction.Right
            self.dead = False
            self.Gui.SetDead()

    def YouDied(self):
        self.dead = True
        self.Gui.SetDead()