from engine_files.entity import *

MINE_SIZE = 10
class Mine(MovableEntity):
    def __init__(self, pos, game_map, player, explosion_size, duration):
        super().__init__((pos[0], pos[1], MINE_SIZE, MINE_SIZE), game_map, 0)
        self.player = player
        self.explosion_size = explosion_size
        self.duration = duration

    def update(self, *args, **kwargs):
        super().update(args, kwargs)

    def draw(self, surface):
        if(not self.active):
            return
        pygame.draw.rect(surface, (50, 50, 255), self)


# todo
#  add delay and limit to setting mines
#  make mines explode after set duration
#  make mines explode if it touches a player
#  update the player's mine counter when mine explodes
#  optional add delay before mine becomes active (do not use self.active, use another variable)
#  add custom sprites for mines and explosions, have a seperate sprite for when mine becomes active