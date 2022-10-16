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

DEBUG = False

TEXTURES = {}


def _get_cached_texture(filename):
    try:
        if os.path.exists(filename) and filename not in TEXTURES:
            TEXTURES[filename] = image.load(filename)

        return TEXTURES[filename]
    except TypeError:
        return None


class APICall:
    def __init__(self, hand_texture, loading_time, session_color, session_size, session_cost):
        self.hand_texture = hand_texture
        self.loading_time = loading_time
        self.session_color = session_color
        self.session_size = session_size
        self.session_cost = session_cost


class Player:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.direction = Vector2(0, 1)
        self.speed = 1
        self.turn_speed = 3
        self.money = 100
        self.points = 0
        self.api = "default"
        self.fov = 60
        self.last_shot = pygame.time.get_ticks()


class Wall:
    def __init__(self, start, end, fill):
        self.start = start
        self.end = end
        self.equation = Vector3(end.y - start.y, -(end.x - start.x), end.x * start.y - start.x * end.y)
        self.direction = (end - start)
        self.fill = fill
        self.texture = _get_cached_texture(fill)


class Session:
    def __init__(self, position, direction, api, speed=3, alive_time=1000):
        self.position = position
        self.direction = direction
        self.api = api
        self.speed = speed
        self.birth_time = pygame.time.get_ticks()
        self.alive_time = alive_time


class Level:
    def __init__(self):
        self.walls = (
            Wall(Vector2(-10, 10), Vector2(-10, -10), (200, 200, 200)),
            Wall(Vector2(-10, -10), Vector2(10, -10), (200, 200, 200)),
            Wall(Vector2(10, -10), Vector2(10, 10), (200, 200, 200)),
            # Wall(Vector2(-10, 10), Vector2(-10, -10), "assets/wall_bricks.png"),
            # Wall(Vector2(-10, -10), Vector2(10, -10), "assets/wall_bricks.png"),
            # Wall(Vector2(10, -10), Vector2(10, 10), "assets/wall_bricks.png"),
            Wall(Vector2(10, 10), Vector2(50, 10), (200, 200, 200)),
            Wall(Vector2(50, 10), Vector2(50, 100), (200, 200, 200)),
            Wall(Vector2(50, 100), Vector2(0, 100), (200, 200, 200)),
            Wall(Vector2(0, 100), Vector2(-50, 100), (200, 200, 200)),
            Wall(Vector2(-50, 100), Vector2(-50, 10), (200, 200, 200)),
            Wall(Vector2(-50, 10), Vector2(-10, 10), (200, 200, 200)),
        )
        self.enemies = ()
        self.sessions = list()


