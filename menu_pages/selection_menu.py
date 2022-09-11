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

class SelectionPage(Page):
    def __init__(self,page_manager):
        super().__init__('selection', page_manager, False,bg_color=(100,100,100))
        start_btn = PageButton((page_manager.window_size[0]/2-40,page_manager.window_size[1]*0.75, 80,40),
                               color=(30,80,30),
                               onclick=self.start_game
                               )
        self.add_component(start_btn)

        player_txt_offset = [50,50]
        self.add_component(PageText((player_txt_offset[0],player_txt_offset[1],80,40),
                                    'Player 1', (0,0,0)))
        self.add_component(PageText((page_manager.window_size[0] - player_txt_offset[0]-80, player_txt_offset[1], 80, 40),
                                    'Player 2', (0, 0, 0)))
        p1_left = 50
        wep_v_offset = 40
        for wep in weapons_list:
            temp_img = get_transparent_surface(pygame.image.load('assets/player1/'+weapons_list[wep]),(60,20))
            self.add_component(PageComponent((p1_left,player_txt_offset[1]+wep_v_offset+10, 60,20),
                                             img=temp_img))
            self.add_component(PageText((p1_left + 80, player_txt_offset[1]+wep_v_offset+10, 80, 40),
                                        wep, (0, 0, 0)))
            wep_v_offset = wep_v_offset + 40

        p2_left = page_manager.window_size[0] - 50 - 80

    def start_game(self, **kwargs):
        self.page_manager.set_current_page(Game(self.page_manager))