
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = pygame.image.load('./graphics/connect4_game_board_section.png').convert_alpha()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
