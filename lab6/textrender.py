from pygame import Color, Rect
from pygame.draw import rect as draw_rect


def render_text(surface, text, text_coord, font, color='gray', align='center'):
    """
    Render a text at given coordinates by a given font
    Optional arguments:
    color: color of font
    align: string — left, center or right
    """
    color = Color(color)
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


class Label:
    """
    Label for getting input from keyboard
    """
    def __init__(self, pos, font, text='', color='gray', interval=20,
                 border_color='gray', border_width=0):
        """
        Initializing label with rect position and text

        Takes arguments:
        rect: Rect-like object
        font: pygame.Font to render
        text: displayed text (default '')

        Optional parameters:
        color: name or Color object to set color of text
        interval: in pixels — height of interval between lines
        border_color: color of rectangle border around text
        border_width: width of border in pixels; if non-positive, no border
        """
        self.rect = Rect(pos, (0, 0))
        self.font = font
        self.text = text
        self.h = interval
        self.color = Color(color)
        self.border_color = Color(border_color)
        self.border_width = border_width
        print(self.rect)

    def render_borders(self, screen):
        if self.border_width > 0:
            draw_rect(screen, self.border_color, self.rect, self.border_width)

    def render(self, screen):
        """
        Rendering lines of containing text on screen
        return rect fitting text
        """
        max_width = 0
        pos_rect = self.rect
        for line in self.text:
            print("render:", pos_rect)
            pos_rect = render_text(screen, line, pos_rect.midtop,
                                   self.font, self.color)
            pos_rect.y += pos_rect.h + self.h
            if max_width < pos_rect.w:
                max_width = pos_rect.w
        self.rect.size = (max_width, pos_rect.y - self.rect.y)
        self.render_borders(screen)
        return self.rect


class InputLabel(Label):
    """
    Label for getting input from keyboard
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.printing = False
