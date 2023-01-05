import pygame
from Enviroment import screenHeight,screenWidth
from Entities import labyrinth

pygame.init()
class MinotaurGame:
    def __init__(self, h: int, w: int) -> None: 
        self.screen = pygame.display.set_mode((w,h),vsync=1)
        pygame.display.set_caption('MinotaurAI')
        pygame.display.set_icon(pygame.image.load('img/minotaurLogo.png'))
        self.playing()
        
    def playing(self) -> None:
        environment = labyrinth(self.screen)
        while True:
            self.screen.fill((253,245,230))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            environment.run()
            pygame.display.update()

game = MinotaurGame(screenHeight,screenWidth)