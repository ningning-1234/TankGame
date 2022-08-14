import math
from explosion import *

from entity import *
class Bullet(MovableEntity):
    def __init__(self, pos, game_map, speed, angle):
        super().__init__((pos[0] - 10, pos[1] - 5, 10, 10), game_map, speed)
        self.angle = angle
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/bullet.png'),(20,10))

        self.x_shift = math.cos(math.radians(self.angle))*self.speed
        self.y_shift = math.sin(math.radians(self.angle))*self.speed
        # self.ignore_map_bounds = True
        # print(self.x_shift, self.y_shift)

    def bound_collide(self, bound):
        self.explode()
        self.active = False

    def wall_collide(self, wall):
        self.explode()
        self.active = False

    def block_collide(self, block):
        self.explode()
        self.active = False

    def explode(self):
        if(self.active == True):
            explosion = Explosion((self[0], self[1]), 25, self.game_map, 10)
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
    def __init__(self, pos, game_map, speed, angle):
        super().__init__(pos, game_map, speed, angle)
        self.bullet_timer = 20

    def bullet_despawn(self):
        self.active = False
        self.explode()

    def update(self, *args, **kwargs):
        self.bullet_timer = self.bullet_timer - 1
        if (self.bullet_timer <= 0):
            self.bullet_despawn()
        super().update(args, kwargs)
