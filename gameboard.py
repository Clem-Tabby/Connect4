
import pygame
from settings import grid, width, screen_height
from gamepiece import GamePiece
from math import floor
from tile import Tile


class GameBoard:

    def __init__(self, surface):
        self.surface = surface

        # Game keeping
        self.player_one = False
        self.game_over = False

        # Pieces
        self.pieces = pygame.sprite.Group()

        # Board tiles
        self.tiles = pygame.sprite.Group()
        self.spawn_tiles()

    # def draw_grid(self):
    #     for row in range(num_rows + 1):
    #         pygame.draw.line(self.surface, (251, 242, 54), (0, row * width + width * 2),
    #                          (num_cols * width, row * width + width * 2), 3)
    #     for col in range(num_cols + 1):
    #         pygame.draw.line(self.surface, (251, 242, 54), (col * width, width * 2),
    #                          (col * width, num_rows * width + width * 2), 3)

    def spawn_tiles(self):
        for row_index, row in enumerate(grid):
            for col_index, col in enumerate(row):
                x = col_index * width
                y = row_index * width + (2 * width)
                tile = Tile((x, y))
                self.tiles.add(tile)

    def spawn_gamepiece(self, pos, color):
        x = width * floor(pos[0] // width)
        self.pieces.add(GamePiece(color, (x, width)))

    def piece_collisions(self):
        for i, sprite in enumerate(self.pieces.sprites()):
            for j, other_sprite in enumerate(self.pieces.sprites()):
                collided = sprite.rect.colliderect(other_sprite)
                if collided and i != j:
                    return collided
                else:
                    continue
            if sprite.rect.y >= screen_height - width or collided:
                sprite.stop = True

    def update_grid(self):
        pass

    def get_click(self):
        click = pygame.mouse.get_pressed()[0]
        if click and not self.game_over:
            self.player_one = not self.player_one
            pos = pygame.mouse.get_pos()
            if self.player_one:
                color = 'red'
            else:
                color = 'blue'
            self.spawn_gamepiece(pos, color)

    def reset(self):
        pass

    def run(self):
        # self.draw_grid()
        self.get_click()
        self.pieces.update()
        self.piece_collisions()
        self.pieces.draw(self.surface)
        self.tiles.draw(self.surface)
