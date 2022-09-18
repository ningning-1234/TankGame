import pygame
from engine_files.utils import get_transparent_surface


class PageManager:
    def __init__(self, bg_color, window_size):
        '''
        Controls the flow of all the pages.
        Responsible for drawing and updating the current page
        :param bg_color: Color of the background when drawing a new frame
        '''
        self.bg_color = bg_color
        self.current_page = None
        self.page_archive = {}
        self.window_size = window_size

    def set_current_page(self, page):
        if (self.current_page is not None):
            if (self.current_page.archive):
                self.archive_page(self.current_page)
        self.current_page = page
        page.page_manager = self

    def archive_page(self, page):
        self.page_archive[page.name] = page

    def update(self, *args, **kwargs):
        if (self.current_page is not None):
            self.current_page.update(*args, **kwargs)

    def draw(self, window):
        window.fill(self.bg_color)
        if (self.current_page is not None):
            self.current_page.draw(window)


class Page:
    def __init__(self, name, page_manager, archive, bg_color=None, bg_img=None):
        '''
        Object to do display a page onto the screen. Contains page components
        :param name: Name of the page
        :param archive: Whether the page should be archived. Achived pages can be retrieved later.
        '''
        self.name = name
        self.page_manager = None
        self.archive = archive
        self.components = []

        self.page_manager = page_manager
        self.bg_color = bg_color
        self.bg_img = bg_img
    def add_component(self, component):
        self.components.append(component)
        component.page = self

    def update(self, *args, **kwargs):
        for component in self.components:
            component.update(*args, **kwargs)

    def draw(self, surface):
        if (self.bg_color is not None):
            surface.fill(self.bg_color)
        if (self.bg_img is not None):
            surface.blit(self.bg_img, (0, 0))

        for component in self.components:
            component.draw(surface)

    def get_component_coords(self, component, coords):
        '''
        Converts windows coordinates into the coordinates on the component.
        Useful for checking if the mouse is on a component
        :param component: Component to get coordinates from
        :param coords: Coordinates relative to the window
        :return: Coordinates on the component based on the given coordinates
        '''
        new_x = coords[0] - component[0]
        new_y = coords[1] - component[1]
        return (new_x, new_y)


class PageComponent(pygame.Rect):
    def __init__(self, pos,
                 color=None, img=None,
                 onhover=None, onhover_args=[], onhover_kwargs={}
                 ):
        super().__init__(pos)
        self.surface = pygame.Surface((self[2], self[3]))
        self.page = None
        self.zindex = 0  # higher zindex will be drawn on top of lower zindex
        # self.draw_type = draw_type

        self.hover_function = False
        if (onhover is not None):
            self.hover_function = True
            self.onhover_func = onhover
            self.onhover_args = onhover_args
            self.onhover_kwargs = onhover_kwargs

        self.color = color
        self.img = img

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        mouse_coords = mouse_inputs['mouse_coords']
        if (self.collidepoint(mouse_coords)):
            if (self.hover_function):
                self.hover()

    def hover(self):
        self.onhover_func(*self.onhover_args, **self.onhover_kwargs)

    def draw(self, surface):
        draw = False
        if (self.color is not None):
            self.surface.fill(self.color)
            draw = True
        if (self.img is not None):
            self.surface.blit(self.img, (0, 0))
            draw = True
        if (draw):
            surface.blit(self.surface, self)


class PageText(PageComponent):
    def __init__(self, pos, text, font_color, antialias=True, **kwargs):
        super().__init__(pos, **kwargs)
        self.text = text
        self.font = pygame.font.SysFont(None, 24)

        self.antialias = antialias
        self.font_color = font_color

        self.text_img = self.font.render(self.text, self.antialias, self.font_color, self.color)

    def update_text(self, new_text):
        self.text = new_text
        self.text_img = self.font.render(self.text, self.antialias, self.font_color, self.color)

    def draw(self, surface):
        surface.blit(self.text_img, self)


class PageButton(PageComponent):
    def __init__(self, pos,
                 click_delay=0,
                 onclick=None, onclick_args=[], onclick_kwargs={},
                 onrel=None, onrel_args=[], onrel_kwargs={},
                 onhold=None, onhold_args=[], onhold_kwargs={},
                 **kwargs):
        super().__init__(pos, **kwargs)
        self.click_function = False
        self.release_function = False
        self.hold_function = False
        if (onclick is not None):
            self.click_function = True
            self.onclick_func = onclick
            self.onclick_args = onclick_args
            self.onclick_kwargs = onclick_kwargs
        if (onrel is not None):
            self.release_function = True
            self.onrel_func = onrel
            self.onrel_args = onrel_args
            self.onrel_kwargs = onrel_kwargs
        if (onhold is not None):
            self.hold_function = True
            self.onhold_func = onhold
            self.onhold_args = onhold_args
            self.onhold_kwargs = onhold_kwargs

        self.prev_clicked = []
        self.clicked = False
        self.click_delay = click_delay

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        # translate into component coordinates
        # mouse_coords = self.page.get_component_coords(self, mouse_inputs['mouse_coords'])
        mouse_coords = mouse_inputs['mouse_coords']

        clicked_btns = []
        released_btns = []

        if (self.collidepoint(mouse_coords)):
            btn_num = 0
            # get clicks
            for btn in mouse_inputs['mouse_btn']:
                if (btn):
                    clicked_btns.append(btn_num)
                btn_num += 1
            if (self.hover_function):
                self.hover()

            for btn in self.prev_clicked:
                if (btn not in clicked_btns):
                    released_btns.append(btn)
        else:
            released_btns = self.prev_clicked.copy()

        if (len(clicked_btns) > 0):
            if (self.click_function):
                self.onclick(clicked_btns)
        if (len(released_btns) > 0):
            if (self.release_function):
                self.onrelease(released_btns)

        self.prev_clicked = clicked_btns

    def onclick(self, btn_number):
        self.onclick_func(*self.onclick_args,btn_number=btn_number, **self.onclick_kwargs)

    def onrelease(self, btn_number):
        self.onrel_func(*self.onrel_args, btn_number=btn_number, **self.onrel_kwargs)

    def onhold(self, btn_number):
        self.onrel_func(*self.onrel_args,btn_number=btn_number, **self.onrel_kwargs)


class PagePercentBar(PageComponent):
    def __init__(self, pos, fill_percent=1,
                 fill_color=None, fill_img=None,
                 horizontal=True, default_dir=True, **kwargs):
        super().__init__(pos, **kwargs)

        self.fill_color = fill_color
        self.fill_img = fill_img
        self.fill_surface = pygame.Surface((self[2], self[3]))

        self.horizontal = horizontal
        self.default_dir = True
        self.fill_percent = max(min(fill_percent, 1), 0)
        self.fill_width = self[2]
        self.fill_height = self[3]
        if (self.horizontal):
            self.fill_width = self.fill_width * self.fill_percent
        else:
            self.fill_height = self.fill_height * self.fill_percent

    def update_fill(self, new_percent):
        self.fill_percent = max(min(new_percent, 1), 0)
        if (self.horizontal):
            self.fill_width = self.fill_width * self.fill_percent
        else:
            self.fill_height = self.fill_height * self.fill_percent

    def draw(self, surface):
        super.draw(surface)

        if (self.color is not None):
            self.surface.fill(self.color)
        if (self.img is not None):
            self.surface.blit(self.img, (0, 0))
        surface.blit(self.fill_surface, self)
