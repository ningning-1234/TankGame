from explosion import *

from engine_files.entity import *
class Bullet(MovableEntity):
    def __init__(self, pos, game_map, speed, angle, explosion_size):
        super().__init__((pos[0] - 10, pos[1] - 5, 10, 10), game_map, speed)
        self.angle = angle
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/bullet.png'),(20, 10))

        self.x_shift = math.cos(math.radians(self.angle))*self.speed
        self.y_shift = math.sin(math.radians(self.angle))*self.speed
        self.explosion_size = explosion_size

        self.self_damage = False

    def bound_collide(self, bound):
        '''
        Explodes the bullet.
        Is called if a bound is colliding with a bullet.
        :param bound: The bound that the bullet is colliding with.
        :return: None
        '''
        self.explode()
        self.active = False

    def wall_collide(self, wall):
        '''
        Explodes the bullet.
        Is called if a wall is colliding with a bullet.
        :param wall: The wall that the bullet is colliding with.
        :return: None
        '''
        self.explode()
        self.active = False

    def block_collide(self, block):
        '''
        Explodes the bullet.
        Is called if a block is colliding with a bullet.
        :param block: The bound that the bullet is colliding with.
        :return: None
        '''
        self.explode()
        self.active = False

    def player_collide(self, player):
        '''
        Explodes the bullet.
        Is called if a player is colliding with a bullet.
        :param player: The bound that the bullet is colliding with.
        :return: None
        '''
        self.explode()
        self.active = False

    def explode(self):
        '''
        Creates an explosion object in the center of the bullet object.
        :return: None
        '''
        if(self.active == True):
            pos = self.explosion_size / 2
            explosion = Explosion((self.centerx - pos, self.centery - pos), self.explosion_size, self.game_map, 10)
            self.game_map.entity_lst.append(explosion)

    def update(self, *args, **kwargs):
        '''
        Updates the bullet position.
        :param args:
        :param kwargs:
        :return: None
        '''
        if(not self.active):
            self.game_map.bullet_lst.remove(self)
        self.move_x = self.x_shift
        self.move_y = self.y_shift
        super().update(args, kwargs)

    def draw(self, surface):
        '''
        Draws bullets on surface.
        Bullets will be rotated if shot at different angles.
        :param surface: The surface the bullet will be drawn on.
        :return: None
        '''
        if(not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Short_Bullet(Bullet):
    def __init__(self, pos, game_map, speed, angle, explosion_size, bullet_timer):
        super().__init__(pos, game_map, speed, angle, explosion_size)
        self.bullet_timer = bullet_timer
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/short_bullet.png'), (10, 10))

    def bullet_despawn(self):
        '''
        Explodes the bullet.
        Is called if the bullet timer hits 0.
        :return: None
        '''
        self.explode()
        self.active = False

    def update(self, *args, **kwargs):
        '''
        Updates the bullet timer.
        :param args:
        :param kwargs:
        :return: None
        '''
        self.bullet_timer = self.bullet_timer - 1
        if (self.bullet_timer <= 0):
            self.bullet_despawn()
        super().update(args, kwargs)

    def draw(self, surface):
        '''
        Draws short bullets on surface.
        Short bullets will be rotated if shot at different angles.
        :param surface: The surface the bullet will be drawn on.
        :return: None
        '''
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)
