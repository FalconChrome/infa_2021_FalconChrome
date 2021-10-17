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


def draw_scrappers(surface):
    for i, (color, scrapper) in enumerate(skyscrappers):
        # print(scrapper)
        w, h = scrapper[1]
        w -= scrapper[0][0]
        h -= scrapper[0][1]
        draw_moved(rect, surface, Color(color), rect=scrapper)


def draw_scrappers_orig(surface):
    for i, (color, scrapper) in enumerate(skyscrappers):
        # print(scrapper)
        w, h = scrapper[1]
        w -= scrapper[0][0]
        h -= scrapper[0][1]
        draw_moved(blit_transp, ellipse, surface, Color(PALEGRAY),
                   rect=spots[i], alpha=140)
        draw_moved(rect, surface, Color(color), rect=scrapper)


def draw_spots(surface, nums=None):
    if nums is None:
        nums = range(7)
    for j in nums:
        draw_moved(blit_transp, ellipse, surface, Color(PALEGRAY),
                   rect=spots[j], alpha=140)


def draw_car(surface):
    ellipse_center(screen, BLACK, car['black'][-1])
    for color in car:
        if color != 'black':
            for p in car[color]:
                rect(screen, Color(color), p)
        else:
            for p in car[color][:-1]:
                ellipse_center(screen, Color(color), p)


draw_scrappers_orig(screen)
draw_spots(screen, range(4, 7))
draw_car(screen)

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
