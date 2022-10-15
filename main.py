import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from random import Random


class Player:
    def __init__(self):
        self.position = self.x, self.y = 0, 0
        self.weapons = ()
        self.money = 100
        self.points = 0


class Level:
    def __init__(self):
        self.walls = ()
        self.enemies = ()


class FiveGeeeeeeeee:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self._icon = pygame.image.load("./icon.png")
        self._running = True
        self._display_surf = None
        self._r = Random()
        self._level = Level()
        self.player = Player()

    def initialize(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("5geeeeeeeee")
        pygame.display.set_icon(self._icon)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False

    def update(self):
        pass

    def wall_height(self, x):
        distance = x * x
        return self.width - self._r.randint(int(self.width / 3), int(2 * self.width / 3))

    def draw(self):
        self._display_surf.fill((255, 0, 255))

        for w in range(0, self.width):
            wall_height = self.wall_height(w)

            pygame.draw.line(
                self._display_surf,
                (0, 0, 255),
                (w, 0),
                (w, self.height / 2 - wall_height / 2)
            )
            pygame.draw.line(
                self._display_surf,
                (0, 255, 255),
                (w, self.height / 2 - wall_height / 2),
                (w, self.height / 2 + wall_height / 2)
            )
            pygame.draw.line(
                self._display_surf,
                (255, 0, 255),
                (w, self.height / 2 + wall_height / 2),
                (w, self.height)
            )

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
