import pygame as pg
import pygame.draw
import sys
import math

from map import Map, TILE_COLOR_DICT, TILE_SIDE_COLOR_DICT
from player import Player

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WW_HALF = WINDOW_WIDTH / 2
WH_HALF = WINDOW_HEIGHT / 2

SPEED = 0.3

TILE_SIZE = 32
TILE_SIZE_HALF = int(TILE_SIZE / 2)
FOV = math.pi / 3  # 60 deg


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('DDA')
        self.screen = pg.display.set_mode((WINDOW_WIDTH * 2, WINDOW_HEIGHT))
        self.surface_fp = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface_map = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pg.time.Clock()

        self.player = Player((5 * TILE_SIZE, 5 * TILE_SIZE))
        self.map = Map(TILE_SIZE)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rotate(-0.01)
            if keys[pygame.K_s]:
                self.player.move('back')
            if keys[pygame.K_d]:
                self.player.rotate(0.01)
            if keys[pygame.K_w]:
                self.player.move('forward')

            self.screen.fill('yellow')
            self.surface_map.fill('black')
            self.surface_fp.fill('black')

            self.render()

            self.screen.blit(self.surface_fp, (0, 0))
            self.screen.blit(self.surface_map, (WINDOW_WIDTH + 2, 0))

            pg.display.flip()
            self.clock.tick()

    def render(self):
        # Render map
        for j in range(self.map.height):
            for i in range(self.map.width):
                idx = j*self.map.width + i
                surface = pg.surface.Surface((TILE_SIZE, TILE_SIZE))
                tile = self.map.tiles[idx]
                surface.fill(TILE_COLOR_DICT.get(tile))
                self.surface_map.blit(surface, (i * TILE_SIZE, j * TILE_SIZE))

        # Render player indicator surface on map
        surface = pg.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surface, 'orange', (TILE_SIZE_HALF, TILE_SIZE_HALF), TILE_SIZE_HALF)
        self.surface_map.blit(surface, (self.player.x - TILE_SIZE_HALF, self.player.y - TILE_SIZE_HALF))

        # Generate rays
        rays = []
        angle = self.player.angle - FOV / 2
        step = FOV / WINDOW_WIDTH
        for i in range(WINDOW_WIDTH):
            rays.append(self.build_ray(angle, i))
            angle += step

        # Cast rays
        for ray in rays:
            self.ray_cast(ray)

    def build_ray(self, angle, i):
        x = math.cos(angle)
        y = math.sin(angle)
        s = max(abs(x), abs(y))
        x /= s
        y /= s
        return x, y, i

    def ray_cast(self, ray):
        ray_dir_x, ray_dir_y, i = ray

        map_x = int(self.player.x / TILE_SIZE)
        map_y = int(self.player.y / TILE_SIZE)

        ray_start_x = self.player.x / TILE_SIZE
        ray_start_y = self.player.y / TILE_SIZE

        if ray_dir_x == 0:
            delta_dist_x = 1e30
        else:
            delta_dist_x = abs(1/ray_dir_x)
        if ray_dir_y == 0:
            delta_dist_y = 1e30
        else:
            delta_dist_y = abs(1/ray_dir_y)

        hit = 0
        side = -1

        if ray_dir_x < 0:
            step_x = -1
            side_dist_x = (ray_start_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - ray_start_x) * delta_dist_x
        if ray_dir_y < 0:
            step_y = -1
            side_dist_y = (ray_start_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - ray_start_y) * delta_dist_y

        while hit == 0:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            pg.draw.rect(self.surface_map, 'purple', pygame.Rect(map_x * TILE_SIZE, map_y * TILE_SIZE, 4, 4))

            hit = self.map.tiles[map_y * self.map.width + map_x]
            if hit:

                pg.draw.line(
                    self.surface_map,
                    'green',
                    (self.player.x, self.player.y),
                    (map_x * TILE_SIZE, map_y * TILE_SIZE)
                )

        if side == 0:
            wall_dist = side_dist_x - delta_dist_x
        else:
            wall_dist = side_dist_y - delta_dist_y

        line_height = int(WINDOW_HEIGHT / wall_dist)

        draw_start = -line_height / 2 + WH_HALF
        if draw_start < 0:
            draw_start = 0
        draw_end = line_height / 2 + WH_HALF
        if draw_end >= WINDOW_HEIGHT:
            draw_end = WINDOW_HEIGHT - 1

        if hit:
            color = TILE_COLOR_DICT.get(hit)
            if side:
                color = TILE_SIDE_COLOR_DICT.get(hit)
            pg.draw.line(self.surface_fp, color=color, start_pos=(i, draw_start), end_pos=(i, draw_end))


if __name__ == '__main__':
    app = App()
    app.run()
