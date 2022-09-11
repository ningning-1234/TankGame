from engine_files.entity import *
from explosion import *

MINE_SIZE = 20
FLASH_DELAY1 = 8
FLASH_START1 = 60
FLASH_DELAY2 = 2
FLASH_START2 = 30
class Mine(MovableEntity):
    def __init__(self, pos, game_map, player, explosion_size, duration):
        super().__init__((pos[0], pos[1], MINE_SIZE, MINE_SIZE), game_map, 0)
        self.player = player
        self.explosion_size = explosion_size
        self.duration = duration
        self.player_collide_timer = 60
        self.img = get_transparent_surface(pygame.image.load('assets/mine.png'), (MINE_SIZE, MINE_SIZE))
        self.inactive_img = get_transparent_surface(pygame.image.load('assets/mine_inactive.png'), (MINE_SIZE, MINE_SIZE))

    def explode(self):
        '''
        Creates an explosion object in the center of the mine object.
        :return: None
        '''
        pos = self.explosion_size / 2
        explosion = Explosion((self.centerx - pos, self.centery - pos), self.explosion_size, self.game_map, 10)
        self.game_map.entity_lst.append(explosion)
        self.active = False

    def player_collide(self, player):
        '''
        Is called if a player is colliding with a mine.
        Has a timer before a player can explode the mine.
        :param player: The player that the mine is colliding with.
        :return: None
        '''
        if (self.player_collide_timer <= 0):
            self.explode()

    def bullet_collide(self, bullet):
        '''
        Explodes the mine.
        Is called if a bullet is colliding with a mine.
        :param bullet: The bullet that the mine is colliding with.
        :return: None
        '''
        self.explode()
        bullet.active = False

    def update(self, *args, **kwargs):
        '''
        Updates mine duration and mine counter.
        :param args:
        :param kwargs:
        :return: None
        '''
        if (not self.active):
            self.game_map.entity_lst.remove(self)
            self.player.mine_counter = self.player.mine_counter - 1

        mine_index = self.collidelist(self.game_map.bullet_lst)
        if (mine_index != -1):
            self.bullet_collide(self.game_map.bullet_lst[mine_index])

        super().update(args, kwargs)
        self.player_collide_timer = self.player_collide_timer - 1
        self.duration = self.duration - 1
        if (self.duration <= 0):
            self.explode()

    def draw(self, surface):
        '''
        Draws mines on surface.
        Mines will flash when it's duration is near 0.
        :param surface: The surface the mine will be drawn on.
        :return: None
        '''
        if(not self.active):
            return
        # pygame.draw.rect(surface, (75, 75, 75), self)
        if (self.player_collide_timer <= 0):
            # flashing
            if (self.duration <= FLASH_START2):
               if((self.duration//FLASH_DELAY2)%2 == 0):
                   surface.blit(self.inactive_img, self)
               else:
                   surface.blit(self.img, self)
            elif (self.duration <= FLASH_START1):
               if((self.duration//FLASH_DELAY1)%2 == 0):
                   surface.blit(self.inactive_img, self)
               else:
                   surface.blit(self.img, self)
            else:
                surface.blit(self.img, self)
        else:
            surface.blit(self.inactive_img, self)

# todo
#  add delay and limit to setting mines
#  make mines explode after set duration
#  make mines explode if it touches a player
#  update the player's mine counter when mine explodes
#  optional add delay before mine becomes active (do not use self.active, use another variable)
#  add custom sprites for mines and explosions, have a seperate sprite for when mine becomes active
