import pygame
from Enviroment import labyrinth
from Entities import screenHeight,screenWidth

pygame.init()
class MinotaurGame:
    def __init__(self, h: int, w: int) -> None: 
        self.screen = pygame.display.set_mode((w,h),vsync=1)
        pygame.display.set_caption('MinotaurAI')
        pygame.display.set_icon(pygame.image.load('img/minotaurLogo.png'))
        
    def playing(self) -> None:
        environment = labyrinth(self.screen)
        while True:
            self.screen.fill((253,245,230))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            environment.run()
            pygame.display.update()

if __name__ == "__main__":
    game = MinotaurGame(screenHeight,screenWidth)
    game.playing()