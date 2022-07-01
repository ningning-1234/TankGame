import math

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
# todo
#  make a reticle for the tank
#  make separate class for reticle
#  pass separate controls

class Player():
    def __init__(self,  player_num, pos, colors, map, kb_controls=default_kb_controls, controller_controls=default_controller_controls):
        self.player_num = player_num
        # self.pos = pos
        self.map = map
        self.kb_controls = kb_controls
        self.controller_controls = controller_controls

        self.tank_body = Tank(pos, map, colors[0], self)
        self.reticle = Reticle((pos[0] + 80, pos[1], 10, 10), map, colors[1], self)

        self.shooting = False
        self.shoot_delay = 20
        self.last_shot=0

    def update(self, *args, **kwargs):
        if(kwargs['kb_inputs'] is not None):
            self.parse_kb_inputs(kwargs['kb_inputs'])
        if(kwargs['controller_inputs'] is not None):
            self.parse_con_buttons(kwargs['controller_inputs'])
            self.parse_con_sticks(kwargs['controller_inputs'])

        if(self.shooting):
            if(self.map.get_time() >= self.last_shot + self.shoot_delay):
                self.shooting = False
                self.reticle.color = self.reticle.normal_color

        self.tank_body.update()
        self.reticle.update()

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
                    if(not self.shooting):
                        self.shoot()

    def parse_con_sticks(self, con_inputs):
        joy_stick_leftX = round(con_inputs.get_axis(CON_AXIS['LEFT_H']) * 4)
        joy_stick_leftY = round(con_inputs.get_axis(CON_AXIS['LEFT_V']) * 4)
        # left/right
        if(abs(joy_stick_leftX)>1):
            self.tank_body.move_x = round(self.tank_body.speed * (joy_stick_leftX / 4))
            # self.move_ip(round(self.speed * (joy_stickX / 4)), 0)
        # up/down
        if(abs(joy_stick_leftY)>1):
            self.tank_body.move_y = round(self.tank_body.speed * (joy_stick_leftY / 4))
            # self.move_ip(0, round(self.speed * (joy_stickY / 4)))

        joy_stick_rightX = round(con_inputs.get_axis(CON_AXIS['RIGHT_H']) * 4)
        joy_stick_rightY = round(con_inputs.get_axis(CON_AXIS['RIGHT_V']) * 4)
        # left/right
        if(abs(joy_stick_rightX)>1):
            self.reticle.move_x = round(self.reticle.speed * (joy_stick_rightX / 4))
        # up/down
        if(abs(joy_stick_rightY)>1):
            self.reticle.move_y = round(self.reticle.speed * (joy_stick_rightY / 4))

    def shoot(self):
        self.last_shot = self.map.get_time()
        print(self.last_shot)
        self.shooting = True
        self.reticle.color = self.reticle.shoot_color
        # todo spawn bullet

    def draw(self, surface):
        self.tank_body.draw(surface)
        self.reticle.draw(surface)

class Tank(MovableEntity):
    def __init__(self, pos, map, color, player):
        super().__init__(pos, map, 4)
        self.color = color
        self.player = player

    def update(self, *args, **kwargs):
        super().update(args, kwargs)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)

class Reticle(MovableEntity):
    def __init__(self, pos, map, color, player):
        super().__init__(pos, map, 3)
        self.normal_color = color
        self.shoot_color = (200, 225, 255)
        self.color = self.normal_color
        self.player= player
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
        dist = math.sqrt((body.centerx-(self.centerx + self.move_x))**2+(body.centery-(self.centery + self.move_y))**2)
        if(dist>self.tank_radius):
            # print('exceeded')
            exceed_ratio = (dist - self.tank_radius)/dist
            exceed_x = body.centerx - self.centerx
            exceed_y = body.centery - self.centery
            self.move_x = exceed_ratio * exceed_x
            self.move_y = exceed_ratio * exceed_y
        super().move()


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)

# todo
#  implement a button for shooting
#  have the tank's reticle light up when shooting