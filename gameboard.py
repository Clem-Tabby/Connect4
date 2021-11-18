
import pygame
from settings import grid, width, screen_height, num_rows, num_cols
from gamepiece import GamePiece
from math import floor
from tile import Tile


class GameBoard:

    def __init__(self, surface):
        self.surface = surface

        # Game keeping
        self.player_one = True
        self.game_over = False
        self.stack_heights = [0 for col in range(num_cols)]

        # Pieces
        self.pieces = pygame.sprite.Group()

        # Board tiles
        self.tiles = pygame.sprite.Group()
        self.spawn_tiles()

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
        for sprite in self.pieces.sprites():
            if sprite.stop is False:
                for other_sprite in self.pieces.sprites():
                    if sprite.rect.colliderect(other_sprite.rect) and other_sprite.stop is True:
                        sprite.stop = True
                        sprite.rect.y -= sprite.y_shift // 2

            if sprite.rect.y >= screen_height - width:
                sprite.stop = True

    def update_grid(self):
        pass

    def check4(self):
        pass

    def all_stopped(self):
        sprites = self.pieces.sprites()
        if len(sprites) > 0:
            stop_list = []
            for sprite in sprites:
                stop_list.append(sprite.stop)
            return all(stop_list)
        else:
            return True

    def get_click(self):
        click = pygame.mouse.get_pressed()[0]
        all_stopped = self.all_stopped()
        pos = pygame.mouse.get_pos()
        col = floor(pos[0]/width)
        if click and not self.game_over and all_stopped and self.stack_heights[col] < num_rows:
            self.player_one = not self.player_one
            if self.player_one:
                color = 'red'
            else:
                color = 'blue'
            self.spawn_gamepiece(pos, color)
            self.stack_heights[col] += 1


    def reset(self):
        pass

    def run(self):
        self.get_click()
        self.pieces.update()
        self.piece_collisions()
        self.pieces.draw(self.surface)
        self.tiles.draw(self.surface)
