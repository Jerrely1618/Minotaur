import pygame
from Entities import Minotaur,Hero,wallSize,Layout
import numpy as np

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
                    
        for line in minotaur.lines:
            pygame.draw.line(self.display_surface,'black',line.pos,line.end,1)
        
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
            for line in hero.lines:
                pygame.draw.line(self.display_surface,'black',line.pos,line.end,1)
                    
    def run(self):
        self.walls.draw(self.display_surface)
        self.enemies.update()
        self.friends.update()
        
        self.enemies.sprite.get_inputs(self.display_surface)
        self.friends.sprite.get_inputs(self.display_surface,self.finishs.sprite)
        
        self.minotaur_collisions()
        self.hero_collisions()

        self.enemies.draw(self.display_surface)
        self.friends.draw(self.display_surface)

class endPoint(pygame.sprite.Sprite):
    def __init__(self,pos,size) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft = pos)
        
class wall(pygame.sprite.Sprite):
    def __init__(self,pos,size) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

