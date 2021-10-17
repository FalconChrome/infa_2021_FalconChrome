import pygame
from pygame.draw import rect, ellipse
from pygame.color import Color
from pygame.rect import Rect
from pic_params import *

pygame.init()

FPS = 30

size = 630, 890
bndx, bndy = 0, 0  # boundaries of picture


def draw_moved(func, *args, rect, **kwargs):
    '''Function for shift draw, helps make bounds'''
    func(*args, ((rect[0][0] - bndx, rect[0][1] - bndy), rect[1]), **kwargs)


# screen size counted with bounds
screen = pygame.display.set_mode((size[0] - 2 * bndx, size[1] - 2 * bndy))

# initial bg filling
screen.fill(WHITE)
draw_moved(rect, screen, Color('azure3'), rect=((0, 0), (630, 565)))
draw_moved(rect, screen, GROUND_GREEN, rect=((0, 570), (630, 320)))
draw_moved(ellipse, screen, Color('azure2'), rect=((-50, 740), (800, 300)))


def blit_transp(func, screen, color, rect, alpha=100):
    '''Blits with transparency a figure drawn with a func argument'''
    if type(rect) != Rect:
        rect = Rect(rect)
    # bounds for figure not to get out of surface
    bx, by = rect.w / 2, rect.h / 2
    surface = pygame.Surface((4 * bx, 4 * by))  # generating additional surface
    surface.set_colorkey(BLACK)  # making bg unblitable
    surface.set_alpha(alpha)
    func(surface, color,  ((bx, by), rect.size))
    screen.blit(surface, (rect.x - bx, rect.y - by))


def ellipse_center(surface, color, coord):
    center, (w, h) = coord
    rect = Rect(0, 0, 2 * w, 2 * h)
    rect.center = center
    ellipse(surface, color, rect)
    return rect


# Way of adjusting coordinates if getting from screen. To be removed.
# spots = [((c[0] + bndx, c[1] + bndy), s) for (c, s) in spots]
# for i in range(len(spots)):
#     # spots[i] = (spots[i][0], spots[i+1][0])
#     print('        ', spots[i], end=',\n')
for i, (color, scrapper) in enumerate(skyscrappers):
    # print(scrapper)
    w, h = scrapper[1]
    w -= scrapper[0][0]
    h -= scrapper[0][1]
    draw_moved(blit_transp, ellipse, screen, Color(PALEGRAY),
               rect=spots[i], alpha=140)
    draw_moved(rect, screen, Color(color), rect=scrapper)
for j in range(i, 7):
    draw_moved(blit_transp, ellipse, screen, Color(PALEGRAY),
               rect=spots[j], alpha=140)
    # print((w, h), end=',\n')
    # skyscrappers[i] = scrapper[0], (w, h)
# To be removed in release version.
# for it in skyscrappers.items():
#     print("'{}'".format(it[0]), it[1], sep=': ', end=',\n')
# for spot in spots:
# for h in houses:
#     blit_transp(rect, *h)

ellipse_center(screen, BLACK, car['black'][-1])
for color in car:
    if color != 'black':
        for p in car[color]:
            rect(screen, Color(color), p)
    else:
        for p in car[color][:-1]:
            ellipse_center(screen, Color(color), p)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        # Helps to get the coords of figures. No need for program correct work.
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos, end=',\n')
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.update()
pygame.quit()
