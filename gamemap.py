import pygame.image

from engine_files.pages import *
from tank import Player
from game_blocks import *

class Game(Page):
    def __init__(self,page_manager, p1_weapon='Streamlined', p2_weapon='Streamlined'):
        super().__init__('game', page_manager, True)

        game_map = GameMap((50, 50, 500, 500))
        p1_bar = PagePercentBar((0,0,300,50), 0, 1, color=(50,50,255))
        self.add_component(p1_bar)

        player1 = Player(1, (0, 0, 50, 50), (100, 275, 50, 50), p1_weapon, game_map,p1_bar,
                         {pygame.K_d: 'BODY RIGHT',
                          pygame.K_s: 'BODY DOWN',
                          pygame.K_a: 'BODY LEFT',
                          pygame.K_w: 'BODY UP',
                          pygame.K_v: 'SHOOT',
                          pygame.K_z: 'MINE'
                          }
                         )
        game_map.player1 = player1

        p2_bar = PagePercentBar((300, 0, 300, 50), 2, 1, color=(255, 50, 50))
        self.add_component(p2_bar)
        player2 = Player(2, (450, 275, 50, 50), (320, 275, 50, 50), p2_weapon, game_map, p2_bar,
                         {pygame.K_RIGHT: 'BODY RIGHT',
                          pygame.K_DOWN: 'BODY DOWN',
                          pygame.K_LEFT: 'BODY LEFT',
                          pygame.K_UP: 'BODY UP',
                          pygame.K_n: 'SHOOT',
                          pygame.K_m: 'MINE'
                          }
                         )
        game_map.player2 = player2

        # block1 = GameBlock((50, 50), 1)
        # game_map.block_lst.append(block1)
        # block2 = GameBlock((100, 0), 2)
        # game_map.block_lst.append(block2)
        # block3 = GameBlock((50, 150), 3)
        # game_map.block_lst.append(block3)
        block4 = BreakableBlock((50, 250), game_map, 2, 50)
        game_map.block_lst.append(block4)

        self.add_component(game_map)
        def selection_return(**kwargs):
            self.page_manager.set_current_page(self.page_manager.page_archive['selection'])
            print(self.page_manager.page_archive)

        test_btn = PageButton((0,50,50,50),
                              onclick=selection_return,
                              # onrel=print,onrel_args=['release'],
                              # onhover=print,onhover_args=['hover'],
                              color=(200,100,100))
        self.add_component(test_btn)

        test_text = PageText((100,20,30,30), 'test', (50,50,50))
        # self.add_component(test_text)
        # self.percent = 0
        # self.test_bar = PagePercentBar((0,0,300,50), 3, self.percent, color=(200,200,0), img=pygame.image.load('assets/test_bar.png'))
        # self.add_component(self.test_bar)

        # block1.wall_lst.remove(block1.wall_lst[0])
    def update(self, *args, **kwargs):
        super().update(*args,**kwargs)
        # self.percent = self.percent + 0.01
        # if(self.percent>1):
        #     self.percent=0
        # self.test_bar.update_fill(self.percent)

class GameMap(PageComponent):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (50,50,50)
        self.bounds = (0, 0, self[2], self[3])
        # self.bounds = (self[0], self[1], self[0] + self[2], self[1]+self[3])
        self.game_timer = 0

        self.player1 = None
        self.player2 = None
        self.bullet_lst = []
        self.block_lst = []
        self.entity_lst = []

        self.surface = pygame.Surface((self[2], self[3]))

    def get_time(self):
        '''
        returns the game time.
        :return: self.game_timer
        '''
        return self.game_timer

    def update(self, *args, **kwargs):
        '''
        Updates all players, bullets and entities.
        :param args:
        :param kwargs:
        :return: None
        '''
        self.player1.update(kb_inputs=kwargs['kb_inputs'], controller_inputs=kwargs['controller_inputs1'])
        if(self.player2 is not None):
            self.player2.update(kb_inputs=kwargs['kb_inputs'], controller_inputs=kwargs['controller_inputs2'])

        for bullet in self.bullet_lst:
            bullet.update()
        for entity in self.entity_lst:
            entity.update()

        self.game_timer = self.game_timer+1

    def draw(self, surface, *args, **kwargs):
        '''
        Updates blocks, bullets, entities and players.
        :param surface: surface: The surface blocks, bullets, entities and players will be drawn on.
        :param args:
        :param kwargs:
        :return: None
        '''
        # draw map
        # pygame.draw.rect(self.surface, self.color, self)
        self.surface.fill(self.color)

        # draw blocks
        for block in self.block_lst:
            block.draw(self.surface)

        # draw bullets
        for bullet in self.bullet_lst:
            bullet.draw(self.surface)

        for entity in self.entity_lst:
            entity.draw(self.surface)

        # draw players
        self.player1.draw(self.surface)
        if (self.player2 is not None):
            self.player2.draw(self.surface)

        surface.blit(self.surface, self)
