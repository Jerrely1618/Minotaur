import pygame
from math import sin,cos,pi

class endPoint(pygame.sprite.Sprite):
    def __init__(self,pos,size) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = pos)
        
class wall(pygame.sprite.Sprite):
    def __init__(self,pos,size) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

class detectionLine():
    def __init__(self,center) -> None:
        self.pos = (0,0)
        self.length = 50
        self.end = (0,0)
        self.centerAdjust = center
        
    def update(self,pos,end,length):
        self.pos = pos
        self.length = length
        self.end = (end[0],end[1])
        
    def calculate_end(self,n,nSize): 
        x = (self.length*cos((pi/5)*n))-self.pos[0]
        y = (self.length*sin((pi/5)*n))-self.pos[1]
        self.end = (-x,-y)

Layout = [
"XXXXXXXXXXXXXXXXXXXXX",
"                    X",
" H                  X",
"                    X",
"XXXXX   X   X   X   X",
"X       X   X   X   X",
"X       X   X   X   X",
"X   XXXXX   XXXXXXXXX",
"X   X           X   X",
"X   X           X   X",
"X   X           X   X",
"X   X   X   X   X   X",
"X   X   X   X       X",
"X   X   X   X       X",
"X   X   X   X       X",
"X   XXXXX   X   X   X",
"X   X       X   X    ",
"X   X       X   X    ",
"X   XM      X   X   E",
"XXXXXXXXXXXXXXXXXXXXX"
]
wallSize = 30
screenHeight = len(Layout) * wallSize
screenWidth = len(Layout[0]) * wallSize