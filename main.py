# Connect 4!
#
# Code by Clem-Tabby
# Background music by Visager: https://freemusicarchive.org/music/Visager/Songs_from_an_Unmade_Forest_World/Roots_Loop
# Background victory noise by


# Pygame platformer
import pygame
import sys
from settings import screen_height, screen_width, background_color
from gameboard import GameBoard

pygame.init()
pygame.mixer.init()
background_music = pygame.mixer.Sound('./Visager - Roots [Loop].mp3')
background_music.play(-1)
screen = pygame.display.set_mode((screen_width, screen_height))
gameboard = GameBoard(screen)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)
    gameboard.run()
    pygame.display.update()
    clock.tick(60)
