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
        self.explode()
        self.active = False

    def wall_collide(self, wall):
        self.explode()
        self.active = False

    def block_collide(self, block):
        self.explode()
        self.active = False

    def player_collide(self, player):
        self.explode()
        self.active = False

    def explode(self):
        if(self.active == True):
            pos = self.explosion_size / 2
            explosion = Explosion((self.centerx - pos, self.centery - pos), self.explosion_size, self.game_map, 10)
            self.game_map.entity_lst.append(explosion)

    def update(self, *args, **kwargs):
        if(not self.active):
            self.game_map.bullet_lst.remove(self)
        self.move_x = self.x_shift
        self.move_y = self.y_shift
        super().update(args, kwargs)

    def draw(self, surface):
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
        self.explode()
        self.active = False

    def update(self, *args, **kwargs):
        self.bullet_timer = self.bullet_timer - 1
        if (self.bullet_timer <= 0):
            self.bullet_despawn()
        super().update(args, kwargs)

    def draw(self, surface):
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)
