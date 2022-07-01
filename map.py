import pygame

class Map(pygame.Rect):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (50,50,50)
        self.bounds = (self[0], self[1], self[0] + self[2], self[1]+self[3])
        self.game_timer = 0

    def get_time(self):
        return self.game_timer

    def update(self):
        self.game_timer = self.game_timer+1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)