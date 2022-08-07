import math

from entity import *
class Bullet(MovableEntity):
    def __init__(self, pos, map, speed, angle):
        super().__init__((pos[0] - 10, pos[1] - 5, 20, 20), map, speed)
        self.angle = angle
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/bullet.png'),(20,10))

        self.x_shift = math.cos(math.radians(self.angle))*self.speed
        self.y_shift = math.sin(math.radians(self.angle))*self.speed
        # self.ignore_map_bounds = True
        # print(self.x_shift, self.y_shift)

    def bound_collide(self, bound):
        self.active = False

    def wall_collide(self, wall):
        self.active = False

    def update(self, *args, **kwargs):
        if(not self.active):
            self.game_map.bullet_lst.remove(self)
        self.move_x = self.x_shift
        self.move_y = self.y_shift
        super().update(args, kwargs)
        # print(self)

    def draw(self, surface):
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)
