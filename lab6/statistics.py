from os.path import join as pjoin
from pygame import Rect, Color, display
from pygame.draw import ellipse as draw_ellipse
from textrender import Label


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
            print("Statistics reset.")
            self.reset()

    def add_stat(self, stat):
        death, score = stat
        stats = self.get_all()
        stats['games'][death] += 1

        stats['highscores'].append(score)
        stats['highscores'].sort(reverse=True)
        stats['highscores'].pop()  # Top 5 leave
        stats_lines = tuple(' = '.join((key, ' '.join((str(x)for x in val))))
                            + '\n'
                            for (key, val) in stats.items())

        with open(self.NAME, 'w') as f:
            f.writelines(stats_lines)

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


class Statistics:
    BLACK = Color('black')
    BG_COLOR = Color('cadetblue3')

    def __init__(self, screen, font):
        '''
        Show best score table
        '''
        self.font = font
        self.screen = screen
        self.rect = Rect(0, 0, 600, 600)
        self.rect.center = self.screen.get_rect().center

    def show(self):
        display.set_caption("Статистика")
        draw_ellipse(self.screen, self.BG_COLOR, self.rect)
        draw_ellipse(self.screen, self.BLACK, self.rect, 7)
        pos = [self.rect.centerx, self.rect.y + self.rect.h // 6]
        self.render_stats(pos)
        display.update()

    def render_stats(self, pos):
        stats = StatisticsFile().get_all(string=True)
        summary_text = f"Всего игр: {stats['games'][0]}"
        highscore_text = ("Лучшие результаты:",) +\
            tuple(score.rjust(6, '0') for score in stats['highscores'])

        summary_label = Label(pos, self.font, summary_text, color=self.BLACK)
        summary_label_rect = summary_label.render(self.screen)
        print("sum label:", summary_label_rect)
        pos[1] = summary_label_rect.bottom + 20
        print(pos)
        highscore_label = Label(pos, self.font, *highscore_text,
                                color=self.BLACK)
        highscore_label.render(self.screen)
