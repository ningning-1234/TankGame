from engine_files.entity import *
from engine_files.utils import *


class Reticle(MovableEntity):
    def __init__(self, pos, game_map, img_folder_path, player):
        super().__init__((pos[0], pos[1], 20, 20), game_map, 5)
        # self.color = self.normal_color

        self.default_img_path = img_folder_path + 'reticle.png'
        self.shoot_img_path = img_folder_path + 'reticle_shoot.png'
        self.default_img = get_transparent_surface(pygame.image.load(self.default_img_path), (self[2], self[3]))
        self.shoot_img = get_transparent_surface(pygame.image.load(self.shoot_img_path), (self[2], self[3]))
        self.img = self.default_img

        self.player = player
        self.tank_radius = 200

        self.ignore_walls = True

        self.x_pos = self.centerx
        self.y_pos = self.centery

    def update(self, *args, **kwargs):
        super().update(args, kwargs)
        self.x_pos = self.centerx
        self.y_pos = self.centery

    def move(self):
        # calculate distance from main body
        body = self.player.tank_body
        dist = get_hyp([body.centerx, body.centery], [(self.centerx + self.move_x), (self.centery + self.move_y)])
        # dist = math.sqrt((body.centerx-(self.centerx + self.move_x))**2+(body.centery-(self.centery + self.move_y))**2)
        if (dist > self.tank_radius):
            # print('exceeded')
            exceed_ratio = (dist - self.tank_radius) / dist
            exceed_x = body.centerx - self.centerx
            exceed_y = body.centery - self.centery
            self.move_x = exceed_ratio * exceed_x
            self.move_y = exceed_ratio * exceed_y
        super().move()

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self)
        surface.blit(self.img, self)