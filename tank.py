from utils import *

import pygame

from entity import *
from controller_mappings import *
from animation import *

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
    def __init__(self, player_num, pos, colors, map, kb_controls=default_kb_controls,
                 controller_controls=default_controller_controls):
        self.player_num = player_num
        # self.pos = pos
        self.map = map
        self.kb_controls = kb_controls
        self.controller_controls = controller_controls

        self.tank_body = Tank(pos, map, colors[0], './assets/body_p' + str(player_num) + '.png', self)
        self.reticle = Reticle((pos[0] + 80, pos[1]), map, colors[1], './assets/reticle_p' + str(player_num) + '.png',
                               self)
        self.cannon = TankCannon(self.tank_body.center, 60, 20, './assets/cannon_p' + str(player_num) + '.png', self)

        self.shooting = False
        self.shoot_delay = 20
        self.last_shot = 0

    def update(self, *args, **kwargs):
        if (kwargs['kb_inputs'] is not None):
            self.parse_kb_inputs(kwargs['kb_inputs'])
        if (kwargs['controller_inputs'] is not None):
            self.parse_con_buttons(kwargs['controller_inputs'])
            self.parse_con_sticks(kwargs['controller_inputs'])

        if (self.shooting):
            if (self.map.get_time() >= self.last_shot + self.shoot_delay):
                self.shooting = False
                self.reticle.color = self.reticle.normal_color

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
        self.last_shot = self.map.get_time()
        print(self.last_shot)
        self.shooting = True
        self.reticle.color = self.reticle.shoot_color
        # todo spawn bullet

    def draw(self, surface):
        self.tank_body.draw(surface)
        self.cannon.draw(surface)
        self.reticle.draw(surface)


class Tank(MovableEntity):
    def __init__(self, pos, map, color, img_path, player):
        super().__init__(pos, map, 4)
        self.color = color
        self.img_path = img_path
        self.img = pygame.image.load(img_path)
        self.img.set_colorkey((0, 0, 0))
        self.player = player

    def update(self, *args, **kwargs):
        super().update(args, kwargs)

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self)
        surface.blit(self.img, self)


class Reticle(MovableEntity):
    def __init__(self, pos, map, color, img_path, player):
        super().__init__((pos[0], pos[1], 20, 20), map, 3)
        self.normal_color = color
        self.shoot_color = (200, 225, 255)
        self.color = self.normal_color
        self.img_path = img_path
        self.img = get_transparent_surface(pygame.image.load(img_path), (self[2], self[3]))

        self.player = player
        self.tank_radius = 200

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


class TankCannon():
    def __init__(self, pos, width, height, img_path, player):
        self.position = pos
        self.width = width
        self.height = height
        self.img_path = img_path
        self.img = get_transparent_surface(pygame.image.load(img_path), (width, height))
        self.player = player

        self.body = player.tank_body
        self.reticle = player.reticle

        # position of the pivot on the image
        # self.image_pivot_pos = [0, 0]
        self.image_pivot_pos = [height/2, height/2]
        # self.image_pivot_pos = [height/2, height/2]

        # self.pivotX = self.width / 2
        # self.pivotY = self.height / 2
        #
        # self.bodyAnchorX = self.body.centerx
        # self.bodyAnchorY = self.body.centery
        #
        # self.centerx = self.bodyAnchorX + (self.width / 2 - self.pivotX)
        # self.centery = self.bodyAnchorY + (self.height / 2 - self.pivotY)

        self.angle = get_angle(self.position, [self.reticle.x_pos, self.reticle.y_pos])
        # self.angle = 0

    def update(self, *args, **kwargs):
        self.position = self.body.center

        self.angle = get_angle(self.position, [self.reticle.x_pos, self.reticle.y_pos])
        # self.angle = (self.angle+1)%360

    def draw(self, surface):
        # position rectangle for the image
        img_pos_rect = [self.position[0] - self.image_pivot_pos[0],
                        self.position[1] - self.image_pivot_pos[1],
                        self.width, self.height]

        # centered rotation of image
        rotated_img, rotated_rect = centered_rotate(self.img, img_pos_rect, -self.angle)

        # rotate image about a pivot
        pivot_rect = img_pivot_rotate(rotated_img, rotated_rect, self.position, -self.angle)
        # pivot_rect = img_pivot_rotate(rotated_img, rotated_rect, pivot_point, -self.angle)

        # pygame.draw.rect(surface, [250, 250, 250], (pivot_rect[0], pivot_rect[1], rotated_img.get_rect()[2], rotated_img.get_rect()[3]))
        # pygame.draw.rect(surface, [250, 150, 150], (rotated_rect[0], rotated_rect[1], rotated_img.get_rect()[2], rotated_img.get_rect()[3]))

        # pygame.draw.rect(surface, [150, 250, 250], img_pos_rect)
        # pygame.draw.rect(surface, [150, 250, 250], (rotated_rect[0],rotated_rect[1],60,20))

        surface.blit(rotated_img, pivot_rect)

        pivot_rotate_point = pivot_rotate(self.position, [self.position[0] + 25, self.position[1] + 25], self.angle)
        # print(pivot_rotate_point)
        # pygame.draw.rect(surface, [150, 150,250], (pivot_point[0],pivot_point[1],2,2))    # pivot point
        pygame.draw.rect(surface, [250, 150, 150], (self.position[0], self.position[1], 2, 2))  # position
        # pygame.draw.rect(surface, [250, 150, 150], img_pos_rect)          # position

# todo
#  when the shoot button is pressed, create a bullet object on the body of the tank
#  the bullet should be at the angle of the cannon
#  the reticle should change its texture while on cooldown
#  give the cannon an animation when firing
