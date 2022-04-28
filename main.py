# Connect 4!
#
# Code by Clem-Tabby
# Background music by Visager: https://freemusicarchive.org/music/Visager/Songs_from_an_Unmade_Forest_World/Roots_Loop
# Background victory noise by Shelby


import pygame
import sys
from settings import screen_height, screen_width, background_color
from gameboard import GameBoard
import resource_path as rp

pygame.init()
pygame.mixer.init()
background_music = pygame.mixer.Sound(rp.resource_path('sfx/Visager - Roots [Loop].mp3'))
background_music.set_volume(0.1)
background_music.play(-1)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Connect 4!')
icon = pygame.image.load(rp.resource_path('graphics/red_game_piece_icon.png'))
pygame.display.set_icon(icon)
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
