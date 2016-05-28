import pygame
from pygame.locals import*
img = pygame.image.load('./images/1.jpg')

img = pygame.transform.scale(img, (100, 100))

white = (255, 64, 64)
w = 640
h = 480
screen = pygame.display.set_mode((w, h))
screen.fill((white))
running = 1

while running:
    screen.fill((white))
    screen.blit(img,(10,0))
    pygame.display.flip()