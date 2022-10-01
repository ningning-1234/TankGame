import pygame

from engine_files.pages import *
from gamemap import Game
from engine_files.utils import get_transparent_surface
from engine_files.controller_mappings import *

weapons_list = {
    'Streamlined' : 'streamlined.png',
    'Spreader' : 'spreader.png',
    'Scatter' : 'scatter.png',
    'Ranger' : 'ranger.png',
    'CloseQuarters' : 'streamlined.png',
    'Charge' : 'streamlined.png',
    'GGAngles' : 'streamlined.png',
    'GGWider' : 'streamlined.png',
    'GGPulse' : 'streamlined.png',
    'GGSpiral' : 'streamlined.png'
}

class TitlePage(Page):
    def __init__(self, page_manager):
        super().__init__('title', page_manager, False, bg_img=pygame.image.load('assets/title_screen.png'))
        # start_btn = PageButton((0, 0, 600, 600),
        #                        onclick=self.start_selection
        #                        )
        # self.add_component(start_btn)
        # title_screen = get_transparent_surface(pygame.image.load('assets/title_screen.png'), (600, 600))
        # self.bg_img = title_screen

    def start_selection(self, **kwargs):
        self.page_manager.set_current_page(SelectionPage(self.page_manager))

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        kb_inputs = kwargs['kb_inputs']
        events = kwargs['events']
        if(True in mouse_inputs['mouse_btn']):
            self.start_selection()
            return
        if (True in kb_inputs):
            self.start_selection()
            return
        for event in events:
            if(event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION):
                self.start_selection()
                return

