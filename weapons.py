from random import randint
from bullet import Bullet
from utils import *
from animation import *
from reticle import *

# generic tank cannon
class TankCannon():
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        self.position = pos
        self.width = width
        self.height = height

        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0,1,2,3,2,1,0],1)
        self.default_img = self.fire_animation_imgs[0]

        self.img = self.default_img
        self.animation = None

        self.player = player

        self.body = player.tank_body
        self.reticle = Reticle((reticle_pos[0] + 80, reticle_pos[1] + 15), self.player.game_map, img_folder_path, self.player)
        self.player.reticle = self.reticle

        # position of the pivot on the image
        # self.image_pivot_pos = [0, 0]
        self.image_pivot_pos = [height/2, height/2]
        # self.image_pivot_pos = [height/2, height/2]

        self.angle = get_angle(self.position, [self.reticle.x_pos, self.reticle.y_pos])
        # self.angle = 0

        self.bullet_spawn_dist = 45
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle))*self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]

        self.shooting = False
        self.shoot_delay = 15
        self.last_shot = 0

    def shoot(self):
        # cooldown check
        if (self.shooting):
            self.cooldown_shoot()
            return

        # shoot bullet
        self.shoot_bullet()

        # set animation
        self.fire_animation.reset()
        self.animation = self.fire_animation

        # set shooting state
        self.shooting = True
        self.reticle.img = self.reticle.shoot_img
        self.last_shot = self.player.game_map.get_time()

    def cooldown_shoot(self):
        pass

    def shoot_bullet(self):
        offset = 0
        bullet = Bullet((self.bullet_spawn[0] + offset, self.bullet_spawn[1] + offset),
                        self.player.game_map, 5, self.angle)

        self.player.game_map.bullet_lst.append(bullet)


    def update(self, *args, **kwargs):
        self.position = self.body.center

        self.angle = get_angle(self.position, [self.reticle.x_pos, self.reticle.y_pos])
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] + math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
        # self.angle = (self.angle+1)%360

        if (self.shooting):
            if (self.player.game_map.get_time() >= self.last_shot + self.shoot_delay):
                self.shooting = False
                self.reticle.img = self.reticle.default_img

    def draw(self, surface):
        if(self.animation is not None):
            img = self.animation.animate()
            if(self.animation.complete == True):
                self.animation = None
        else:
            img = self.img
        # position rectangle for the image
        img_pos_rect = [self.position[0] - self.image_pivot_pos[0],
                        self.position[1] - self.image_pivot_pos[1],
                        self.width, self.height]

        # centered rotation of image
        rotated_img, rotated_rect = centered_rotate(img, img_pos_rect, -self.angle)

        # rotate image about a pivot
        pivot_rect = img_pivot_rotate(rotated_img, rotated_rect, self.position, -self.angle)
        # pivot_rect = img_pivot_rotate(rotated_img, rotated_rect, pivot_point, -self.angle)

        surface.blit(rotated_img, pivot_rect)

        # draw position
        # pygame.draw.rect(surface, [250, 150, 150], (self.position[0], self.position[1], 2, 2))

# class StreamLined(TankCannon):
#     def __init__(self, pos, width, height, img_folder_path, player):
#         super().__init__(pos, width, height, img_folder_path, player)
#         self.player.shoot_delay = 15
#         self.fire_animation_imgs = [
#             get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
#             get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
#             get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
#             get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
#         ]
#         self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
#         self.default_img = self.fire_animation_imgs[0]
#         self.img = self.default_img
#
#     def shoot(self):
#         offsetx = randint(-5, 5)
#         offsety = randint(-5, 5)
#         bullet = Bullet((self.bullet_spawn[0] + offsetx, self.bullet_spawn[1] + offsety),
#                         self.player.game_map, 5, self.angle)
#         self.player.game_map.bullet_lst.append(bullet)
#
#         self.fire_animation.reset()
#         self.animation = self.fire_animation

class Spreader(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, player):
        super().__init__(pos, width, height, img_folder_path, player)
        self.shoot_delay = 30
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'spreader.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'spreader_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'spreader_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'spreader_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        offsetx = randint(-5, 5)
        offsety = randint(-5, 5)
        bullet1 = Bullet((self.bullet_spawn[0] + offsetx, self.bullet_spawn[1] + offsety),
                        self.player.game_map, 5, self.angle)
        self.player.game_map.bullet_lst.append(bullet1)
        bullet2 = Bullet((self.bullet_spawn[0] + offsetx, self.bullet_spawn[1] + offsety),
                        self.player.game_map, 5, self.angle - 15)
        self.player.game_map.bullet_lst.append(bullet2)
        bullet3 = Bullet((self.bullet_spawn[0] + offsetx, self.bullet_spawn[1] + offsety),
                        self.player.game_map, 5, self.angle + 15)
        self.player.game_map.bullet_lst.append(bullet3)



class Scatter(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, player):
        super().__init__(pos, width, height, img_folder_path, player)
        self.shoot_delay = 10
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'scatter.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'scatter_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'scatter_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'scatter_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        rand_angle = randint(-15, 15)
        bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                        self.player.game_map, 5, self.angle + rand_angle)
        self.player.game_map.bullet_lst.append(bullet)


class Ranger(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, player):
        super().__init__(pos, width, height, img_folder_path, player)
        self.shoot_delay = 20
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'ranger.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'ranger_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'ranger_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'ranger_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                        self.player.game_map, 10, self.angle)
        self.player.game_map.bullet_lst.append(bullet)

# todo
#  make a special cannon that shoots a special type of bullet
#  the bullet should disappear after a certain amount of time

weapons_table = {
    'Streamlined' : TankCannon,
    'Spreader' : Spreader,
    'Scatter' : Scatter,
    'Ranger' : Ranger
}
