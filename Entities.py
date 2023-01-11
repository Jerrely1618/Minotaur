import pygame
from math import dist,sin,cos,pi
import numpy as np
        
DETECTION_POINTS = 4
# Detection points (4): Left,Right,Up and Down distance to closest wall
# Self coordinates (2): X and Y
# Opossite coordinates(2): X and Y
TOTAL_INPUTS = DETECTION_POINTS + 4

class Minotaur(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:

        #Loading the sprite
        super().__init__()
        self.image = pygame.image.load('img/Mino.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        
        #Input parameters
        self.pos = pos
        self.lines = []
        for i in range(DETECTION_POINTS):
            line = detectionLine(center=-10)
            self.lines.append(line)
        
    def movement(self): #for user mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction.y = 0
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction.y = 0
        elif keys[pygame.K_UP]:
            self.direction.y = -1
            self.direction.x = 0
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.direction.x = 0
        else: 
            self.direction.x = 0
            self.direction.y = 0

    def update(self):
        self.movement()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

    def get_inputs(self,surface):
        inputs = np.zeros(TOTAL_INPUTS)

        #Position input
        self.pos = (self.rect.x,self.rect.y)
        inputs[0] = self.pos[0]
        inputs[1] = self.pos[1]

        #Surrounding inputs
        n = 2
        for i,line in enumerate(self.lines):
                linePos = (self.pos[0]-line.centerAdjust,self.pos[1]-line.centerAdjust)
                for depth in range(max(screenHeight,screenWidth)):
                    x = -((depth*cos((pi/2)*i))-linePos[0])
                    y = -((depth*sin((pi/2)*i))-linePos[1])
                    pxArray = pygame.PixelArray(surface)
                    if pxArray[int(x),int(y)] == 12500670:
                        line.update(linePos,(x,y),depth)
                        inputs[n] = depth
                        n += 1
                        break
        
class Hero(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        
        #Loading the sprite
        super().__init__()
        self.image = pygame.image.load('img/Hero.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.Collided = False

        #Input parameters
        self.reward = 0
        self.pos = pos
        self.lines = []
        for i in range(DETECTION_POINTS):
            line = detectionLine(center=-10)
            self.lines.append(line)
        
    def movement(self): #for user mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.direction.y = 0
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.direction.y = 0
        elif keys[pygame.K_w]:
            self.direction.y = -1
            self.direction.x = 0
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.direction.x = 0
        else: 
            self.direction.x = 0
            self.direction.y = 0

    def update(self) -> np.array:
        self.movement()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

    def get_inputs(self,surface,finish_line):
        inputs = np.zeros(TOTAL_INPUTS + 1) #Additional reward input (Distance to the finish line)

        #Position input
        self.pos = (self.rect.x,self.rect.y)
        inputs[0] = self.pos[0]
        inputs[1] = self.pos[1]

        #Surrounding inputs
        n = 2
        for i,line in enumerate(self.lines):

                linePos = (self.pos[0]-line.centerAdjust,self.pos[1]-line.centerAdjust)
                for depth in range(max(screenHeight,screenWidth)):
                    x = -((depth*cos((2*pi/DETECTION_POINTS)*i))-linePos[0])
                    y = -((depth*sin((2*pi/DETECTION_POINTS)*i))-linePos[1])
                    pxArray = pygame.PixelArray(surface)
                    if pxArray[int(x),int(y)] == 12500670:
                        line.update(linePos,(x,y),depth)
                        inputs[n] = depth
                        n += 1
                        break
        
        #Reward input
        if self.Collided == False:
            self.reward = dist([self.pos[0],self.pos[1]],[finish_line.rect.x,finish_line.rect.y])
        else:
            self.reward = 0
        inputs[n] = int(self.reward)

        print(inputs)

class detectionLine():
    def __init__(self,center) -> None:
        self.pos = (0,0)
        self.length = 0
        self.end = (0,0)
        self.centerAdjust = center
        
    def update(self,pos,end,length):
        self.pos = pos
        self.length = length
        self.end = end

Layout = [
"XXXXXXXXXXXXXXXXXXXX",
"X                  X",
"X H                X",
"X                  X",
"XXXXX   X   X   X  X",
"X       X   X   X  X",
"X       X   X   X  X",
"X   XXXXX   XXXXXXXX",
"X   X          X   X",
"X   X          X   X",
"X   X          X   X",
"X   X   X  X   X   X",
"X   X   X  X       X",
"X   X   X  X       X",
"X   X   X  X       X",
"X   XXXXX  X   X   X",
"X   X      X   X   X",
"X   X      X   X   X",
"X   XM     X   X  EX",
"XXXXXXXXXXXXXXXXXXXX"
]
wallSize = 30
screenHeight = len(Layout) * wallSize
screenWidth = len(Layout[0]) * wallSize