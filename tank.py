from utils import *
from animation import Animation

import pygame

from entity import *
from weapons import *
from controller_mappings import *
from bullet import *
from animation import *
from random import randint

default_kb_controls = {pygame.K_d: 'BODY RIGHT',
                       pygame.K_s: 'BODY DOWN',
                       pygame.K_a: 'BODY LEFT',
                       pygame.K_w: 'BODY UP',
                       pygame.K_RIGHT: 'BODY RIGHT',
                       pygame.K_DOWN: 'BODY DOWN',
                       pygame.K_LEFT: 'BODY LEFT',
                       pygame.K_UP: 'BODY UP'
                       }
default_controller_controls = {'DPAD_UP': 'BODY UP',
                               'DPAD_DOWN': 'BODY DOWN',
                               'DPAD_LEFT': 'BODY LEFT',
                               'DPAD_RIGHT': 'BODY RIGHT',
                               'L': 'SHOOT'
                               }

class Player():
    def __init__(self, player_num, tank_pos, reticle_pos, weapon, game_map, kb_controls=default_kb_controls,
                 controller_controls=default_controller_controls):
        self.player_num = player_num
        self.game_map = game_map
        self.kb_controls = kb_controls
        self.controller_controls = controller_controls

        self.folder = './assets/player' + str(player_num) + '/'

        self.tank_body = Tank(tank_pos, game_map, self.folder + 'body.png', self)
        self.reticle = Reticle((reticle_pos[0] + 80, reticle_pos[1] + 15),
                               game_map,
                               self.folder + 'reticle.png',
                               self.folder + 'reticle_shoot.png', self)
        if(weapon in weapons_table):
            self.cannon = weapons_table[weapon](self.tank_body.center, 60, 20, self.folder, self)
        else:
            self.cannon = TankCannon(self.tank_body.center, 60, 20, self.folder, self)

        self.shooting = False
        self.shoot_delay = 15
        self.last_shot = 0



    def update(self, *args, **kwargs):
        if (kwargs['kb_inputs'] is not None):
            self.parse_kb_inputs(kwargs['kb_inputs'])
        if (kwargs['controller_inputs'] is not None):
            self.parse_con_buttons(kwargs['controller_inputs'])
            self.parse_con_sticks(kwargs['controller_inputs'])

        if (self.shooting):
            if (self.game_map.get_time() >= self.last_shot + self.shoot_delay):
                self.shooting = False
                self.reticle.img = self.reticle.default_img
        self.tank_body.update()
        self.reticle.update()
        self.cannon.update()

    def parse_kb_inputs(self, kb_inputs):
        for key in self.kb_controls:
            if (kb_inputs[key]):
                if (self.kb_controls[key] == 'BODY RIGHT'):
                    self.tank_body.move_x = self.tank_body.speed
                if (self.kb_controls[key] == 'BODY DOWN'):
                    self.tank_body.move_y = self.tank_body.speed
                if (self.kb_controls[key] == 'BODY LEFT'):
                    self.tank_body.move_x = -self.tank_body.speed
                if (self.kb_controls[key] == 'BODY UP'):
                    self.tank_body.move_y = -self.tank_body.speed
                # shoot
                if (self.kb_controls[key] == 'SHOOT'):
                    if (not self.shooting):
                        self.shoot()

    def parse_con_buttons(self, con_inputs):
        for button in self.controller_controls:
            if (con_inputs.get_button(CON_BUTTONS[button])):
                # movement
                if (self.controller_controls[button] == 'BODY RIGHT'):
                    self.tank_body.move_x = self.tank_body.speed
                if (self.controller_controls[button] == 'BODY DOWN'):
                    self.tank_body.move_y = self.tank_body.speed
                if (self.controller_controls[button] == 'BODY LEFT'):
                    self.tank_body.move_x = -self.tank_body.speed
                if (self.controller_controls[button] == 'BODY UP'):
                    self.tank_body.move_y = -self.tank_body.speed
                # shoot
                if (self.controller_controls[button] == 'SHOOT'):
                    if (not self.shooting):
                        self.shoot()

    def parse_con_sticks(self, con_inputs):
        joy_stick_leftX = round(con_inputs.get_axis(CON_AXIS['LEFT_H']) * 4)
        joy_stick_leftY = round(con_inputs.get_axis(CON_AXIS['LEFT_V']) * 4)
        # left/right
        if (abs(joy_stick_leftX) > 1):
            self.tank_body.move_x = round(self.tank_body.speed * (joy_stick_leftX / 4))
            # self.move_ip(round(self.speed * (joy_stickX / 4)), 0)
        # up/down
        if (abs(joy_stick_leftY) > 1):
            self.tank_body.move_y = round(self.tank_body.speed * (joy_stick_leftY / 4))
            # self.move_ip(0, round(self.speed * (joy_stickY / 4)))

        joy_stick_rightX = round(con_inputs.get_axis(CON_AXIS['RIGHT_H']) * 4)
        joy_stick_rightY = round(con_inputs.get_axis(CON_AXIS['RIGHT_V']) * 4)
        # left/right
        if (abs(joy_stick_rightX) > 1):
            self.reticle.move_x = round(self.reticle.speed * (joy_stick_rightX / 4))
        # up/down
        if (abs(joy_stick_rightY) > 1):
            self.reticle.move_y = round(self.reticle.speed * (joy_stick_rightY / 4))

    def shoot(self):
        self.last_shot = self.game_map.get_time()
        # print(self.last_shot)
        self.shooting = True
        self.reticle.img = self.reticle.shoot_img
        self.cannon.shoot()

        # bullet = Bullet((self.cannon.bullet_spawn[0] + offset, self.cannon.bullet_spawn[1] + offset),
        #                 self.game_map, 5, self.cannon.angle)
        # self.game_map.bullet_lst.append(bullet)

        # bullet = Bullet((self.cannon.bullet_spawn), self.map, 5, self.cannon.angle)
        # self.map.bullet_lst.append(bullet)
        # bullet = Bullet((self.cannon.bullet_spawn), self.map, 5, self.cannon.angle)
        # self.map.bullet_lst.append(bullet)
        # self.cannon.fire_animation.reset()
        # self.cannon.animation = self.cannon.fire_animation


    def draw(self, surface):
        self.tank_body.draw(surface)
        self.cannon.draw(surface)
        self.reticle.draw(surface)

class Tank(MovableEntity):
    def __init__(self, pos, map, img_path, player):
        super().__init__(pos, map, 4)
        self.img_path = img_path
        self.img = get_transparent_surface(pygame.image.load(img_path), (self[2], self[3]))
        self.player = player

    def update(self, *args, **kwargs):
        super().update(args, kwargs)

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self)
        surface.blit(self.img, self)

class Reticle(MovableEntity):
    def __init__(self, pos, map, default_img_path, shoot_img_path, player):
        super().__init__((pos[0], pos[1], 20, 20), map, 3)
        # self.color = self.normal_color

        self.default_img_path = default_img_path
        self.shoot_img_path = shoot_img_path
        self.default_img = get_transparent_surface(pygame.image.load(default_img_path), (self[2], self[3]))
        self.shoot_img = get_transparent_surface(pygame.image.load(shoot_img_path), (self[2], self[3]))
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

