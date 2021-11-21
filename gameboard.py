import pygame
from settings import grid, width, screen_width, screen_height, num_rows, num_cols
from gamepiece import GamePiece
from math import floor
from tile import Tile
from upper_border import UpperBorder


class GameBoard:

    def __init__(self, surface):
        self.surface = surface
        self.end_noise = pygame.mixer.Sound('sfx/Yeah! Teehee!.wav')

        # Game keeping
        self.player_one = True
        self.game_over = False
        self.stack_heights = [0 for col in range(num_cols)]
        self.connect = 1  # Length of connected pieces
        self.winner = ''
        self.end_noise_played = False

        # Pieces
        self.pieces = pygame.sprite.Group()
        self.positions = []
        self.colors = []

        # Board tiles
        self.tiles = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()
        self.spawn_tiles()
        self.spawn_border()

    def spawn_tiles(self):
        for row_index, row in enumerate(grid):
            for col_index, col in enumerate(row):
                x = col_index * width
                y = row_index * width + (2 * width)
                tile = Tile((x, y))
                self.tiles.add(tile)

    def spawn_border(self):
        for col in range(num_cols):
            x = col * width
            y = 2 * width
            border = UpperBorder((x, y))
            self.borders.add(border)

    def spawn_gamepiece(self, pos, color):
        x = width * floor(pos[0] // width)
        self.pieces.add(GamePiece(color, (x, width)))

    def get_positions_colors(self):
        self.positions = []
        self.colors = []

        for sprite in self.pieces.sprites():
            self.positions.append(sprite.rect.topleft)
            self.colors.append(sprite.color)
        return self.positions, self.colors

    def check4(self):
        offsets = [(-width, 0), (-width, width), (0, width), (width, width),
                   (width, 0), (width, -width), (0, -width), (-width, -width)]
        positions, colors = self.get_positions_colors()

        for sprite in self.pieces.sprites():
            sprite_pos = sprite.rect.topleft

            for offset in offsets:
                connect = 1
                while connect < 4:
                    target_pos = tuple(map(lambda a, b: a + b, sprite_pos, offset))
                    try:
                        i = positions.index(target_pos)
                    except ValueError:
                        break  # No piece at target_pos
                    if sprite.color == colors[i] and self.all_stopped():
                        connect += 1
                        sprite_pos = target_pos
                    else:
                        break  # Colors didn't match

                if connect == 4:
                    self.game_over = True
                    self.winner = sprite.color
                    break

    def piece_collisions(self):
        if not self.all_stopped():
            for sprite in self.pieces.sprites():
                if sprite.stop is False:
                    for other_sprite in self.pieces.sprites():
                        if sprite.rect.colliderect(other_sprite.rect) and other_sprite.stop is True:
                            sprite.stop = True
                            sprite.rect.y -= sprite.y_shift // 2

                    if sprite.rect.y >= screen_height - width:
                        sprite.stop = True

    def all_stopped(self):
        sprites = self.pieces.sprites()

        if len(sprites) > 0:
            stop_list = []
            for sprite in sprites:
                stop_list.append(sprite.stop)
            all_stopped = all(stop_list)
            return all_stopped
        else:
            return True

    def get_click(self):
        click = pygame.mouse.get_pressed()[0]
        all_stopped = self.all_stopped()
        pos = pygame.mouse.get_pos()
        col = floor(pos[0] / width)

        if click and not self.game_over and all_stopped and self.stack_heights[col] < num_rows:
            if self.player_one:
                color = 'red'
            else:
                color = 'blue'
            self.spawn_gamepiece(pos, color)
            self.stack_heights[col] += 1
            self.player_one = not self.player_one

    def reset(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.pieces.empty()
            self.stack_heights = [0 for col in range(num_cols)]
            self.end_noise_played = False
            self.game_over = False

    def run(self):
        self.get_click()
        self.pieces.update()
        self.piece_collisions()
        self.check4()
        self.pieces.draw(self.surface)
        self.tiles.draw(self.surface)
        self.borders.draw(self.surface)

        # Handle game over state
        if self.game_over:
            end_string = self.winner.upper() + " WINS!"
            if self.winner == 'red':
                text_color = (255, 0, 0)
            else:
                text_color = (0, 0, 255)
            end_font = pygame.font.Font('freesansbold.ttf', 25)
            end_text = end_font.render(end_string, True, text_color)
            text_width, text_height = end_font.size(end_string)
            self.surface.blit(end_text, ((screen_width - text_width) / 2, width / 2))
            if not self.end_noise_played:
                self.end_noise.play(0)
                self.end_noise_played = True
                print(self.end_noise_played)

        self.reset()
