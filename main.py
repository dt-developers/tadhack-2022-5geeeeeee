#
#

# ignore pygame advertisement, sorry just to self-aware lib
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame import image, display, draw
from pygame.math import Vector2, Vector3

import math
from random import Random


class Player:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.direction = Vector2(0, -1)
        self.speed = 3
        self.turn_speed = 10
        self.money = 100
        self.points = 0
        self.api = 0


TEXTURES = {}


def _get_cached_texture(filename):
    try:
        if os.path.exists(filename) and filename not in TEXTURES:
            TEXTURES[filename] = image.load(filename)

        return TEXTURES[filename]
    except TypeError:
        return None


def _get_cached_and_scaled_texture(name, size):
    scaled_name = name + str(size)
    texture = _get_cached_texture(name)

    if scaled_name not in TEXTURES:
        scaled = pygame.transform.scale(
            texture, size
        )
        TEXTURES[scaled_name] = scaled

    return TEXTURES[scaled_name]


class Wall:
    def __init__(self, start, end, fill):
        self.start = start
        self.end = end
        self.equation = Vector3(end.y - start.y, -(end.x - start.x), end.x * start.y - start.x * end.y)
        self.direction = (end - start)
        self.fill = fill
        self.texture = _get_cached_texture(fill)


class Projectile:
    def __init__(self, position, direction, api, speed=1):
        self.position = position
        self.direction = direction
        self.api = api
        self.speed = speed
        self.birth_time = pygame.time.get_ticks()


class Level:
    def __init__(self):
        self.textures = (
            "./assets/brick.png",
            "./assets/flowers.png",
            "./assets/tech.png",
            "./assets/portrait.png",
        )

        self.walls = (
            Wall(Vector2(-10, 10), Vector2(-10, -10), "assets/wall_bricks.png"),
            Wall(Vector2(-10, -10), Vector2(10, -10), "assets/wall_bricks.png"),
            Wall(Vector2(10, -10), Vector2(10, 10), "assets/wall_bricks.png"),
            Wall(Vector2(10, 10), Vector2(50, 10), (200, 200, 200)),
            Wall(Vector2(50, 10), Vector2(50, 100), (200, 200, 200)),
            Wall(Vector2(50, 100), Vector2(0, 100), (200, 200, 200)),
            Wall(Vector2(0, 100), Vector2(-50, 100), (200, 200, 200)),
            Wall(Vector2(-50, 100), Vector2(-50, 10), (200, 200, 200)),
            Wall(Vector2(-50, 10), Vector2(-10, 10), (200, 200, 200)),
        )
        self.enemies = ()
        self.projectiles = list()


