import pygame
from pygame.draw import rect, ellipse
from pygame.color import Color
from pygame.rect import Rect

pygame.init()

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PALEGRAY = (155, 178, 178, 255)

size = 630, 890
bndx, bndy = 0, 0  # boundaries of picture


def draw_moved(surface, func, *args, rect, **kwargs):
    '''Function for shift draw, helps make bounds'''
    func(surface, *args,
         ((rect[0][0] - bndx, rect[0][1] - bndy), rect[1]), **kwargs)


# screen size counted with bounds
screen = pygame.display.set_mode((size[0] - 2 * bndx, size[1] - 2 * bndy))

# initial bg filling
screen.fill(WHITE)
draw_moved(screen, rect, Color('azure3'), rect=((0, 0), (630, 565)))
draw_moved(screen, rect, Color(80, 103, 101, 255), rect=((0, 570), (630, 320)))
draw_moved(screen, ellipse, Color('azure2'), rect=((-50, 740), (800, 300)))


def blit_transp(screen, func, color, rect, alpha=100):
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


# Databases for coords of scrappers and spots
skyscrappers = [('lightsteelblue3', ((14, 22), (127, 568))),
                (PALEGRAY, ((162, 50), (135, 549))),
                ('honeydew2', ((473, 19), (144, 574))),
                ('gray', ((101, 133), (148, 544))),
                ('paleturquoise4', ((418, 162), (133, 525)))]
spots = [((-75, 57), (519, 149)),
         ((86, 427), (272, 101)),
         ((-76, 648), (161, 41)),
         ((182, -12), (589, 146)),
         ((45, 703), (171, 47)),
         ((131, 221), (602, 145)),
         ((50, 766), (166, 42))]


car = {'turquoise3':
       (((292, 740), (132, 28)),  # for blue recctangle parts
        ((246, 768), (264, 48))),
       'white':
       (((306, 748), (40, 20)),  # for white rectangle parts
        ((372, 748), (40, 20))),
       'black':
       (((292, 810), (28, 20)),  # for elliptic parts
        ((470, 810), (28, 20)),
        ((243, 803), (18, 4)))}

for i, (color, scrapper) in enumerate(skyscrappers):
    # print(scrapper)
    draw_moved(screen, blit_transp, ellipse, Color(PALEGRAY),
               rect=spots[i], alpha=140)
    draw_moved(screen, rect, Color(color), rect=scrapper)

for j in range(i, 7):
    draw_moved(screen, blit_transp, ellipse, Color(PALEGRAY),
               rect=spots[j], alpha=140)

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
