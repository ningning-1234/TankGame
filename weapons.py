from random import randint
from bullet import *
from engine_files.animation import Animation
from reticle import *

# generic tank cannon
class TankCannon():
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        self.position = pos
        self.width = width
        self.height = height
        self.explosion_size = 30

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
        self.shooting = False
        self.shoot_delay = 15
        self.last_shot = 0

    def shoot(self):
        '''
        Attempts to shoot a bullet. Does not shoot if on cooldown.
        Calls self.shoot_bullet() if able to shoot.
        Plays firing animation and changes reticle image upon successful shot.
        :return: None
        '''
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
        '''
        Abstract method.
        Called on when attempting to shoot while on cooldown.
        :return: None
        '''
        pass

    def shoot_bullet(self):
        '''
        Spawns a bullet object.
        Bullet object can have a random offset ranging between 5 and -5.
        Called on when attempting to shoot when not on cooldown.
        :return: None
        '''
        offsetx = randint(-5, 5)
        offsety = randint(-5, 5)
        bullet = Bullet((self.bullet_spawn[0] + offsetx, self.bullet_spawn[1] + offsety),
                        self.player.game_map, 5, self.angle, 5, self.explosion_size, self.player)

        self.player.game_map.bullet_lst.append(bullet)

    def update(self, *args, **kwargs):
        '''
        Updates the cannons position, angle and bullets spawn coordinates.
        Also checks when you can shoot.
        :param args:
        :param kwargs:
        :return: None
        '''
        self.position = self.body.center
        self.angle = get_angle(self.position, [self.reticle.x_pos, self.reticle.y_pos])
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) *  self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] + math.sin(math.radians(self.angle)) *  self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
        # self.angle = (self.angle+1)%360
        if (self.shooting):
            if (self.player.game_map.get_time() >= self.last_shot + self.shoot_delay):
                self.shooting = False
                self.reticle.img = self.reticle.default_img

    def draw(self, surface):
        '''
        Draws the cannon on surface.
        Cannon will be drawn rotated around its pivot point.
        :param surface: The surface the cannon will be drawn on.
        :return: None
        '''
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
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 30
        self.bullet_spawn_dist = 45
        self.angle_change = -15
        self.damage = 4
        self.explosion_size = 25
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
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
        '''
        Shoots 3 bullets in 3 angles.
        :return: None
        '''
        for g in range(0, 3):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 5, self.angle + self.angle_change, 4, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
            self.angle = self.angle + 15

class Scatter(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 10
        self.bullet_spawn_dist = 45
        self.explosion_size = 20
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
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
        '''
        Shoots bullets in random angle ranging between 15 to -15.
        :return: None
        '''
        rand_angle = randint(-15, 15)
        bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                        self.player.game_map, 5, self.angle + rand_angle, 4, self.explosion_size, self.player)
        self.player.game_map.bullet_lst.append(bullet)

class Ranger(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 20
        self.bullet_spawn_dist = 45
        self.explosion_size = 50
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
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
        '''
        Shoots a bullet that is fast.
        :return:
        '''
        bullet = Ranger_Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                                self.player.game_map, 10, self.angle, 2, self.explosion_size, self.player, 3, 1, 30)
        self.player.game_map.bullet_lst.append(bullet)

class Angles(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 0
        self.bullet_spawn_dist = 200
        self.angle_change = 0
        self.explosion_size = 20

        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        '''
        Shoots bullets in 24 angles.
        :return: None
        '''
        for g in range(0, 24):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 5, self.angle + self.angle_change, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
            self.angle = self.angle + 15

class Wider(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 5
        self.angle_change = -25
        self.explosion_size = 25

        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        '''
        Shoots 50 bullets in a spread.
        :return:
        '''
        for g in range(0, 50):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 8, self.angle + self.angle_change, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
            self.angle = self.angle + 1

class Pulse(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 60
        self.bullet_spawn_dist = 0
        self.angle_change = 0
        self.explosion_size = 10
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        '''
        Shoots bullets all around itself.
        :return:
        '''
        for g in range(0, 359):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 5, self.angle + self.angle_change, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
            self.angle = self.angle + 1

class Spiral(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 0
        self.bullet_spawn_dist = 0
        self.angle_change = 0
        self.explosion_size = 10
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        for g in range(0, 24):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 5, self.angle + self.angle_change, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
        self.angle = self.angle + 24

class CloseQuarters(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 2
        self.bullet_spawn_dist = 45
        self.bullet_timer = 20
        self.explosion_size = 15

        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        '''
        Shoots many short bullets in a wide spread.
        Short bullets have a timer before they explode.
        :return: None
        '''
        rand_angle = randint(-45, 45)
        bullet = Short_Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                              self.player.game_map, 5, self.angle + rand_angle, 1, self.explosion_size, self.player, self.bullet_timer)
        self.player.game_map.bullet_lst.append(bullet)

class Charge(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 600
        self.bullet_spawn_dist = 45
        self.bullet_timer = 30
        self.angle_change = -15
        self.explosion_size = 25
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
        self.fire_animation_imgs = [
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation1.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation2.png'), (width, height)),
            get_transparent_surface(pygame.image.load(img_folder_path + 'streamlined_animation3.png'), (width, height)),
        ]
        self.fire_animation = Animation(self.fire_animation_imgs, 2, [0, 1, 2, 3, 2, 1, 0], 1)
        self.default_img = self.fire_animation_imgs[0]
        self.img = self.default_img

    def shoot_bullet(self):
        for g in range(0, 30):
            bullet = Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                            self.player.game_map, 8, self.angle + self.angle_change, 2, self.explosion_size, self.player)
            self.player.game_map.bullet_lst.append(bullet)
            self.angle = self.angle + 1

    def cooldown_shoot(self):
        bullet = Short_Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                              self.player.game_map, 5, self.angle, self.explosion_size, self.bullet_timer)
        self.player.game_map.bullet_lst.append(bullet)

class Homer(TankCannon):
    def __init__(self, pos, width, height, img_folder_path, reticle_pos, player):
        super().__init__(pos, width, height, img_folder_path, reticle_pos, player)
        self.shoot_delay = 10
        self.bullet_spawn_dist = 45
        self.explosion_size = 20
        bullet_spawn_x = self.position[0] + math.cos(math.radians(self.angle)) * self.bullet_spawn_dist
        bullet_spawn_y = self.position[1] - math.sin(math.radians(self.angle)) * self.bullet_spawn_dist
        self.bullet_spawn = [bullet_spawn_x, bullet_spawn_y]
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
        if (self.player.player_num == 1):
            target = self.player.game_map.player2.tank_body
        else:
            target = self.player.game_map.player1.tank_body
        bullet = Homing_Bullet((self.bullet_spawn[0], self.bullet_spawn[1]),
                        self.player.game_map, 5, self.angle, 4, self.explosion_size, self.player, target)
        self.player.game_map.bullet_lst.append(bullet)

weapons_table = {
    'Streamlined' : TankCannon,
    'SL' : TankCannon,
    'Spreader' : Spreader,
    'SP' : Spreader,
    'Scatter' : Scatter,
    'SC' : Scatter,
    'Ranger' : Ranger,
    'RA' : Ranger,
    'CloseQuarters' : CloseQuarters,
    'CQ' : CloseQuarters,
    'Charge' : Charge,
    'CH' : Charge,
    'Homer' : Homer,
    'Ho' : Homer,
    'GGAngles' : Angles,
    'GGWider' : Wider,
    'GGPulse' : Pulse,
    'GGSpiral' : Spiral
}
