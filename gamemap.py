import pygame
from pages import *
from tank import Player
from wall import Block

class Game(Page):
    def __init__(self):
        super().__init__("game", True)

        game_map = GameMap((50, 100, 500, 500))
        player1 = Player(1, (100, 275, 50, 50), (100, 275, 50, 50), [(100, 175, 255), (25, 100, 255)], game_map,
                         {pygame.K_d: 'BODY RIGHT',
                          pygame.K_s: 'BODY DOWN',
                          pygame.K_a: 'BODY LEFT',
                          pygame.K_w: 'BODY UP'}
                         )
        game_map.player1 = player1
        player2 = Player(2, (450, 275, 50, 50), (320, 275, 50, 50), [(255, 100, 100), (255, 25, 25)], game_map,
                         {pygame.K_RIGHT: 'BODY RIGHT',
                          pygame.K_DOWN: 'BODY DOWN',
                          pygame.K_LEFT: 'BODY LEFT',
                          pygame.K_UP: 'BODY UP'}
                         )
        game_map.player2 = player2

        # bullet = Bullet((250, 250), map, 5, 0)
        # map.bullet_lst.append(bullet)

        block1 = Block((50, 50), 1)
        game_map.block_lst.append(block1)
        block2 = Block((200, 0), 2)
        game_map.block_lst.append(block2)
        block3 = Block((50, 150), 3)
        game_map.block_lst.append(block3)
        block4 = Block((50, 250), 2)
        game_map.block_lst.append(block4)
        self.add_component(game_map)
        test_btn = PageButton((20,20,30,30),
                              onclick=print,onclick_args=['click'],
                              onrel=print,onrel_args=['release'],
                              draw_type='fill', color=(200,100,100))
        self.add_component(test_btn)

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

        self.surface = pygame.Surface((self[2], self[3]))

    def get_time(self):
        return self.game_timer

    def update(self, *args, **kwargs):
        self.player1.update(kb_inputs=kwargs['kb_inputs'], controller_inputs=kwargs['controller_inputs1'])
        if(self.player2 is not None):
            self.player2.update(kb_inputs=kwargs['kb_inputs'], controller_inputs=kwargs['controller_inputs2'])

        for bullet in self.bullet_lst:
            bullet.update()

        self.game_timer = self.game_timer+1

    def draw(self, surface, *args, **kwargs):
        # draw map
        # pygame.draw.rect(self.surface, self.color, self)
        self.surface.fill(self.color)

        # draw blocks
        for block in self.block_lst:
            block.draw(self.surface)

        # draw bullets
        for bullet in self.bullet_lst:
            bullet.draw(self.surface)

        # draw players
        self.player1.draw(self.surface)
        if (self.player2 is not None):
            self.player2.draw(self.surface)

        surface.blit(self.surface, self)