class SelectionPage(Page):
    def __init__(self, page_manager):
        super().__init__('selection', page_manager, False, bg_img=pygame.image.load('assets/selection_screen.png'))

        self.selected_weps = ['Streamlined', 'Streamlined']
        self.selected_btns = [None, None]
        self.hover_btn_id = [0,0]

        def start_onhover(btn):
            btn.color = (255, 0, 0)
        def start_unhover(btn):
            btn.color = (30, 80, 30)

        def temp_onhover(btn):
            btn.color = (100, 100, 100)

        def temp_unhover(btn):
            if (btn not in self.selected_btns):
                btn.color = (70, 70, 70)

        self.white_color = (200, 200, 200)
        player_txt_offset = [75, 75]

        self.btn_lst=[[],[]]

        # player 1
        self.add_component(PageText((player_txt_offset[0],player_txt_offset[1],80,40),
                                    'Player 1', self.white_color))
        p1_left = 80
        wep_v_offset = 40
        n = 0
        for wep in weapons_list:
            temp_btn = PageButton((p1_left - 5, player_txt_offset[1]+wep_v_offset + 5, 70, 30),
                                  color=(70, 70, 70), border_color=self.white_color)

            temp_btn.click_function = True
            temp_btn.onclick_func = self.weapon_select_button
            temp_btn.onclick_args = [1, wep, temp_btn]
            temp_btn.onclick_kwargs = {}

            temp_btn.hover_function = True
            temp_btn.onhover_func = temp_onhover
            temp_btn.onhover_args = [temp_btn]
            temp_btn.onhover_kwargs = {}

            temp_btn.unhover_function = True
            temp_btn.unhover_func = temp_unhover
            temp_btn.unhover_args = [temp_btn]
            temp_btn.unhover_kwargs = {}

            temp_btn.player_btn_id = n

            if(wep==self.selected_weps[0]):
                self.selected_btns[0] = temp_btn
                self.hover_btn_id[0] = n
                temp_btn.color = (100, 100, 100)
                temp_btn.border_size = 1

            self.add_component(temp_btn)
            self.btn_lst[0].append(temp_btn)
            temp_img = get_transparent_surface(pygame.image.load('assets/player1/'+weapons_list[wep]),(60,20))
            self.add_component(PageComponent((p1_left,player_txt_offset[1]+wep_v_offset+10, 60,20),
                                             img=temp_img))
            self.add_component(PageText((p1_left + 80, player_txt_offset[1]+wep_v_offset+10, 80, 40),
                                        wep, self.white_color))
            wep_v_offset = wep_v_offset + 40
            n = n+1

        # player 2
        self.add_component(PageText((page_manager.window_size[0] - player_txt_offset[0]-64, player_txt_offset[1], 80, 40),
                                    'Player 2', self.white_color))
        p2_left = page_manager.window_size[0] - 259
        wep_v_offset = 40
        n=0
        for wep in weapons_list:
            temp_btn = PageButton((p2_left + 115, player_txt_offset[1] + wep_v_offset + 5, 70, 30),
                                  color=(70, 70, 70), border_color=self.white_color)
            temp_btn.click_function = True
            temp_btn.onclick_func = self.weapon_select_button
            temp_btn.onclick_args = [2, wep, temp_btn]
            temp_btn.onclick_kwargs = {}

            temp_btn.hover_function = True
            temp_btn.onhover_func = temp_onhover
            temp_btn.onhover_args = [temp_btn]
            temp_btn.onhover_kwargs = {}

            temp_btn.unhover_function = True
            temp_btn.unhover_func = temp_unhover
            temp_btn.unhover_args = [temp_btn]
            temp_btn.unhover_kwargs = {}

            temp_btn.player_btn_id = n

            if (wep == self.selected_weps[1]):
                self.selected_btns[1] = temp_btn
                temp_btn.border_size = 1

            self.add_component(temp_btn)
            self.btn_lst[1].append(temp_btn)
            temp_img = get_transparent_surface(pygame.image.load('assets/player2/'+weapons_list[wep]),(60,20))
            self.add_component(PageComponent((p2_left + 120, player_txt_offset[1]+wep_v_offset+10, 60, 20),
                                             img=temp_img))
            self.add_component(PageText((p2_left - 10, player_txt_offset[1]+wep_v_offset+10, 80, 40),
                                        wep, self.white_color))
            wep_v_offset = wep_v_offset + 40
            n=n+1

         # start button
        start_btn = PageButton((page_manager.window_size[0] / 2 - 40, page_manager.window_size[1] * 0.85, 80, 40),
                                   color=(30, 80, 30),
                                   onclick=self.start_game
                                )
        start_btn.zindex = 2
        start_btn.hover_function = True
        start_btn.onhover_func = start_onhover
        start_btn.onhover_args = [start_btn]
        start_btn.onhover_kwargs = {}

        start_btn.unhover_function = True
        start_btn.unhover_func = start_unhover
        start_btn.unhover_args = [start_btn]
        start_btn.unhover_kwargs = {}

        self.add_component(start_btn)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        controller1 = kwargs['controller_inputs1']
        controller2 = kwargs['controller_inputs2']
        events = kwargs['events']
        for event in events:
            print(event)
            if(event.type == pygame.JOYBUTTONDOWN):
                if(event.joy==0):
                    if(event.button==CON_BUTTONS['DPAD_DOWN']):
                        self.btn_lst[0][self.hover_btn_id[0]].unhover()
                        self.hover_btn_id[0] = (self.hover_btn_id[0] + 1) % len(self.btn_lst[0])
                        self.btn_lst[0][self.hover_btn_id[0]].hover()
                    if (event.button==CON_BUTTONS['DPAD_UP']):
                        self.btn_lst[0][self.hover_btn_id[0]].unhover()
                        self.hover_btn_id[0] = (self.hover_btn_id[0] - 1) % len(self.btn_lst[0])
                        self.btn_lst[0][self.hover_btn_id[0]].hover()
            if(event.type == pygame.KEYDOWN):
                if(event.key==pygame.K_s):
                    self.btn_lst[0][self.hover_btn_id[0]].unhover()
                    self.hover_btn_id[0] = (self.hover_btn_id[0] + 1) % len(self.btn_lst[0])
                    self.btn_lst[0][self.hover_btn_id[0]].hover()
        # todo:
        #  let the hover selection work for all keyboard inputs
        #  let arrow keys work for player 2
        #  put the repeated code in a function

    #when a weapon select button is pressed
    def weapon_select_button(self, player, weapon, button, **kwargs):
        self.selected_weps[player-1] = weapon
        self.selected_btns[player-1].border_size = 0
        self.selected_btns[player-1].color = (70, 70, 70)
        self.selected_btns[player-1] = button
        self.hover_btn_id[player-1] = button.player_btn_id
        button.color = (100, 100, 100)
        button.border_size = 1
        print('Player1 weapon set to ' + weapon)
        print(self.hover_btn_id)

    def start_game(self, **kwargs):
        self.page_manager.set_current_page(Game(self.page_manager, self.selected_weps[0], self.selected_weps[1]))
