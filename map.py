import pygame

class Map(pygame.Rect):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (50,50,50)
        self.bounds = (self[0], self[1], self[0] + self[2], self[1]+self[3])
        self.game_timer = 0

        self.player1 = None
        self.player2 = None
        self.bullet_lst = []

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
        pygame.draw.rect(surface, self.color, self)

        # draw bullets
        for bullet in self.bullet_lst:
            bullet.draw(surface)

        # draw players
        self.player1.draw(surface)
        if (self.player2 is not None):
            self.player2.draw(surface)