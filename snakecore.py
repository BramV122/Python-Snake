"""
Snake game Core code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
from enum import Enum
import random
import math

# --- Constants --------------------------------------------------------------------------------------------------------
SNAKE_SEGMENT_RADIUS = 10

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
        self.Gui.SetSnakeSegmentRadius(SNAKE_SEGMENT_RADIUS)
        self.width, self.height = self.Gui.GetScreenSize()
        self.CalcGrid()

        self.bodyLength = 3
        self.body = self.GenerateBody()
        self.direction = Direction.Right

        self.score = 0
        self.moves = 0
        self.CurrentFoodLoc = None
        self.AddSegment = False

        self.UpdateGui()
        arcade.schedule( self.move, 1/15 )
        self.paused = False
        self.dead = False

        arcade.schedule( self.SpawnFood, random.random() * 2 )

    def CalcGrid(self):
        self.width = (self.width - 2*SNAKE_SEGMENT_RADIUS) / SNAKE_SEGMENT_RADIUS
        self.height = (self.height - 2*SNAKE_SEGMENT_RADIUS) / SNAKE_SEGMENT_RADIUS

    def GenerateBody(self):
        body = []
        while len(body) < self.bodyLength:
            coor = [int(self.width/2) - len(body), int(self.height/2)]
            body.append(coor)
        return body
        
    def UpdateGui(self):
        self.Gui.SetBody(self.body)
        self.Gui.SetScore(self.score)
        self.Gui.SetMoves(self.moves)
        self.Gui.SetFood(self.CurrentFoodLoc)

    def move(self, _):
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

            if self.AddSegment:
                new_body.append( self.body[-1] )
                self.AddSegment = False

            if new_body[0][0] < 0 or new_body [0][0] > self.width:
                new_body = self.body
                self.YouDied()

            if new_body[0][1] < 0 or new_body [0][1] > self.height:
                new_body = self.body
                self.YouDied()

            self.moves += 1

            self.body = new_body
            self.BodyCollisionDetecion()
            self.CheckFoodEaten()
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
            self.Gui.SetPaused()

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

    def BodyCollisionDetecion(self):
        head = self.body[0]
        if head in self.body[1:]:
            self.YouDied()

    def SpawnFood(self, _):
        x, y = self.GetRandomCoor()
        self.CurrentFoodLoc = [x, y]
        self.UpdateGui()
        arcade.unschedule(self.SpawnFood)

    def GetRandomCoor(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        if [x, y] in self.body and self.CalcDistanceBetweenPoints(self.body[0], [x,y]) < 10:
            x, y = self.GetRandomCoor()

        return x, y

    def CalcDistanceBetweenPoints(self, point1, point2):
        x_dist = abs( point1[0] - point2[0] )
        y_dist = abs( point1[1] - point2[1] )

        x_dist_pow = math.pow( x_dist, 2 )
        y_dist_pow = math.pow( y_dist, 2 )
        dist = math.sqrt( x_dist_pow + y_dist_pow )

        return int( dist )

    def CheckFoodEaten(self):
        head = self.body[0]

        if self.CurrentFoodLoc == head:
            self.score += 1
            self.CurrentFoodLoc = None
            self.UpdateGui()
            arcade.schedule( self.SpawnFood, random.random() * 2 )
            self.AddSegment = True