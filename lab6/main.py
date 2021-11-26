import pygame
from pygame.color import Color
from circles import Circles
from statistics import Statistics, StatisticsFile
from os import path
from rendering import Label, render_text


class Game:
    """
    The main class for controlling game flow
    """
    FONT_NAME = path.join('data', 'mr_AfronikG.ttf')
    BG_FILENAME = path.join('data', 'images', 'background.jpg')

    def __init__(self):
        '''
        Setting background, generating circles
        '''
        self.SMALL_FONT = pygame.font.Font(self.FONT_NAME, 40)
        # self.MED_FONT = pygame.font.Font(FONT_NAME, 35)
        self.score = 0
        self.status_rect = pygame.Rect(0, 0, 150, 50)
        self.set_bg()
        self.gen_circles()

    def set_bg(self):
        self.bg_image = pygame.image.load(self.BG_FILENAME).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               screen.get_size())
        screen.blit(self.bg_image, ((0, 0), size))
        pygame.display.update()

    def gen_circles(self):
        self.circle_group = pygame.sprite.Group()
        self.circles_set = (Circles(size, self.circle_group,
                                    circle_type='osu', frequency=2),)

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

    def status_bar(self, screen):
        '''
        Rendering status bar with score
        '''
        # screen.fill(Color('cadetblue3'), self.status_rect)
        render_text(screen, f"Счёт: {round(self.score, 2)}",
                    (20, 35), self.SMALL_FONT,
                    color=Color('orange'), align='left').inflate(2, 2)

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
                    return 0
                elif event.type == pygame.K_UP:
                    if event.key in (pygame.K_SPACE, pygame.K_ESC,
                                     pygame.K_RETURN):
                        return 1
            clock.tick(FPS)

    def mainloop(self):
        """
        Main loop proccessing game events
        """
        FPS = 24
        clock = pygame.time.Clock()
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                else:
                    self.process_event(event)

            self.update(FPS)
            self.render()
            clock.tick(FPS)

    def play(self):
        self.meet_player()
        self.mainloop()
        self.end()

    def update(self, FPS):
        '''
        Update circles container and then each circle aside
        '''
        for circles in self.circles_set:
            circles.update(FPS)
        self.circle_group.update(FPS, size)

    def render(self):
        '''
        Rendering background, circles and status bar
        '''
        screen.blit(self.bg_image, ((0, 0), size))
        self.circle_group.draw(screen)
        self.status_bar(screen)

        pygame.display.update()

    def end(self):
        '''
        Saving statistics
        '''
        StatisticsFile().add_stat((0, round(self.score)))
        Statistics(screen, self.SMALL_FONT).show()

        waiting = 2
        while waiting > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        waiting -= 1


if __name__ == "__main__":
    try:
        pygame.init()
        size = 1600, 960
        screen = pygame.display.set_mode(size)
        game = Game()
        game.play()
    finally:
        pygame.quit()
