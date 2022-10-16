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
                 border_size=0, border_color=(0,0,0),
                 onhover=None, onhover_args=[], onhover_kwargs={},
                 unhover=None, unhover_args=[], unhover_kwargs={},
                 ):
        super().__init__(pos)
        self.surface = pygame.Surface((self[2], self[3]))
        self.page = None
        self.zindex = 0  # higher zindex will be drawn on top of lower zindex
        # self.draw_type = draw_type

        self.hovered = False
        self.hover_function = False
        if (onhover is not None):
            self.hover_function = True
            self.onhover_func = onhover
            self.onhover_args = onhover_args
            self.onhover_kwargs = onhover_kwargs
        self.unhover_function = False
        if (unhover is not None):
            self.unhover_function = True
            self.unhover_func = unhover
            self.unhover_args = unhover_args
            self.unhover_kwargs = unhover_kwargs


        self.color = color
        self.img = img

        self.border_size = border_size
        self.border_color = border_color

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        mouse_coords = mouse_inputs['mouse_coords']
        if (self.collidepoint(mouse_coords)):
            new_hover = False
            if(not self.hovered):
                new_hover = True
            self.hovered = True
            if (self.hover_function):
                self.hover()
        else:
            if(self.hovered):
                self.hovered = False
                if(self.unhover_function):
                    self.unhover()

    def hover(self):
        self.onhover_func(*self.onhover_args,**self.onhover_kwargs)

    def unhover(self):
        self.unhover_func(*self.unhover_args, **self.unhover_kwargs)

    def draw(self, surface):
        draw = False
        if (self.color is not None):
            self.surface.fill(self.color)
            draw = True
        if (self.img is not None):
            self.surface.blit(self.img, (0, 0))
            draw = True
        if (self.border_size>0):
            pygame.draw.rect(self.surface,self.border_color, (0,0,self.width,self.height), self.border_size)
            draw=True
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
            new_hover = False
            if (not self.hovered):
                new_hover = True
            self.hovered = True
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
            if (self.hovered):
                self.hovered = False
                if (self.unhover_function):
                    self.unhover()
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
    def __init__(self, pos,drain_dir, bar_percent=1, **kwargs):
        super().__init__(pos, **kwargs)

        # right, down, left, up
        self.drain_dir = drain_dir
        self.bar_percent = max(min(bar_percent, 1), 0)
        self.max_width = self[2]
        self.max_height = self[3]

    def update_fill(self, new_percent):
        self.bar_percent = max(min(new_percent, 1), 0)
        # right, down, left, up
        if (self.drain_dir==0):
            self.fill_width = self.bar_width * self.fill_percent
        elif (self.drain_dir==1):
            self.fill_height = self.bar_height * self.fill_percent
        elif (self.drain_dir==2):
            self.fill_width = self.bar_width * self.fill_percent
        elif (self.drain_dir==3):
            self.fill_height = self.bar_height * self.fill_percent

    def draw(self, surface):
        draw = False
        if (self.color is not None):
            self.surface.fill(self.color)
            draw = True
        if (self.img is not None):
            self.surface.blit(self.img, (0, 0))
            draw = True
        if (self.border_size > 0):
            pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), self.border_size)
            draw = True
        if (not draw):
            return
        # right
        if (self.drain_dir==0):
            cropped = pygame.Surface((self.max_width * self.bar_percent, self.max_height))
            cropped.blit(self.surface, (self.max_width * (self.bar_percent-1), 0))
            blit_pos = [self.max_width * (1-self.bar_percent), 0]
        # down
        if (self.drain_dir==1):
            cropped = pygame.Surface((self.max_width, self.max_height * self.bar_percent))
            cropped.blit(self.surface, (0,  self.max_height * (self.bar_percent-1)))
            blit_pos = [0, self.max_height * (1-self.bar_percent)]
        # left
        if (self.drain_dir==2):
            cropped = pygame.Surface((self.max_width * self.bar_percent, self.max_height))
            cropped.blit(self.surface, (0, 0))
            blit_pos = [0, 0]
        # up
        if (self.drain_dir==3):
            cropped = pygame.Surface((self.max_width, self.max_height* self.bar_percent))
            cropped.blit(self.surface, (0, 0))
            blit_pos = [0, 0]
        if (draw):
            surface.blit(cropped, blit_pos)