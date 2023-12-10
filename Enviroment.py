import pygame
from Entities import Minotaur,Hero,wallSize,Layout
import numpy as np
from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec
from Entities import TOTAL_INPUTS 
from tf_agents.environments import py_environment

class labyrinth(py_environment.PyEnvironment):
    def __init__(self,surface):
        self.display_surface = surface
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.GroupSingle()
        self.friends = pygame.sprite.GroupSingle()
        self.finishs = pygame.sprite.GroupSingle()
        self.current_time_step = None
        self._episode_ended = False
        
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
    def observation_spec(self):
        return array_spec.BoundedArraySpec(shape=(TOTAL_INPUTS,), dtype=np.float32, minimum=0, name='observation')

    def action_spec(self):
        return array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')

    def _reset(self):
        self.current_time_step = None
        self.friends.sprite.reset()
        self.start_time = pygame.time.get_ticks()
        self._episode_ended = False
        return ts.restart(np.array(self._get_observation(), dtype=np.float32))

    def _step(self, action):
        if self._episode_ended:
            return self._reset()

        self.friends.sprite.movement(action)
        self.friends.sprite.update()

        collision_reward = 0.0
        for block in self.walls.sprites():
            if block.rect.colliderect(self.friends.sprite.rect):
                collision_reward = -0.1
                break

        if self.friends.sprite.rect.colliderect(self.finishs.sprite.rect):
            reward = 1.0
            self._episode_ended = True
            return ts.termination(np.array(self._get_observation(), dtype=np.float32), reward)

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        print(f"Elapsed Time: {elapsed_time}")

        if elapsed_time >= 100:
            self._episode_ended = True
            reward = -0.5
            return ts.termination(np.array(self._get_observation(), dtype=np.float32), reward)

        reward = collision_reward
        return ts.transition(np.array(self._get_observation(), dtype=np.float32), reward, discount=1.0)


    def _get_observation(self):
        self.render()
        hero_inputs = self.friends.sprite.get_inputs(self.display_surface, self.finishs.sprite)
        # minotaur_inputs = self.enemies.sprite.get_inputs(self.display_surface)
        return np.array(hero_inputs)
    
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
                    
        # for line in minotaur.lines:
        #     pygame.draw.line(self.display_surface,'black',line.pos,line.end,1)
        
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
            # for line in hero.lines:
            #     pygame.draw.line(self.display_surface,'black',line.pos,line.end,1)
    def render(self, mode='rgb_array'):
        if mode != 'rgb_array':
            raise NotImplementedError('Only "rgb_array" mode is supported.')
        self.display_surface.fill((253, 245, 230))
        self.run()
        pygame.display.flip()
        return pygame.surfarray.array3d(self.display_surface)
    
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
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft = pos)
        
class wall(pygame.sprite.Sprite):
    def __init__(self,pos,size) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

