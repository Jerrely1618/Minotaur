import pygame
from Enviroment import wall,wallSize,Layout,detectionLine,endPoint
from math import dist
import numpy as np

input_layer = np.zeros(11)
class labyrinth:
    def __init__(self,surface):
        self.display_surface = surface
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.GroupSingle()
        self.friends = pygame.sprite.GroupSingle()
        self.finishs = pygame.sprite.GroupSingle()
        
        for i,row in enumerate(Layout):
            for j,tile in enumerate(row):
                x = j * wallSize
                y = i * wallSize
                if tile == 'X':
                    side = wall((x,y),wallSize)
                    self.walls.add(side)
                if tile == 'M':
                    enemy = Minotaur((x,y+5))
                    self.enemies.add(enemy)
                if tile == 'H':
                    for hero in range(1):
                        friend = Hero((x,(y+5)))
                        self.friends.add(friend)
                if tile == 'E':
                    finish = endPoint((x,y),wallSize)
                    self.finishs.add(finish)
                    
    def minotaur_collisions(self):
        minotaur = self.enemies.sprite
        finish = self.finishs.sprite
        minotaur.rect.x += minotaur.direction.x
        
        for block in self.walls.sprites():
            if block.rect.colliderect(minotaur.rect):
                if minotaur.direction.x > 0:
                    minotaur.rect.right = block.rect.left
                elif minotaur.direction.x < 0:
                    minotaur.rect.left = block.rect.right
                elif minotaur.direction.y > 0:
                    minotaur.rect.bottom = block.rect.top
                elif minotaur.direction.y < 0:
                    minotaur.rect.top = block.rect.bottom
        
    def hero_collisions(self):
        finish = self.finishs.sprite
        for hero in self.friends.sprites():
            hero.rect.x += hero.direction.x
            for block in self.walls.sprites():
                if block.rect.colliderect(hero.rect):
                    hero.Collided = True
                    if hero.direction.x > 0:
                        hero.rect.right = block.rect.left
                    elif hero.direction.x < 0:
                        hero.rect.left = block.rect.right
                    elif hero.direction.y > 0:
                        hero.rect.bottom = block.rect.top
                    elif hero.direction.y < 0:
                        hero.rect.top = block.rect.bottom
                for i,line in enumerate(hero.lines):
                    if block.rect.clipline(line.pos,line.end):
                        pygame.draw.circle(self.display_surface,'red',line.end,10)
                    
    def run(self):
        self.walls.draw(self.display_surface)
        
        self.enemies.update()
        self.friends.update(self.finishs.sprite)
        self.minotaur_collisions()
        self.hero_collisions()
        self.enemies.draw(self.display_surface)
        self.friends.draw(self.display_surface)
        
class Minotaur(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.image = pygame.image.load('img/Mino.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        
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
        
class Hero(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.image = pygame.image.load('img/Hero.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.reward = 0
        self.Collided = False
        
        self.lines = []
        for i in range(11):
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

    def update(self,finish):
        self.movement()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        pos = (self.rect.x,self.rect.y)
        for i,line in enumerate(self.lines):
            linePos = (pos[0]-line.centerAdjust,pos[1]-line.centerAdjust)
            line.calculate_end(i,len(self.lines)-1)
            line.update(linePos,line.end,line.length)
        # if self.Collided == False:
        self.reward = dist([pos[0],pos[1]],[finish.rect.x,finish.rect.y])
        # else:
        #     self.reward = 0
