import pygame
from pygame.transform import flip, scale, rotozoom
from pygame.draw import rect as draw_rect, ellipse as draw_ellipse
from pygame.color import Color
from pygame.rect import Rect
from pic_params import WHITE, BLACK, PALEGRAY, GROUND_GREEN
import pic_params as pic
# pygame.draw.Draw
pygame.init()
size = 630, 1080
FPS = 30

bndx, bndy = -5, -5  # boundaries of picture


def draw_bounded(surface, func, *args, rect, **kwargs):
    '''Function for shift draw, helps make bounds'''
    func(surface, *args, ((rect[0][0] - bndx, rect[0][1] - bndy),
         rect[1]), **kwargs)


# screen size counted with bounds
screen = pygame.display.set_mode((size[0] - 2 * bndx, size[1] - 2 * bndy))


def blit_transp(screen, draw_figure, rect, color=WHITE, colorkey=BLACK,
                alpha=100):
    '''Blits with transparency a figure drawn with a func argument'''
    if type(rect) != Rect:
        rect = Rect(rect)
    # bounds for figure not to get out of surface
    bx, by = rect.w / 2, rect.h / 2
    surface = pygame.Surface((4 * bx, 4 * by))  # generating additional surface
    surface.set_colorkey(colorkey)  # making bg unblitable
    draw_figure(surface, color, ((bx, by), rect.size))
    # screen.blit(surface,screen (rect.x - bx, rect.y - by))
    print("blitted", draw_figure)


def master_draw(screen, draw_pic, *args, scale_factor=(1, 1), fit_rect=None,
                orig_size=(630, 890), reverse=False, rotation=False,
                alpha=5, colorkey=BLACK, **kwargs):
    '''
    Mastering component to the result screen.
    With a given fit_rect brings a picture to that's size
    from original size of drawing.
    '''
    if fit_rect is None:
        fit_rect = Rect(screen)
    elif scale_factor == (1, 1):
        scale_factor = (fit_rect.w // orig_size[0], fit_rect.h // orig_size[1])
    elif type(fit_rect) != Rect:
        fit_rect = Rect(fit_rect)
    surface = pygame.Surface(orig_size)
    draw_pic(surface, *args, **kwargs)
    if rotation:
        surface = rotozoom(surface, rotation, scale_factor)
    else:
        surface = scale(surface, scale_factor)
    if reverse:
        surface = flip(surface)

    blit_transp(screen, lambda some_surf, color, rect: some_surf.blit(surface,
                rect), fit_rect, alpha=alpha)

    print("blitted", )


def draw_bg(screen):
    '''
    Draws a background of the picture.
    '''
    screen.fill(WHITE)
    draw_bounded(screen, draw_rect, Color('azure3'), rect=((0, 0), (630, 565)))
    draw_bounded(screen, draw_rect, GROUND_GREEN, rect=((0, 570), (630, 320)))
    # draw_bounded(ellipse, screen, Color('azure2'),
    #              rect=((-50, 740), (800, 300)))


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
    draw_ellipse(surface, color, rect)
    return rect


def draw_scrappers(surface):
    '''
    Function drawing the scrappers with parameters from data.
    '''
    surface.fill(Color('white'))
    draw_bounded(surface, draw_rect, Color('azure3'),
                 rect=((0, 0), (630, 565)))
    for i, (color, scrapper) in enumerate(pic.skyscrappers):
        draw_bounded(surface, draw_rect, Color(color), rect=scrapper)
        # screen.blit(surface, Rect((0, 0), (500, 500)))


def draw_scrappers_orig(surface):
    '''
    Function drawing the scrappers with parameters from data.
    Interfering with spots.
    '''
    for i, (color, scrapper) in enumerate(pic.skyscrappers):
        draw_bounded(screen, blit_transp, draw_ellipse, color=Color(PALEGRAY),
                     rect=pic.spots[i], alpha=140)
        draw_bounded(surface, draw_rect, Color(color), rect=scrapper)


def draw_spots(surface, nums=None):
    '''
    Function drawing the spots with parameters from data.
    '''

    if nums is None:
        nums = range(7)
    for j in nums:
        draw_bounded(blit_transp, screen, draw_ellipse, color=Color(PALEGRAY),
                     rect=pic.spots[j], alpha=140)


def draw_car(surface):
    '''
    Function drawing the car with parameters from data.
    '''
    ellipse_center(screen, BLACK, pic.car['black'][-1])
    for color in pic.car:
        if color != 'black':
            for p in pic.car[color]:
                draw_rect(screen, Color(color), p)
        else:
            for p in pic.car[color][:-1]:
                ellipse_center(screen, Color(color), p)


def draw_brand_new_picture(screen):
    '''
    Function drawing the whole picture with parameters from data.
    '''
    draw_bg(screen)
    # (360, 785), (220, 305),
    master_draw(screen, draw_scrappers,
                fit_rect=Rect((220, 305), (size[1] - 220, 545)))
    # draw_car(screen)


def draw_orig_picture(screen):
    '''
    Function drawing the whole picture with parameters from data.
    '''
    draw_bg(screen)
    draw_scrappers_orig(screen)
    draw_spots(screen, range(4, 7))
    draw_car(screen)


draw_brand_new_picture(screen)
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
