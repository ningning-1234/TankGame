from engine_files.animation import Animation
from engine_files.entity import *

explosion_imgs = []
for g in range(0, 15):
    explosion_imgs.append(pygame.image.load('./assets/explosion/explosion_' + str(g) + '.png'))

class Explosion(MovableEntity):
    def __init__(self, pos, damage, explode_size, game_map, duration, owner, speed=0):
        pos = (pos[0], pos[1], explode_size, explode_size)
        super().__init__(pos, game_map, speed)
        self.explode_size = explode_size
        self.duration = duration

        self.owner = owner
        # whether the bullet can hit its owner
        self.self_damage = True
        self.damage = damage
        self.block_damage = self.damage
        self.collide_entities = []
        img_lst = []
        # todo
        #  make imgs scale
        self.animation = Animation(explosion_imgs, 1, list(range(0, len(explosion_imgs))), default_frame=len(explosion_imgs)-1)
        #self.img = get_transparent_surface(pygame.image.load('./assets/explosion/explosion_0.png'), (self.explode_size, self.explode_size))

    def player_collide(self, player):
        if (not self.self_damage):
            if (player == self.owner):
                return
        if(player not in self.collide_entities):
            player.take_damage(self.damage, self)
            self.collide_entities.append(player)

    def block_collide(self, block):
        if (block not in self.collide_entities):
            block.entity_collide(self)
            self.collide_entities.append(block)

    def update(self, *args, **kwargs):
        '''
        Updates explosion timer.
        :param args:
        :param kwargs:
        :return: None
        '''
        self.duration = self.duration - 1
        if (self.duration <= 0):
            self.game_map.entity_lst.remove(self)
        super().update(args, kwargs)

    def draw(self, surface):
        '''
        Draws explosions on surface
        :param surface: The surface the explosion will be drawn on.
        :return: None
        '''
        pygame.draw.rect(surface, (100, 100, 100), self)
        new_img = pygame.transform.scale(self.animation.animate(), (self.explode_size, self.explode_size))
        surface.blit(new_img, self)

class Mine_Explosion(Explosion):
    def __init__(self, pos, damage, explode_size, game_map, duration, owner, speed=0):
        super().__init__(pos, damage, explode_size, game_map, duration, owner, speed)
        self.explode_size = explode_size
        self.duration = duration

        self.owner = owner
        # whether the bullet can hit its owner
        self.self_damage = True
        self.damage = 25
        self.block_damage = 1000
        self.collide_entities = []
