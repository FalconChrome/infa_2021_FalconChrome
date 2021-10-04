import pygame
from pygame.draw import rect, polygon, ellipse
from pygame.color import Color

pygame.init()

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PALEGRAY = (155, 178, 178, 255)

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
draw_moved(rect, screen, Color(80, 103, 101, 255), rect=((0, 570), (630, 320)))
draw_moved(ellipse, screen, Color('azure2'), rect=((-50, 740), (800, 300)))


def blit_transp(func, screen, color, rect, alpha=100):
    '''Blits with transparency a figure drawn with a func argument'''
    if type(rect) != pygame.Rect:
        rect = pygame.Rect(rect)
    w, h = rect.w, rect.h
    surface = pygame.Surface((1.5 * w, 1.5 * h))
    surface.set_colorkey(BLACK)
    surface.set_alpha(alpha)
    func(surface, color,  ((0, 0), rect.size))
    screen.blit(surface, (rect.x, rect.y))


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

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        # Helps to get the coords of figures. No need for program correct work.
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos(), end=',\n')
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.update()
pygame.quit()
