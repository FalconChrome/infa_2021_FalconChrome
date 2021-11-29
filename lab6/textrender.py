from pygame import Color, Rect
from pygame.draw import rect as draw_rect


class Label:
    """
    Label class for showing text on screen
    """
    def __init__(self, pos, font, *text, color='gray', interval=20,
                 align='center', border_color='gray', border_width=0):
        """
        Initializing label with given position, font and text.
        By default align is center so coordinates are considered as midtop.

        Required arguments:
        pos: tuple of two floats; relative position of text depends on align
        font: Font object
        text: text to be showed (list parameter)

        Optional parameters:
        align: string — left, center or right
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
        self.align = align
        self.border_color = Color(border_color)
        self.border_width = border_width

    def set_text(self, *text):
        """
        Setter for text
        """
        self.text = text

    def render(self, surface):
        """
        Rendering lines of containing text on surface
        return rect fitting text
        """
        pos_rect = self.rect
        for line in self.text:
            print("render:", pos_rect)
            pos_rect = self.render_text(surface, line, pos_rect)
            pos_rect.y += pos_rect.h + self.h
            if self.rect.w < pos_rect.w:
                self.rect.w = pos_rect.w
                self.rect.x = pos_rect.x
        self.rect.h = pos_rect.y - self.rect.y
        self.render_borders(surface)
        return self.rect

    def render_text(self, surface, text, pos_rect):
        """
        Render a text at given position
        Arguments:
        surface: Surface on which label is rendered
        text: text
        pos_rect: Rect relatively which render text
        """
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()

        if self.align == 'center':
            text_rect.midtop = pos_rect.midtop
        elif self.align == 'left':
            text_rect.topleft = pos_rect.topleft
        elif self.align == 'right':
            text_rect.topright = pos_rect.topright

        surface.blit(text_surface, text_rect)
        return text_rect

    def render_borders(self, surface):
        """
        Render borders of label if borders set
        """
        if self.border_width > 0:
            draw_rect(surface, self.border_color, self.rect, self.border_width)


class InputLabel(Label):
    """
    Label for getting input from keyboard
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.printing = False
