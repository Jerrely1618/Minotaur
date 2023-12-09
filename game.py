import pygame
from Enviroment import labyrinth
from Entities import screenHeight,screenWidth
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_tf_policy
import time
from AI import HeroAgent


pygame.init()
class MinotaurGame:
    def __init__(self, h: int, w: int) -> None: 
        self.screen = pygame.display.set_mode((w,h),vsync=1)
        pygame.display.set_caption('MinotaurAI')
        pygame.display.set_icon(pygame.image.load('img/minotaurLogo.png'))
        
        self.tf_env = tf_py_environment.TFPyEnvironment(labyrinth(self.screen))
        self.agent_handler = HeroAgent(self.tf_env)
        self.agent = self.agent_handler.get_agent()
        
    def agent_policy(self, time_step):
        action_step = self.agent.policy.action(time_step)
        action =  action_step.action.numpy()[0]
        print(f"Agent chose action: {action}")
        return action
    
    def playing(self) -> None:
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((253,245,230))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.time.delay(10)
            if self.tf_env.current_time_step().is_last():
                self.tf_env.reset()
            time_step = self.tf_env.current_time_step()
            action = self.agent_policy(time_step)
            next_time_step = self.tf_env.step(action)
            self.tf_env.render()
            pygame.display.update()
            clock.tick(60)
if __name__ == "__main__":
    game = MinotaurGame(screenHeight,screenWidth)
    game.playing()