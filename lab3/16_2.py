import pygame
from pygame.transform import flip, scale, rotozoom
from pygame.draw import rect, ellipse
from pygame.color import Color
from pygame.rect import Rect
from pic_params import *

pygame.init()
size = 630, 890
FPS = 30

bndx, bndy = 0, 0  # boundaries of picture


def draw_bounded(func, *args, rect, **kwargs):
    '''Function for shift draw, helps make bounds'''
    func(*args, ((rect[0][0] - bndx, rect[0][1] - bndy), rect[1]), **kwargs)


# screen size counted with bounds
screen = pygame.display.set_mode((size[0] - 2 * bndx, size[1] - 2 * bndy))


def blit_transp(draw_figure, screen, rect, color=WHITE, alpha=100):
    '''Blits with transparency a figure drawn with a func argument'''
    if type(rect) != Rect:
        rect = Rect(rect)
    # bounds for figure not to get out of surface
    bx, by = rect.w / 2, rect.h / 2
    surface = pygame.Surface((4 * bx, 4 * by))  # generating additional surface
    surface.set_colorkey(BLACK)  # making bg unblitable
    surface.set_alpha(alpha)
    draw_figure(surface, color, ((bx, by), rect.size))
    screen.blit(surface, (rect.x - bx, rect.y - by))


def master_draw(screen, draw_pic, *args, scale_factor=1, fit_rect=None,
                orig_size=(630, 890), reverse=False, rotation=False,
                alpha=255, **kwargs):
    '''
    Mastering component to the result screen.
    With a given fit_rect brings a picture to that's size
    from original size of drawing.
    '''
    if fit_rect is None:
        fit_rect = Rect(screen)
    elif type(fit_rect) != Rect:
        fit_rect = Rect(fit_rect)
    elif scale_factor == 1:
        scale_factor = fit_rect.w / orig_size[0]
    surface = pygame.Surface(orig_size)
    draw_pic(surface, *args, **kwargs)
    if rotation:
        rotozoom(screen, rotation, scale_factor)
    else:
        scale(screen, scale_factor)
    if reverse:
        flip(surface)
    blit_transp(lambda *args: None, screen, WHITE, fit_rect, alpha=alpha)


def draw_bg(screen):
    '''
    Draws a background of the picture.
    '''
    screen.fill(WHITE)
    draw_bounded(rect, screen, Color('azure3'), rect=((0, 0), (630, 565)))
    draw_bounded(rect, screen, GROUND_GREEN, rect=((0, 570), (630, 320)))
    draw_bounded(ellipse, screen, Color('azure2'),
                 rect=((-50, 740), (800, 300)))


def ellipse_center(surface, color, coord):
    '''
    Draw an ellipse with given center coordinates of that.
    surface - pygame.Surface object
    color - pygame.Color object or corresponding tuple
    coord - coordinate of the center
    '''
    center, (w, h) = coord
    rect = Rect(0, 0, 2 * w, 2 * h)
    rect.center = center
    ellipse(surface, color, rect)
    return rect


def draw_scrappers(surface):
    '''
    Function drawing the scrappers with parameters from data.
    '''
    for i, (color, scrapper) in enumerate(skyscrappers):
        # print(scrapper)
        w, h = scrapper[1]
        w -= scrapper[0][0]
        h -= scrapper[0][1]
        draw_bounded(rect, surface, Color(color), rect=scrapper)


def draw_scrappers_orig(surface):
    '''
    Function drawing the scrappers with parameters from data.
    Interfering with spots.
    '''
    for i, (color, scrapper) in enumerate(skyscrappers):
        # print(scrapper)
        w, h = scrapper[1]
        w -= scrapper[0][0]
        h -= scrapper[0][1]
        draw_bounded(blit_transp, ellipse, surface, color=Color(PALEGRAY),
                     rect=spots[i], alpha=140)
        draw_bounded(rect, surface, Color(color), rect=scrapper)


def draw_spots(surface, nums=None):
    '''
    Function drawing the spots with parameters from data.
    '''

    if nums is None:
        nums = range(7)
    for j in nums:
        draw_bounded(blit_transp, ellipse, surface, color=Color(PALEGRAY),
                     rect=spots[j], alpha=140)


def draw_car(surface):
    '''
    Function drawing the car with parameters from data.
    '''
    ellipse_center(screen, BLACK, car['black'][-1])
    for color in car:
        if color != 'black':
            for p in car[color]:
                rect(screen, Color(color), p)
        else:
            for p in car[color][:-1]:
                ellipse_center(screen, Color(color), p)


def draw_result_picture(screen):
    '''
    Function drawing the whole picture with parameters from data.
    '''
    draw_bg(screen)
    draw_scrappers_orig(screen)
    draw_spots(screen, range(4, 7))
    draw_car(screen)


draw_result_picture(screen)
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
