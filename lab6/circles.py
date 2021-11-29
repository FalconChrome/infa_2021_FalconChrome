from pygame import sprite, surface, Color
from pygame.draw import circle
from pygame.transform import rotozoom
from pygame.math import Vector2 as Vec
from random import randint

E = 2.718281828

BLACK = Color("black")


def randsign():
    return randint(0, 1) * 2 - 1


def randintsigned(a, b):
    return randint(a, b) * randsign()


class Circle(sprite.Sprite):
    R_MIN = 30
    R_MAX = 60

    def gen_image(self, r, hue):
        """
        Function generating circle image
        """
        image = surface.Surface((2 * r,) * 2)
        image.set_colorkey(BLACK)
        color = Color(BLACK)
        color.hsla = ((hue + randint(-10, 10)) % 360,
                      (r - self.R_MIN) * 90 // (self.R_MAX - self.R_MIN),
                      (r - self.R_MIN + 1) * 90
                      // (self.R_MAX - self.R_MIN + 1),
                      100)
        circle(image, color, (r, r), r)
        return image

    def __init__(self, bounds, *groups, hue=None):
        super().__init__(*groups)
        self.r = randint(self.R_MIN, self.R_MAX)
        if hue is None:
            hue = randint(0, 360)
        self.image = self.gen_image(self.r, hue)
        self.rect = self.image.get_rect()
        self.rect.move_ip(randint(100, bounds[0] - 100),
                          randint(100, bounds[1] - 100))

    def click(self, pos):
        return ((self.rect.centerx - pos[0]) ** 2 +
                (self.rect.centery - pos[1]) ** 2) < self.r ** 2

    def update(self, *args):
        pass

    def score(self):
        return 1


class MovingCircle(Circle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.v = [randintsigned(20, 100) for _ in range(2)]

    def update(self, FPS, size, *args):
        """
        Move circle
        """
        super().update(*args)
        new_coords = []
        for i in range(2):
            new_coord = self.rect.center[i] + self.v[i] / FPS
            if self.r > new_coord:
                new_coord = 2 * self.r - new_coord
                self.v[i] *= -1
            elif new_coord > size[i] - self.r:
                new_coord = 2 * (size[i] - self.r) - new_coord
                self.v[i] *= -1
            new_coords.append(new_coord)
        self.rect.center = tuple(new_coords)


class CircleOsu(Circle):
    prev_circle = Vec(200, 200)
    prev_diff = Vec(200, 200)

    def __init__(self, interval, N, bounds, *args, **kwargs):
        super().__init__(bounds, *args, **kwargs)
        self.count = 0
        self.max_count = self.gen_timing(interval, N)
        pos = self.gen_pos(bounds)
        self.rect.center = pos
        CircleOsu.prev_diff = pos - self.prev_circle
        CircleOsu.prev_circle = pos

        self.init_image = self.image.copy()
        self.init_r = self.r
        self.end_image = self.gen_end_image(self.r)
        self.step_image()

    def gen_pos(self, bounds):
        new_diff = self.prev_diff.rotate(randint(-60, 60))\
                   * randint(20, 30) / 25
        if new_diff.magnitude_squared() < 100 ** 2:
            pos = self.prev_circle + Vec([randintsigned(100, 300)
                                         for _ in range(2)])
        else:
            pos = self.prev_circle + new_diff
        for (i, coord) in enumerate(pos):
            if coord < 100:
                pos[i] = 200 - coord
            elif coord > bounds[i] - 100:
                pos[i] = 2 * (bounds[i] - 100) - coord
        return pos

    def gen_timing(self, interval, N):
        k = 64
        return randint(k * (N - 2), k * (N - 1.5)) / k * max(interval, 1)

    def step_image(self):
        factor = self.count / self.max_count
        self.image = rotozoom(self.init_image, 0, factor)
        self.image.set_colorkey(BLACK)
        self.r = self.init_r * factor

    def gen_end_image(self, r):
        end_image = self.init_image.copy()
        circle(end_image, Color("navy"), (r, r), r, width=r//6)
        return end_image

    def update(self, *args):
        super().update(*args)
        self.count += 1
        if self.count < self.max_count - 1:
            self.step_image()
        elif self.count == int(self.max_count - 1) + 1:
            self.image = self.end_image
            self.r = self.init_r

    def score(self):
        accuracy = abs(self.count - self.max_count) / self.max_count
        if accuracy <= 0.05:  # Pure perfect
            score = 2
        elif accuracy <= 0.25:  # Perfect
            score = 2 - 16 * accuracy ** 2
        elif accuracy <= 0.5:  # Good
            score = 1.5 - 2 * accuracy
        else:  # Bad
            score = 0.5 / accuracy - 0.5
        return round(score, 2)


class MovingCircleOsu(MovingCircle, CircleOsu):
    def score(self):
        base_score = super().score()
        return base_score * 1.5


class Circles:
    N_MAX = 5
    TYPES = {'': Circle, 'moving': MovingCircle, 'osu': CircleOsu,
             'movingosu': MovingCircleOsu}

    def __init__(self, bounds, *groups, circle_type='', frequency=2):
        self.groups = groups
        self.bounds = bounds
        self.circle_type = circle_type
        self.Circle = Circles.TYPES[circle_type]
        self.circles = []
        self.frequency = frequency
        self.count = 0
        self.color = 180

    def gen_rand_circle(self, *args):
        self.circles.append(
            self.Circle(*args, self.bounds, *self.groups, hue=self.color)
        )

    def kill_circle(self, index=0):
        try:
            victim = self.circles.pop(index)
            score = victim.score()
            victim.kill()
            return score
        except IndexError:
            return None

    def click(self, pos):
        for (i, c) in enumerate(self.circles):
            if c.click(pos):
                score = self.kill_circle(i)
                return score

    def update(self, FPS):
        if self.count >= FPS / self.frequency:
            if len(self.circles) >= self.N_MAX:
                self.kill_circle()
            if 'osu' in self.circle_type:
                self.gen_rand_circle(FPS / self.frequency, self.N_MAX)
            else:
                self.gen_rand_circle()
            self.count = 0
            # self.color += 20
        self.count += 1
