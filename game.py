import pygame
from Enviroment import labyrinth
from Entities import screenHeight,screenWidth
from tf_agents.environments import tf_py_environment
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
        action = action_step.action.numpy()[0]
        return action
    
    def playing(self, num_episodes=5,model_path = '/models'):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 25)
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
                action = self.agent_policy(time_step)
                next_time_step = self.tf_env.step(action)
                
                reward = next_time_step.reward.numpy()[0]
                episode_reward += reward
                
                reward_text = font.render(f'Total Reward: {episode_reward:.2f}', True, (0, 0, 0))
                inputs_text = font.render(f'Inputs: {next_time_step.observation.numpy()[0]}', True, (0, 0, 0))
                action_text = font.render(f'Action: {action}', True, (0, 0, 0))
                self.tf_env.render()
                self.screen.blit(reward_text, (10, 10))
                self.screen.blit(inputs_text, (10, 30))
                self.screen.blit(action_text, (10, 50))
                pygame.display.update()
                time_step = next_time_step
                clock.tick(30)
                
            experience = self.agent.collect_data_spec
            # if (_ + 1) % 5 == 0:
            print(experience)
            #     self.agent.train(experience=experience) 
            print(f"Total Episode Reward: {episode_reward}")
        self.agent_handler.save_policy(model_path)

if __name__ == "__main__":
    game = MinotaurGame(screenHeight,screenWidth)
    game.playing(num_episodes=10000,model_path='./models')