class FiveGeeeeeeeee:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self._running = True
        self._icon = None
        self._font = None
        self._display_surf = None
        self._r = Random()
        self._level = Level()
        self._api_calls = None
        self._keys_down = set()
        self.player = Player()

    def initialize(self):
        pygame.init()
        display.set_caption("5geeeeeeeee")

        self._display_surf = display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._font = pygame.font.SysFont("", 48)

        self._icon = image.load("./assets/icon.png")
        display.set_icon(self._icon)

        self._api_calls = {
            "default": APICall(image.load("./assets/api_default.png"), 300, (128, 128, 128), 50, 0),
            "latency": APICall(image.load("./assets/api_latency.png"), 10, (255, 0, 0), 20, 1),
            "throughput": APICall(image.load("./assets/api_throughput.png"), 1000, (255, 255, 0), 200, 10),
        }

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

            self._keys_down.add(event.key)

    def update_inputs(self):
        if pygame.K_DOWN in self._keys_down or pygame.K_s in self._keys_down:
            self.player.position -= self.player.direction * self.player.speed
        if pygame.K_UP in self._keys_down or pygame.K_w in self._keys_down:
            self.player.position += self.player.direction * self.player.speed
        if pygame.K_a in self._keys_down:
            self.player.position -= self.player.direction.rotate(90) * self.player.speed
        if pygame.K_d in self._keys_down:
            self.player.position += self.player.direction.rotate(90) * self.player.speed

        if pygame.K_LEFT in self._keys_down:
            self.player.direction.rotate_ip(-self.player.turn_speed)
        if pygame.K_RIGHT in self._keys_down:
            self.player.direction.rotate_ip(self.player.turn_speed)

        if pygame.K_1 in self._keys_down:
            self.player.api = "default"
        if pygame.K_2 in self._keys_down:
            self.player.api = "latency"
        if pygame.K_3 in self._keys_down:
            self.player.api = "throughput"

        if pygame.K_SPACE in self._keys_down:
            now = pygame.time.get_ticks()
            api = self._api_calls[self.player.api]
            if self.player.money > api.session_cost:
                if now > self.player.last_shot + api.loading_time:
                    self._level.sessions.append(
                        Session(
                            self.player.position.copy(),
                            self.player.direction.copy(),
                            self.player.api
                        )
                    )
                    self.player.last_shot = now
                    self.player.money -= api.session_cost

        # DEBUG
        if pygame.K_TAB in self._keys_down:
            if self.player.api == "latency":
                self.player.api = "throughput"
            elif self.player.api == "throughput":
                self.player.api = "default"
            else:
                self.player.api = "latency"

    def update_sessions(self):
        now = pygame.time.get_ticks()
        for session in self._level.sessions:
            session.position += session.direction * session.speed
            if now > session.birth_time + session.alive_time:
                self._level.sessions.remove(session)
            else:
                for wall in self._level.walls:
                    a, b, c = wall.equation
                    x, y = session.position
                    if math.isclose(a * x + b * y + c, 0):
                        # collission
                        if session in self._level.sessions:
                            self._level.sessions.remove(session)

    def update(self):
        self.update_inputs()
        self.update_sessions()

    def _wall_intersection_at_column(self, column):
        ray_direction = self.player.direction.rotate(-self.player.fov / 2)
        ray_direction.rotate_ip(self.player.fov * (column / self.width))

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

        api = self._api_calls[self.player.api]
        api_rect = api.hand_texture.get_rect()
        hud.blit(api.hand_texture, (self.width - api_rect.width, self.height - api_rect.height))

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
            offset + player.position + player.direction.rotate(player.fov / -2) * 100,
            1
        )

        draw.line(
            surface,
            (255, 0, 0),
            offset + player.position,
            offset + player.position + player.direction * 20,
            1
        )

        draw.line(
            surface,
            (255, 0, 0),
            offset + player.position,
            offset + player.position + player.direction.rotate(player.fov / 2) * 100,
            1
        )

        for p in self._level.sessions:
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
        texture = pygame.transform.scale(
            wall.texture,
            (width, wall_height)
        )

        surface.blit(
            texture,
            (column, int(self.height / 2 - wall_height / 2)),
            (u * width, 0, 1, wall_height)
        )

    def draw_sessions(self, surface, sessions):
        player = self.player
        fov = player.fov
        near = 50
        offset = Vector2(100, 50)

        for session in sessions:
            x0 = player.position + player.direction.rotate(-fov / 2) * near

            xw = player.position + player.direction.rotate(fov / 2) * near
            xv = xw - x0

            if DEBUG:
                draw.circle(surface, (0, 0, 128), offset + x0, 2)
                draw.circle(surface, (0, 0, 128), offset + xw, 2)
                draw.line(surface, (0, 0, 128), offset + x0, offset + xw)

            s = session.position
            p = player.position

            equation_x = Vector3(xw.y - x0.y, -(xw.x - x0.x), xw.x * x0.y - x0.x * xw.y)
            equation_ps = Vector3(s.y - p.y, -(s.x - p.x), s.x * p.y - p.x * s.y)

            intersection = equation_x.cross(equation_ps)
            if intersection.z < 0 or not math.isclose(intersection.z, 0):
                intersection = intersection.xy / intersection.z

                x = (intersection.x - x0.x) / xv.x
                if 0 < x < 1:
                    if DEBUG:
                        # projected
                        draw.circle(surface, (255, 255, 0), offset + intersection, 2)

                    # real
                    api = self._api_calls[session.api]

                    draw.circle(
                        surface,
                        api.session_color,
                        (x * self.width, self.height / 2),
                        api.session_size * 10 / player.position.distance_to(intersection)
                    )

    def draw(self):
        self._display_surf.fill((0, 0, 0))

        self.draw_level(self._display_surf)

        self.draw_minimap(self._display_surf, self.player, Vector2(100, 50))

        self.draw_sessions(self._display_surf, self._level.sessions)

        self.draw_hud(self._display_surf)

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
