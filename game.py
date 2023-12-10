import pygame
from Enviroment import labyrinth
from Entities import screenHeight,screenWidth
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_tf_policy
from tf_agents.trajectories import trajectory
import time
import sys
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
        return action
    
    def playing(self, num_episodes=5,model_path = '/models'):
        clock = pygame.time.Clock()
        for _ in range(num_episodes):
            print("Episode", _)
            time_step = self.tf_env.reset()
            episode_reward = 0.0

            while not time_step.is_last():
                self.screen.fill((253, 245, 230))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.time.delay(10)
                action_step = self.agent.policy.action(time_step)
                action = self.agent_policy(time_step)
                next_time_step = self.tf_env.step(action)

                reward = next_time_step.reward.numpy()[0]
                episode_reward += reward
                # print(f"Step Reward: {reward}")
                inputs = next_time_step.observation.numpy()[0]
                # print(f"Inputs: {inputs}")

                self.tf_env.render()
                pygame.display.update()

                time_step = next_time_step
                clock.tick(30)

            print(f"Total Episode Reward: {episode_reward}")
            
            print(self.agent_handler.agent.collect_data_spec)
            experience = trajectory.from_transition(
                time_step,
                action,
                next_time_step,
            )
            print(experience)
            
            
        self.agent_handler.save_policy(model_path)

if __name__ == "__main__":
    game = MinotaurGame(screenHeight,screenWidth)
    game.playing(num_episodes=10,model_path='/models')
    