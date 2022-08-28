from engine_files.entity import *

class Explosion(MovableEntity):
    def __init__(self, pos, explode_size, game_map, duration, speed=0):
        pos = (pos[0], pos[1], explode_size, explode_size)
        super().__init__(pos, game_map, speed)
        self.explode_size = explode_size
        self.duration = duration

    def update(self, *args, **kwargs):
        self.duration = self.duration - 1
        if (self.duration <= 0):
            self.game_map.entity_lst.remove(self)

    def draw(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), self)
