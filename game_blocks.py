from bullet import Bullet
from explosion import *
from engine_files.wall import Block
from random import randint

class GameBlock(Block):
    def __init__(self, pos, game_map, block_type):
        self.game_map = game_map
        size = (50, 50)
        sprite_folder = '1-1_block'
        if (block_type == 1):
            size = (50, 50)
            sprite_folder = '1-1_block'
        if (block_type == 2):
            size = (100, 100)
            sprite_folder = '2-2_block'
        if (block_type == 3):
            size = (100, 50)
            sprite_folder = '2-1_block'
        if (block_type == 4):
            size = (100, 50)
            sprite_folder = '2-1_block'
        self.folder = './assets/blocks/' + sprite_folder
        random_sprite = randint(1, 2)
        img = get_transparent_surface(pygame.image.load(self.folder + '/block' + str(random_sprite) + '.png'), size)
        if (block_type == 4):
            size = (50, 100)
            img = pygame.transform.rotate(img, 90)
        super().__init__(pos, size, img)
        print(self)

    def entity_collide(self, entity):
        return

crack_overlays1x1 = [
    pygame.image.load('./assets/blocks/crack_overlay1-1/crack_overlay0.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-1/crack_overlay1.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-1/crack_overlay2.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-1/crack_overlay3.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-1/crack_overlay4.png')
]
crack_overlays2x1 = [
    pygame.image.load('./assets/blocks/crack_overlay2-1/crack_overlay0.png'),
    pygame.image.load('./assets/blocks/crack_overlay2-1/crack_overlay1.png'),
    pygame.image.load('./assets/blocks/crack_overlay2-1/crack_overlay2.png'),
    pygame.image.load('./assets/blocks/crack_overlay2-1/crack_overlay3.png'),
    pygame.image.load('./assets/blocks/crack_overlay2-1/crack_overlay4.png')
]
crack_overlays1x2 = [
    pygame.image.load('./assets/blocks/crack_overlay1-2/crack_overlay0.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-2/crack_overlay1.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-2/crack_overlay2.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-2/crack_overlay3.png'),
    pygame.image.load('./assets/blocks/crack_overlay1-2/crack_overlay4.png')
]
class BreakableBlock(GameBlock):
    def __init__(self, pos, game_map, block_type, health):
        super().__init__(pos, game_map, block_type)
        self.health = health
        self.max_health = health
        self.bullet_multiplier = 1
        self.explosion_multiplier = 1
        self.overlay = []
        if(block_type == 3):
            for i in crack_overlays2x1:
                self.overlay.append(get_transparent_surface(i, self.size))
        elif(block_type == 4):
            for i in crack_overlays1x2:
                self.overlay.append(get_transparent_surface(i, self.size))
        else:
            for i in crack_overlays1x1:
                self.overlay.append(get_transparent_surface(i, self.size))

    # def update(self, *args, **kwargs):
    #     if(self.health<self.max_health):
    #         self.health = self.health+0.1

    def entity_collide(self, entity):
        if(issubclass(type(entity), Bullet)):
            print('bullet collide',end=' ')
            self.health = self.health - entity.block_damage * self.bullet_multiplier
        if (issubclass(type(entity), Explosion)):
            print('explosion collide',end=' ')
            self.health = self.health - entity.block_damage * self.explosion_multiplier
        print(self.health)
        if(self.health <= 0):
            self.block_destroy()
        return

    def draw(self, surface):
        super().draw(surface)
        if(self.health/self.max_health<0.2):
            surface.blit(self.overlay[4], self)
        elif(self.health/self.max_health<0.4):
            surface.blit(self.overlay[3], self)
        elif (self.health / self.max_health < 0.6):
            surface.blit(self.overlay[2], self)
        elif (self.health / self.max_health < 0.8):
            surface.blit(self.overlay[1], self)
        elif (self.health / self.max_health <= 1):
            surface.blit(self.overlay[0], self)

    def block_destroy(self):
        self.game_map.block_lst.remove(self)
