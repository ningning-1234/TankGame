import pygame

class PageManager:
    def __init__(self, bg_color):
        self.bg_color = bg_color
        self.current_page=None
        self.page_archive = {}

    def set_current_page(self,page):
        if(self.current_page is not None):
            if(self.current_page.archive):
                self.archive_page(self.current_page)
        self.current_page = page
        page.page_manager = self

    def archive_page(self, page):
        self.page_archive[page.name] = page

    def update(self, *args, **kwargs):
        if (self.current_page is not None):
            self.current_page.update( *args, **kwargs)

    def draw(self, window):
        window.fill(self.bg_color)
        if (self.current_page is not None):
            self.current_page.draw(window)

class Page:
    def __init__(self, name, archive):
        self.name = name
        self.page_manager = None
        self.archive = archive
        self.components = []

    def add_component(self, component):
        self.components.append(component)
        component.page = self

    def update(self, *args, **kwargs):
        for component in self.components:
            component.update(*args, **kwargs)

    def draw(self, surface):
        for component in self.components:
            component.draw(surface)

    # converts windows coordinates into component coordinates
    def get_component_coords(self,component, coords):
        new_x = coords[0] - component[0]
        new_y = coords[1] - component[1]
        return (new_x,new_y)

class PageComponent(pygame.Rect):
    def __init__(self, pos, draw_type='fill', color=(100,100,100), img=None):
        super().__init__(pos)
        self.surface = pygame.Surface((self[2], self[3]))
        self.page = None
        self.zindex = 0 #higher zindex will be drawn on top of lower zindex
        self.draw_type = draw_type
        if(draw_type=='fill'):
            self.color = color
        if(draw_type=='img'):
            self.img = img

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface):
        if(self.draw_type=='fill'):
            self.surface.fill(self.color)
        if(self.draw_type=='img'):
            self.surface.blit(self.image,(0,0))

        surface.blit(self.surface, self)

class PageButton(PageComponent):
    def __init__(self, pos,
                 onclick=None, onclick_args=[], onclick_kwargs={},
                 onrel=None, onrel_args=[], onrel_kwargs={},
                 onhover=None, onhover_args=[],onhover_kwargs={},
                 **kwargs):
        super().__init__(pos,**kwargs)
        self.click_function = False
        self.release_function = False
        self.hover_function = False
        if(onclick is not None):
            self.click_function = True
            self.onclick_func = onclick
            self.onclick_args = onclick_args
            self.onclick_kwargs = onclick_kwargs
        if(onrel is not None):
            self.release_function = True
            self.onrel_func = onrel
            self.onrel_args = onrel_args
            self.onrel_kwargs = onrel_kwargs
        if(onhover is not None):
            self.hover_function = True
            self.onhover_func = onhover
            self.onhover_args = onhover_args
            self.onhover_kwargs = onhover_kwargs
        self.held = False

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        # translate into component coordinates
        # mouse_coords = self.page.get_component_coords(self, mouse_inputs['mouse_coords'])
        mouse_coords = mouse_inputs['mouse_coords']
        if(self.collidepoint(mouse_coords)):
            btn_num = 0
            for btn in mouse_inputs['mouse_btn']:
                if(btn):
                    self.held = True
                    if (self.click_function):
                        self.onclick(btn_num)
                    break
                btn_num = btn_num +1

            if(self.hover_function):
                self.hover()

    def onclick(self, btn_number):

        self.onclick_func(*self.onclick_args, **self.onclick_kwargs)

    def onrelease(self, btn_number):
        self.held = False
        self.onrel_func(*self.onrel_args, **self.onrel_kwargs)

    def hover(self):
        self.onhover_func(*self.onhover_args, **self.onhover_kwargs)



