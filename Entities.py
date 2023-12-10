import pygame
from math import sqrt,sin,cos,pi
import numpy as np
        
DETECTION_POINTS = 4
# Detection points (4): Left,Right,Up and Down distance to closest wall
# Self coordinates (2): X and Y
# Opossite coordinates(2): X and Y
# Distance from the finish line in X vector and Y vector(2)
TOTAL_INPUTS = DETECTION_POINTS + 4

class Minotaur(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.image = pygame.image.load('img/Mino.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        
        self.pos = pos
        self.initial_pos = pos
        self.lines = []
        for i in range(DETECTION_POINTS):
            line = detectionLine(center=-10)
            self.lines.append(line)
        
    def movement(self):
        keys = pygame.key.get_pressed()
        move_right, move_left, move_up, move_down = 0, 0, 0, 0

        if keys[pygame.K_RIGHT]:
            move_right = 1
        if keys[pygame.K_LEFT]:
            move_left = 1
        if keys[pygame.K_UP]:
            move_up = 1
        if keys[pygame.K_DOWN]:
            move_down = 1
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            move_up = 1
            move_right = 1
        self.direction.x = int(move_right) - int(move_left)
        self.direction.y = int(move_down) - int(move_up)

        if self.direction.x != 0 and self.direction.y != 0:
            self.direction /= sqrt(2)
        

    def update(self):
        self.movement()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y * 2

    def get_inputs(self,surface):
        inputs = np.zeros(TOTAL_INPUTS)

        self.pos = (self.rect.x,self.rect.y)
        inputs[0] = self.pos[0]
        inputs[1] = self.pos[1]

        n = 2
        TARGET_COLOR = 12500670
        for i, line in enumerate(self.lines):
            linePos = (self.pos[0] - line.centerAdjust, self.pos[1] - line.centerAdjust)
            cos_val = cos((pi / 2) * i)
            sin_val = sin((pi / 2) * i)

            for depth in range(max(screenHeight, screenWidth)):
                x = -((depth * cos_val) - linePos[0])
                y = -((depth * sin_val) - linePos[1])
                pxArray = pygame.PixelArray(surface)
                x_index, y_index = int(x), int(y)

                if 0 <= x_index < surface.get_width() and 0 <= y_index < surface.get_height():
                    if pxArray[x_index, y_index] == TARGET_COLOR:
                        line.update(linePos, (x, y), depth)
                        inputs[n] = depth
                        n += 1
                        break
        
        del pxArray
        return inputs
    
class Hero(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.image = pygame.image.load('img/Hero.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.Collided = False
        self.reward = 0
        self.pos = pos
        self.initial_pos = pos
        self.lines = []
        
        for i in range(DETECTION_POINTS):
            line = detectionLine(center=-10)
            self.lines.append(line)
    def reset(self):
        self.rect.topleft = self.initial_pos
        self.direction = pygame.math.Vector2(0, 0)
        self.Collided = False
        
    def movement(self, action):
        if action == 0:
            self.direction.x = 1
            self.direction.y = 0
        elif action == 1:
            self.direction.x = -1
            self.direction.y = 0
        elif action == 2:
            self.direction.y = -1
            self.direction.x = 0
        elif action == 3:
            self.direction.y = 1
            self.direction.x = 0
        else:
            self.direction.x = 0
            self.direction.y = 0

    def update(self) -> np.array:
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

    def get_inputs(self,surface,finish_line):
        inputs = np.zeros(TOTAL_INPUTS)
        self.pos = (self.rect.x,self.rect.y)
        inputs[0] = self.pos[0]
        inputs[1] = self.pos[1]
        n = 2
        TARGET_COLOR = 12500670
        finish_position = np.array([finish_line.rect.x, finish_line.rect.y])
        hero_position = np.array([self.pos[0], self.pos[1]])
        distance_vector = finish_position - hero_position
        inputs[n] = distance_vector[0]
        inputs[n + 1] = distance_vector[1]
        n += 2
        
        for i, line in enumerate(self.lines):
            linePos = (self.pos[0] - line.centerAdjust, self.pos[1] - line.centerAdjust)
            cos_val = cos((pi / 2) * i)
            sin_val = sin((pi / 2) * i)

            for depth in range(max(screenHeight, screenWidth)):
                x = -((depth * cos_val) - linePos[0])
                y = -((depth * sin_val) - linePos[1])
                
                pxArray = pygame.PixelArray(surface)

                x_index, y_index = int(x), int(y)

                if 0 <= x_index < surface.get_width() and 0 <= y_index < surface.get_height():
                    if pxArray[x_index, y_index] == TARGET_COLOR:
                        line.update(linePos, (x, y), depth)
                        inputs[n] = depth
                        n += 1
                        break
        del pxArray
        return inputs

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