class FiveGeeeeeeeee:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self._running = True
        self._icon = None
        self._font = None
        self._display_surf = None
        self._r = Random()
        self._level = Level()
        self._apis = None
        self._keys_down = set()
        self.player = Player()

    def initialize(self):
        pygame.init()
        display.set_caption("5geeeeeeeee")

        self._display_surf = display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._font = pygame.font.SysFont("", 48)

        self._icon = image.load("./assets/icon.png")
        display.set_icon(self._icon)

        self._apis = (
            image.load("./assets/api_default.png"),
            image.load("./assets/api_latency.png"),
            image.load("./assets/api_throughput.png"),
        )

        self._level.textures = (image.load(x) for x in self._level.textures)

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYUP:
            if event.key in self._keys_down:
                self._keys_down.remove(event.key)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False

            # DEBUG
            if event.key == pygame.K_TAB:
                self.player.api = (self.player.api + 1) % len(self._apis)

            self._keys_down.add(event.key)

    def update(self):
        if pygame.K_DOWN in self._keys_down:
            self.player.position -= self.player.direction * self.player.speed
        if pygame.K_UP in self._keys_down:
            self.player.position += self.player.direction * self.player.speed

        if pygame.K_LEFT in self._keys_down:
            self.player.direction.rotate_ip(-self.player.turn_speed)
        if pygame.K_RIGHT in self._keys_down:
            self.player.direction.rotate_ip(self.player.turn_speed)

        if pygame.K_SPACE in self._keys_down:
            self._level.projectiles.append(
                Projectile(
                    self.player.position.copy(),
                    self.player.direction.copy(),
                    self.player.api
                )
            )

        now = pygame.time.get_ticks()
        for projectile in self._level.projectiles:
            projectile.position += projectile.direction * projectile.speed
            if now > projectile.birth_time + 300:
                self._level.projectiles.remove(projectile)

    def _wall_intersection_at_column(self, column):
        fov = 60

        ray_direction = self.player.direction.rotate(-fov / 2)
        ray_direction.rotate_ip(fov * (column / self.width))

        ray_start = self.player.position
        ray_end = ray_start + ray_direction

        ray_equation = Vector3(
            ray_end.y - ray_start.y,
            -(ray_end.x - ray_start.x)
            , ray_end.x * ray_start.y - ray_start.x * ray_end.y
        )

        intersecting_walls = list()
        for wall in self._level.walls:
            intersection = ray_equation.cross(wall.equation)
            if intersection.z < 0 or math.isclose(intersection.z, 0):
                # no intersection
                continue
            else:
                # back to 2d
                intersection = (intersection.xy / intersection.z)

                # point hitting wall facing wall?
                # px = p0 + x*v
                # px - p0 = x*v
                # (px - p0) / v = x
                if not math.isclose(ray_end.x, 0):
                    distance = (intersection.x - ray_start.x) / ray_direction.x
                elif not math.isclose(ray_end.y, 0):
                    distance = (intersection.y - ray_start.y) / ray_direction.y
                else:
                    continue

                if not math.isclose(wall.direction.x, 0):
                    on_wall = (intersection.x - wall.start.x) / wall.direction.x
                elif not math.isclose(wall.direction.y, 0):
                    on_wall = (intersection.y - wall.start.y) / wall.direction.y
                else:
                    continue

                if distance > 0 and 0 < on_wall < 1:
                    intersecting_walls.append((distance, wall, on_wall))

        intersecting_walls.sort(key=lambda x: x[0])

        if len(intersecting_walls) > 0:
            return intersecting_walls[0]
        else:
            return None

    def draw_hud(self, surface):
        money = self._font.render('Money: %03d' % self.player.money, True, (255, 0, 255))
        points = self._font.render('Points: %03d' % self.player.points, True, (255, 0, 255))

        hud = surface.copy()
        draw.rect(hud, (0, 0, 0), (0, 0, self.width, 36))
        hud.blit(money, (10, 0))
        hud.blit(points, (self.width - points.get_rect().width - 10, 0))

        api = self._apis[self.player.api]
        api_rect = api.get_rect()
        hud.blit(api, (self.width - api_rect.width, self.height - api_rect.height))

        surface.blit(hud, (0, 0))

    def draw_minimap(self, surface, player, offset):
        draw.polygon(
            surface,
            (0, 0, 0),
            list(map(lambda x: offset + x.start, self._level.walls))
        )

        for wall in self._level.walls:
            draw.line(surface, (255, 255, 255), offset + wall.start, offset + wall.end)

        draw.circle(
            surface,
            (255, 0, 0),
            offset + self.player.position,
            3
        )

        draw.line(
            surface,
            (255, 0, 0),
            offset + player.position,
            offset + player.position + player.direction * 10,
            1
        )

        for p in self._level.projectiles:
            draw.circle(
                surface,
                (0, 255, 0),
                offset + p.position,
                3
            )

    def draw_level(self, surface):
        for column in range(0, self.width):
            intersection = self._wall_intersection_at_column(column)
            wall = None
            u = None
            if intersection:
                (distance, wall, u) = intersection
                if distance == 0:
                    wall_height = 0
                else:
                    wall_height = 10000 * 1 / distance
            else:
                wall_height = 0

            pygame.draw.line(
                surface,
                (0, 0, 128),
                (column, 0),
                (column, self.height / 2 - wall_height / 2)
            )

            if wall:
                if wall.texture:
                    self.draw_textured_slice(column, surface, u, wall, wall_height)
                else:
                    pygame.draw.line(
                        surface,
                        wall.fill,
                        (column, self.height / 2 - wall_height / 2),
                        (column, self.height / 2 + wall_height / 2),
                    )

            pygame.draw.line(
                surface,
                (128, 0, 128),
                (column, self.height / 2 + wall_height / 2),
                (column, self.height)
            )

    def draw_textured_slice(self, column, surface, u, wall, wall_height):
        width = wall.texture.get_rect().width
        texture = _get_cached_and_scaled_texture(wall.fill, (width, wall_height))

        surface.blit(
            texture,
            (column, int(self.height / 2 - wall_height / 2)),
            (u * width, 0, 1, wall_height)
        )

        # for y in range(0, int(wall_height)):
        #     color = texture.get_at(
        #         (int(u * width), int((y / wall_height) * height)),
        #     )
        #
        #     surface.set_at(
        #         (column, int(self.height / 2 - wall_height / 2 + y)),
        #         color
        #     )
        #

    def draw(self):
        self._display_surf.fill((0, 0, 0))

        self.draw_level(self._display_surf)

        self.draw_hud(self._display_surf)

        self.draw_minimap(self._display_surf, self.player, Vector2(100, 50))

        pygame.display.update()
        pass

    def cleanup(self):
        pygame.quit()

    def run(self):
        self.initialize()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.update()
            self.draw()

        self.cleanup()


if __name__ == "__main__":
    print("\n\nWelcome to 5Geeeeeeeeieee!")
    geeeee = FiveGeeeeeeeee()
    geeeee.run()

    print("\n\nDone! Player got %d points." % geeeee.player.points)
