
import pygame
from settings import y_shift
import resource_path as rp


class GamePiece(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()
        self.y_shift = y_shift
        self.stop = False
        self.color = color
        image = pygame.image.load(rp.resource_path('graphics/' + self.color + '_game_piece.png')).convert_alpha()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if not self.stop:
            self.rect.y += self.y_shift
        else:
            self.y_shift = 0
