from bullet import Bullet
from explosion import Explosion
from engine_files.wall import Block

class GameBlock(Block):
    def __init__(self, pos, game_map, block_type):
        super().__init__(pos, block_type)
        self.game_map = game_map

    def entity_collide(self, entity):
        return

class BreakableBlock(GameBlock):
    def __init__(self, pos, game_map, block_type, health):
        super().__init__(pos, game_map, block_type)
        self.health = health
        self.max_health = health

    def entity_collide(self, entity):
        if(issubclass(type(entity), Bullet)):
            print('bullet collide')
            self.block_destroy()
        if(issubclass(type(entity), Explosion)):
            print('explosion collide')
            self.block_destroy()
        return

    def block_destroy(self):
        self.game_map.block_lst.remove(self)