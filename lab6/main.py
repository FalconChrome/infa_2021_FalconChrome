import pygame
from pygame.color import Color
from circles import Circles
import os
from os import path

pygame.init()


def render_text(surface, text, text_coord, font, color=None, align='center'):
    if color is None:
        color = pygame.color.Color('gray')
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.midtop = text_coord
    elif align == 'left':
        text_rect.topleft = text_coord
    elif align == 'right':
        text_rect.topright = text_coord

    surface.blit(text_surface, text_rect)
    return text_rect.height


class StatisticsFile:
    """
    Distinct class for safe work with statistics file
    While initializing checks the file format
    games - number of played games
    highscores - 5 best scores
    """
    NAME = os.path.join('data', 'statistics.txt')
    OPTIONS = {'games': 0, 'highscores': 1}  # Sequence of values saving

    def reset(self):
        with open(self.NAME, 'w') as f:
            f.writelines(('games = 0\n'  # format of file
                          'highscores = 0 0 0 0 0\n'))

    def __init__(self):
        try:
            stats = self.get_all()
            # checking format
            if not(len(stats['games']) == 1 and
                   len(stats['highscores']) == 5):
                self.reset()
        except (FileNotFoundError, ValueError, KeyError):
            self.reset()

    def add_stat(self, stat):
        death, score = stat
        stats = self.get_all()

        stats['games'][death] += 1

        stats['highscores'].append(score)
        stats['highscores'].sort(reverse=True)
        stats['highscores'].pop()  # Top 5 leave

        stats = tuple(' = '.join((key, ' '.join((str(x) for x in val)))) + '\n'
                      for (key, val) in stats.items())

        with open(self.NAME, 'w') as f:
            f.writelines(stats)

    def get(self, option):
        with open(self.NAME) as f:
            stats = f.readlines()
        return stats[self.OPTIONS[option]].strip().split(' = ')[1].split()

    def get_all(self, string=False):
        with open(self.NAME) as f:
            stats = f.readlines()
        stats = dict(line.strip().split(' = ') for line in stats)
        if not string:
            stats = {key: [int(x) for x in stats[key].split()]
                     for key in stats}
        else:
            stats = {key: stats[key].split() for key in stats}
        return stats


class Game:
    """
    The main class for controlling game flow
    """
    FONT_NAME = path.join('data', 'mr_AfronikG.ttf')
    SMALL_FONT = pygame.font.Font(FONT_NAME, 40)
    BG_FILENAME = path.join('data', 'images', 'background.jpg')

    def __init__(self):
        '''
        Setting background, generating circles
        '''
        self.score = 0
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
        '''
        Process mouse click and keys press
        '''
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
        render_text(screen, f"Счёт: {round(self.score, 2)}",
                    (20, 10), self.SMALL_FONT,
                    color=Color('lightgray'), align='left')

    def mainloop(self):
        '''
        Main loop proccessing game events
        '''
        FPS = 24
        clock = pygame.time.Clock()
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                    finished = True
                else:
                    self.process_event(event)

            self.update(FPS)
            self.render()
            clock.tick(FPS)

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
        StatisticsFile().add_stat((0, self.score))
        self.show_statistics()

    def show_statistics(self):
        '''
        Show best score table
        '''
        pass


if __name__ == "__main__":
    try:
        size = 1600, 960
        screen = pygame.display.set_mode(size)
        game = Game()
        game.mainloop()
    finally:
        pygame.quit()
