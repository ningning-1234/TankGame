from engine_files.pages import *
from gamemap import Game
from engine_files.utils import get_transparent_surface

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
        start_btn = PageButton((0, 0, 600, 600),
                               onclick=self.start_selection
                               )
        # self.add_component(start_btn)
        # title_screen = get_transparent_surface(pygame.image.load('assets/title_screen.png'), (600, 600))
        # self.bg_img = title_screen

    def start_selection(self, **kwargs):
        self.page_manager.set_current_page(SelectionPage(self.page_manager))

    def update(self, *args, **kwargs):
        mouse_inputs = kwargs['mouse_inputs']
        kb_inputs = kwargs['kb_inputs']
        controller_inputs1 = kwargs['controller_inputs1']
        controller_inputs2 = kwargs['controller_inputs2']
        if(True in mouse_inputs['mouse_btn']):
            self.start_selection()
            return
        if (True in kb_inputs):
            self.start_selection()
            return
        # if (True in controller_inputs1['mouse_btn']):
        #     self.start_selection()
        #     return
        # print(self.parse_con_buttons(kwargs['controller_inputs']))

class SelectionPage(Page):
    def __init__(self, page_manager):
        super().__init__('selection', page_manager, False,bg_color=(100,100,100))

        self.selected_weps = ['Streamlined', 'Streamlined']
        self.selected_btns = [None, None]

        def start_onhover(btn):
            btn.color = (255,0,0)
        def start_unhover(btn):
            btn.color=(30,80,30)

        # start button
        start_btn = PageButton((page_manager.window_size[0]/2-40,page_manager.window_size[1]*0.75, 80,40),
                               color=(30,80,30),
                               onclick=self.start_game
                               )
        start_btn.hover_function = True
        start_btn.onhover_func = start_onhover
        start_btn.onhover_args = [start_btn]
        start_btn.onhover_kwargs = {}

        start_btn.unhover_function = True
        start_btn.unhover_func = start_unhover
        start_btn.unhover_args = [start_btn]
        start_btn.unhover_kwargs = {}

        self.add_component(start_btn)

        # player title
        player_txt_offset = [50,50]
        self.add_component(PageText((player_txt_offset[0],player_txt_offset[1],80,40),
                                    'Player 1', (0,0,0)))
        self.add_component(PageText((page_manager.window_size[0] - player_txt_offset[0]-80, player_txt_offset[1], 80, 40),
                                    'Player 2', (0, 0, 0)))

        #todo
        # when hovering over a button, change its background to a darker shade of gray
        # when unhovered, change it back to its original color
        # when selected, the background should stay that gray
        # when deselected, it should change back to the original color

        p1_left = 50
        wep_v_offset = 40
        for wep in weapons_list:
            temp_btn = PageButton((p1_left - 5, player_txt_offset[1]+wep_v_offset + 5, 70, 30),
                                  color=(70, 70, 70), border_color=(255,255,0))
            temp_btn.click_function = True
            temp_btn.onclick_func = self.weapon_select_button
            temp_btn.onclick_args = [1, wep, temp_btn]
            temp_btn.onclick_kwargs = {}

            if(wep==self.selected_weps[0]):
                self.selected_btns[0] = temp_btn
                temp_btn.border_size = 2

            self.add_component(temp_btn)
            temp_img = get_transparent_surface(pygame.image.load('assets/player1/'+weapons_list[wep]),(60,20))
            self.add_component(PageComponent((p1_left,player_txt_offset[1]+wep_v_offset+10, 60,20),
                                             img=temp_img))
            self.add_component(PageText((p1_left + 80, player_txt_offset[1]+wep_v_offset+10, 80, 40),
                                        wep, (0, 0, 0)))
            wep_v_offset = wep_v_offset + 40

        p2_left = page_manager.window_size[0] - 50 - 160
        wep_v_offset = 40
        for wep in weapons_list:
            temp_btn = PageButton((p2_left + 115, player_txt_offset[1] + wep_v_offset + 5, 70, 30),
                                  color=(70, 70, 70), border_color=(255,255,0))
            temp_btn.click_function = True
            temp_btn.onclick_func = self.weapon_select_button
            temp_btn.onclick_args = [2, wep, temp_btn]
            temp_btn.onclick_kwargs = {}

            if (wep == self.selected_weps[1]):
                self.selected_btns[1] = temp_btn
                temp_btn.border_size = 2

            self.add_component(temp_btn)
            temp_img = get_transparent_surface(pygame.image.load('assets/player2/'+weapons_list[wep]),(60,20))
            self.add_component(PageComponent((p2_left + 120, player_txt_offset[1]+wep_v_offset+10, 60, 20),
                                             img=temp_img))
            self.add_component(PageText((p2_left - 10, player_txt_offset[1]+wep_v_offset+10, 80, 40),
                                        wep, (0, 0, 0)))
            wep_v_offset = wep_v_offset + 40

    def weapon_select_button(self, player, weapon, button, **kwargs):
        self.selected_weps[player-1] = weapon
        print(button)
        self.selected_btns[player-1].border_size = 0
        self.selected_btns[player-1] = button
        button.border_size = 2
        print('Player1 weapon set to ' + weapon)


    def start_game(self, **kwargs):
        self.page_manager.set_current_page(Game(self.page_manager, self.selected_weps[0], self.selected_weps[1]))
