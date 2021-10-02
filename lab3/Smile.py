import pygame
from pygame.draw import *
from pygame.color import Color

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

points = [(60, 139),
(164, 205),
(221, 206),
(327, 168),
(129, 328),
(259, 328),
(125, 219),
(262, 220),
(189, 251)]

lw = 16

r1 = 9 
r2 = 19
r3 = 26
R = 140


#rect(screen, (255, 0, 255), (100, 100, 200, 200))

#rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
#polygon(screen, (255, 255, 0), [(100,100), (200,50),
                              #  (300,100), (100100)])
#polygon(screen, (0, 0, 255), # [(100,100), (20050),
                              #  (300,100), (100100)], 5)
#circle(screen, (0, 255, 0), (200, 175), 50)
screen.fill(Color("grey"))

circle(screen, Color("yellow"), points[-1], R)

line(screen, (0, 0, 0), points[0], points[1], lw)
line(screen, (0, 0, 0), points[2], points[3], lw)
line(screen, (0, 0, 0), points[4], points[5], 2 * lw)

circle(screen, Color("red"), points[-3], r3)
circle(screen, Color("black"), points[-3], r1)
circle(screen, Color("red"), points[-2], r2)
circle(screen, Color("black"), points[-2], r1)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


pygame.quit()
