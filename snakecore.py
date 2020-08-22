"""
Snake game Core code

Developer: Bram Verstraeten
"""

# --- Imports ----------------------------------------------------------------------------------------------------------
import arcade
import enum
import random
import math

# --- Constants --------------------------------------------------------------------------------------------------------
SNAKE_LENGTH = 3
SNAKE_SPEED = 1/10

# --- Class ------------------------------------------------------------------------------------------------------------
class Direction(enum.Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

# --- Class ------------------------------------------------------------------------------------------------------------
class SnakeCore():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        self.__score = 0
        self.__numMoves = 0

        self.__body = self.GenerateBody()
        self.__food = None
        self.__direction = Direction.Right

        self.__paused = False
        self.__dead = False

        arcade.schedule(self.update, SNAKE_SPEED)
        arcade.schedule(self.SpawnFood, random.random()*2)

    # Getters
    def GetScore(self):
        return self.__score
    
    def GetNumMoves(self):
        return self.__numMoves

    def GetBody(self):
        return self.__body

    def GetFood(self):
        return self.__food

    def GetDead(self):
        return self.__dead

    def GetPaused(self):
        return self.__paused

    def GenerateBody(self):
        body = []
        while len(body) < SNAKE_LENGTH:
            x = int( self.__width / 2  - len(body) )
            y = int( self.__height / 2 )
            coor = [x, y]
            body.append(coor)
        return body

    def KeyPressed(self, key):
        if key == arcade.key.UP and not self.__direction == Direction.Down:
            self.__direction = Direction.Up
        elif key == arcade.key.DOWN and not self.__direction == Direction.Up:
            self.__direction = Direction.Down
        elif key == arcade.key.RIGHT and not self.__direction == Direction.Left:
            self.__direction = Direction.Right
        elif key == arcade.key.LEFT and not self.__direction == Direction.Right:
            self.__direction = Direction.Left

        if key == arcade.key.P:
            self.__paused = False if self.__paused else True
            
        if key == arcade.key.ENTER:
            self.Reset()

    def Reset(self):
        self.__score = 0
        self.__numMoves = 0
        self.__direction = Direction.Right
        self.__dead = False
        self.__body = self.GenerateBody()
        self.__food = None

    def MoveSnake(self):
        new_body = []
        x = 0
        y = 0
        if self.__direction == Direction.Right or self.__direction == Direction.Left:
            if self.__direction == Direction.Right:
                x = 1
            else:
                x = -1
        elif self.__direction == Direction.Up or self.__direction == Direction.Down:
            if self.__direction == Direction.Up:
                y = 1
            else:
                y = -1
        head = self.__body[0]
        new_head = [head[0] + x, head[1] + y]
        new_body.append(new_head)

        for i, _ in enumerate( self.__body ):
            if not i == 0:
                new_body.append( self.__body[i-1] )

        self.__numMoves += 1

        edgeCollision = False
        if new_head[0] < 0 or new_head[0] > self.__width:
            edgeCollision = True
        if new_head[1] < 0 or new_head[1] > self.__height:
            edgeCollision = True

        return new_body, edgeCollision

    def BodyCollisionDetection(self, body):
        head = body[0]
        dead = False
        if head in body[1:]:
            dead = True
        return dead

    def SpawnFood(self, _):
        x, y = self.GetRandomCoor()
        self.__food = [x, y]
        arcade.unschedule(self.SpawnFood)

    def GetRandomCoor(self):
        x = random.randint(0, self.__width)
        y = random.randint(0, self.__height)

        if [x, y] in self.__body and self.CalcDistanceBetweenPoints(self.__body[0], [x,y]) > 5:
            x, y = self.GetRandomCoor()

        return x, y

    def CalcDistanceBetweenPoints(self, point1, point2):
        x_dist = abs( point1[0] - point2[0] )
        y_dist = abs( point2[1] - point2[1] )
        x_dist_pow = math.pow( x_dist, 2 )
        y_dist_pow = math.pow( y_dist, 2 )
        dist = math.sqrt( x_dist_pow + y_dist_pow )
        return int(dist)

    def CheckFoodEaten(self, body):
        head = body[0]
        eaten = False
        if self.__food == head:
            self.__score += 1
            self.__food = None
            eaten = True
            arcade.schedule(self.SpawnFood, random.random()*2)
        return eaten

    def update(self, _):
        if not self.__paused and not self.__dead:
            new_body, self.__dead = self.MoveSnake()

            if not self.__dead:
                self.__dead = self.BodyCollisionDetection(new_body)

            if not self.__dead:
                new_segment = self.CheckFoodEaten(new_body)
                if new_segment:
                    new_body.append( self.__body[-1] )

            if not self.__dead:
                self.__body = new_body