import pygame
from pygame.color import Color
from circles import Circles
from statistics import Statistics, StatisticsFile
from os import path
from textrender import Label


class Game:
    """
    The main class for controlling game flow
    """
    FONT_NAME = path.join('data', 'mr_AfronikG.ttf')
    BG_FILENAME = path.join('data', 'images', 'background.jpg')

    def __init__(self):
        """
        Setting background, generating circles
        """
        self.screen = pygame.display.set_mode(SIZE)
        self.SMALL_FONT = pygame.font.Font(self.FONT_NAME, 40)
        self.score = 0
        status_label = Label((20, 35), self.SMALL_FONT, 'Счёт: 0',
                             color=Color('orange'), align='left')
        self.status_label = status_label
        status_label.render(self.screen)
        self.lifebar_rect = pygame.Rect(status_label.rect.bottomleft,
                                        (180, 30))
        self.set_bg()
        self.gen_circles()

    def set_bg(self):
        self.bg_image = pygame.image.load(self.BG_FILENAME).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               self.screen.get_size())
        self.screen.blit(self.bg_image, ((0, 0), SIZE))
        pygame.display.update()

    def gen_circles(self):
        self.circle_group = pygame.sprite.Group()
        self.circles_set = (Circles(SIZE, self.circle_group,
                                    circle_type='osu', frequency=2, amount=10),)

    def process_event(self, event):
        """
        Process mouse click and keys press
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for circles in self.circles_set:
                # add score when clicked circle
                score = circles.click(event.pos)
                if score is not None:
                    self.score += score

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_z, pygame.K_x):
                for circles in self.circles_set:
                    # add score when clicked circle
                    score = circles.click(pygame.mouse.get_pos())
                    if score is not None:
                        self.score += score

    def status_bar(self):
        """
        Rendering status bar with score and life bar
        """
        self.status_label.set_text(f"Счёт: {round(self.score)}")
        self.status_label.render(self.screen)
        life = sum(1 - circles.fails / circles.LOSE
                   for circles in self.circles_set) / len(self.circles_set)
        life_rect = self.lifebar_rect.copy()
        life_rect.w *= life
        pygame.draw.rect(self.screen, Color('orangered'), life_rect)
        pygame.draw.rect(self.screen, Color('orange'),
                         self.lifebar_rect, width=4)

    def meet_player(self):
        """
        Ask player level of difficulty
        """
        FPS = 24
        clock = pygame.time.Clock()
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.K_UP:
                    if event.key in (pygame.K_SPACE, pygame.K_ESC,
                                     pygame.K_RETURN):
                        finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    finished = True
            clock.tick(FPS)

    def mainloop(self):
        """
        Main loop proccessing game events
        """
        FPS = 24
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.process_event(event)

            self.update(FPS)
            self.render()
            clock.tick(FPS)

    def update(self, FPS):
        """
        Update circles container and then each circle aside
        """
        for circles in self.circles_set:
            circles.update(FPS)
            if circles.complete:
                self.running = False
        self.circle_group.update(FPS, SIZE)

    def render(self):
        """
        Rendering background, circles and status bar
        """
        self.screen.blit(self.bg_image, ((0, 0), SIZE))
        self.circle_group.draw(self.screen)
        self.status_bar()

        pygame.display.update()

    def end(self):
        """
        Saving statistics
        """
        StatisticsFile().add_stat((0, round(self.score)))
        Statistics(self.screen, self.SMALL_FONT).show()

        waiting = 2
        while waiting > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        waiting -= 1

    def play(self):
        self.meet_player()
        self.mainloop()
        self.end()


if __name__ == "__main__":
    pygame.init()
    SIZE = 1600, 960
    game = Game()
    game.play()
    pygame.quit()
