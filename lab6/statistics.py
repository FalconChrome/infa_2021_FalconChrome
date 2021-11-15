from os.path import join as pjoin
from pygame import Rect, Color, display
from pygame.draw import ellipse as draw_ellipse
from rendering import render_text


class StatisticsFile:
    """
    Distinct class for safe work with statistics file
    While initializing checks the file format
    games - number of played games
    highscores - 5 best scores
    """
    NAME = pjoin('data', 'statistics.txt')
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
        except (FileNotFoundError, ValueError, KeyError) as e:
            print(e)
            self.reset()

    def add_stat(self, stat):
        death, score = stat
        stats = self.get_all()
        print("stats now:", stats)
        stats['games'][death] += 1

        stats['highscores'].append(score)
        stats['highscores'].sort(reverse=True)
        stats['highscores'].pop()  # Top 5 leave
        stats_lines = tuple(' = '.join((key, ' '.join((str(x)for x in val))))
                            + '\n'
                            for (key, val) in stats.items())

        print("stat lines:", stats_lines)
        with open(self.NAME, 'w') as f:
            f.writelines(stats_lines)
        with open(self.NAME) as f:
            print("stat file after:", f.read())

    def get(self, option):
        with open(self.NAME) as f:
            stats = f.readlines()
        return stats[self.OPTIONS[option]].strip().split(' = ')[1].split()

    def get_all(self, string=False):
        with open(self.NAME) as f:
            stats = f.readlines()
            print("got:", stats)
        stats = dict(line.strip().split(' = ') for line in stats)
        if not string:
            stats = {key: [int(x) for x in stats[key].split()]
                     for key in stats}
        else:
            stats = {key: stats[key].split() for key in stats}
        return stats


class Statistics:
    BLACK = Color('black')
    BG_COLOR = Color('cadetblue3')

    def __init__(self, screen, font):
        '''
        Show best score table
        '''
        self.font = font
        self.screen = screen

    def show(self):
        stats_rect = Rect(0, 0, 600, 600)
        stats_rect.center = self.screen.get_rect().center
        display.set_caption("Статистика")
        draw_ellipse(self.screen, self.BG_COLOR, stats_rect)
        draw_ellipse(self.screen, self.BLACK, stats_rect, 7)
        pos = [stats_rect.centerx, stats_rect.y + stats_rect.h // 6]
        self.render_stats(pos)
        display.update()

    def render_stats(self, pos):
        stats = StatisticsFile().get_all(string=True)
        text = (f"Всего игр: {stats['games'][0]}",
                "Лучшие результаты:",
                *(score.rjust(6, '0') for score in stats['highscores']))

        pos[1] += self.step_line(text[0], pos) + 20
        for line in text[1:]:
            pos[1] += self.step_line(line, pos)

    def step_line(self, line, pos):
        h = render_text(self.screen, line, pos, self.font, self.BLACK).h
        return 20 + h
