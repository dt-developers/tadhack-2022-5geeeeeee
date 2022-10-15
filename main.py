#
#

# ignore pygame advertisement, sorry just to self aware lib
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame import image, display, draw
from pygame.math import Vector2

from random import Random


class Player:
    def __init__(self):
        self.position = Vector2(50, 50)
        self.direction = Vector2(0, -1)
        self.speed = .1
        self.turn_speed = 1
        self.money = 100
        self.points = 0
        self.api = 0


class Wall:
    def __init__(self, start, end, texture_index):
        self.start = start
        self.end = end
        self.direction = end - start
        self.texture_index = texture_index


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
            Wall(Vector2(0, 0), Vector2(100, 0), 0),
            Wall(Vector2(100, 0), Vector2(100, 100), 1),
            Wall(Vector2(100, 100), Vector2(0, 100), 2),
            Wall(Vector2(0, 100), Vector2(0, 0), 3),
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

    def wall_intersection_at_column(self, column):
        fov = 60

        # direction of ray
        direction = self.player.direction.rotate(-fov / 2)
        direction.rotate_ip(fov * (column / self.width))

        intersecting_walls = list()

        pd = self.player.direction
        for wall in self._level.walls:
            wd = wall.direction
            dot = wd.dot(pd)

            if dot < 0:
                # not hitting
                continue
            else:




            if 0 < column < 1:
                distance = (intersection - self.player.position) / self.player.direction
            intersecting_walls.append((distance, wall))
            else:
                continue

        if len(intersecting_walls) > 0:
            intersecting_walls.sort(key=lambda it: it[0])
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

    def draw_player(self, surface, player):
        draw.circle(
            surface,
            (255, 0, 0),
            self.player.position,
            5
        )

        draw.line(
            surface,
            (255, 0, 0),
            player.position,
            player.position + player.direction * 10,
            1
        )

        for p in self._level.projectiles:
            draw.circle(
                surface,
                (0, 255, 0),
                p.position,
                3
            )

    def draw_level(self, surface):
        for w in range(0, self.width):
            intersection = self.wall_intersection_at_column(w)
            if intersection:
                (distance, wall) = intersection
                wall_height = 1 / distance
            else:
                wall_height = 0

            pygame.draw.line(
                surface,
                (0, 0, 255),
                (w, 0),
                (w, self.height / 2 - wall_height / 2)
            )
            pygame.draw.line(
                surface,
                (0, 255, 255),
                (w, self.height / 2 - wall_height / 2),
                (w, self.height / 2 + wall_height / 2)
            )
            pygame.draw.line(
                surface,
                (255, 0, 255),
                (w, self.height / 2 + wall_height / 2),
                (w, self.height)
            )

    def draw(self):
        self._display_surf.fill((255, 0, 255))

        self.draw_level(self._display_surf)

        self.draw_hud(self._display_surf)

        # debug
        self.draw_player(self._display_surf, self.player)

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
