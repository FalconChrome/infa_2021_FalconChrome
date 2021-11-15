from pygame import Color


def render_text(surface, text, text_coord, font, color=None, align='center'):
    if color is None:
        color = Color('gray')
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.midtop = text_coord
    elif align == 'left':
        text_rect.topleft = text_coord
    elif align == 'right':
        text_rect.topright = text_coord

    surface.blit(text_surface, text_rect)
    return text_rect
