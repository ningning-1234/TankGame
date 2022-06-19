import pygame
from controller_mappings import *
from animation import *

default_kb_controls = {pygame.K_d: 'RIGHT',
                       pygame.K_s: 'DOWN',
                       pygame.K_a: 'LEFT',
                       pygame.K_w: 'UP',
                       pygame.K_RIGHT: 'RIGHT',
                       pygame.K_DOWN: 'DOWN',
                       pygame.K_LEFT: 'LEFT',
                       pygame.K_UP: 'UP'
                       }
default_controller_controls = {'DPAD_UP': 'UP',
                               'DPAD_DOWN': 'DOWN',
                               'DPAD_LEFT': 'LEFT',
                               'DPAD_RIGHT': 'RIGHT'
                               }

class Tank(pygame.Rect):
    def __init__(self, pos, map, color, player_num, kb_controls=default_kb_controls, controller_controls=default_controller_controls):
        super().__init__(pos)
        self.speed = 4
        self.move_x = 0
        self.move_y = 0
        self.color = color
        self.map = map
        self.player_num = player_num
        self.kb_controls = kb_controls
        self.controller_controls = controller_controls

    def update(self, *args, **kwargs):
        self.move_x = 0
        self.move_y = 0
        if(kwargs['kb_inputs'] is not None):
            self.parse_kb_inputs(kwargs['kb_inputs'])
        if(kwargs['controller_inputs'] is not None):
            self.parse_con_buttons(kwargs['controller_inputs'])
            self.parse_con_sticks(kwargs['controller_inputs'])
        self.move()

    def move(self):
        # left wall
        if (self[0] + self.move_x < self.map.bounds[0]):
            self.move_x = self.map.bounds[0] - self[0]

        # right wall
        if (self[0] + self[2] + self.move_x > self.map.bounds[2]):
            self.move_x = self.map.bounds[2] - (self[0] + self[2])

        # top wall
        if (self[1] + self.move_y < self.map.bounds[1]):
            self.move_y = self.map.bounds[1] - self[1]
        # bottom wall
        if (self[1] + self[3] + self.move_y > self.map.bounds[3]):
            self.move_y = self.map.bounds[3] - (self[1] + self[3])

        self.move_ip(self.move_x, self.move_y)

    def parse_kb_inputs(self, kb_inputs):
        for key in self.kb_controls:
            if (kb_inputs[key]):
                if (self.kb_controls[key] == 'RIGHT'):
                    self.move_x = self.speed
                if (self.kb_controls[key] == 'DOWN'):
                    self.move_y = self.speed
                if (self.kb_controls[key] == 'LEFT'):
                    self.move_x = -self.speed
                if (self.kb_controls[key] == 'UP'):
                    self.move_y = -self.speed

    def parse_con_buttons(self, con_inputs):
        for button in self.controller_controls:
            if (con_inputs.get_button(CON_BUTTONS[button])):
                if (self.controller_controls[button] == 'RIGHT'):
                    self.move_x = self.speed
                if (self.controller_controls[button] == 'DOWN'):
                    self.move_y = self.speed
                if (self.controller_controls[button] == 'LEFT'):
                    self.move_x = -self.speed
                if (self.controller_controls[button] == 'UP'):
                    self.move_y = -self.speed

    def parse_con_sticks(self, con_inputs):
        joy_stickX = round(con_inputs.get_axis(CON_AXIS['LEFT_H']) * 4)
        joy_stickY = round(con_inputs.get_axis(CON_AXIS['LEFT_V']) * 4)
        # left/right
        if(abs(joy_stickX)>1):
            self.move_x = round(self.speed * (joy_stickX / 4))
            # self.move_ip(round(self.speed * (joy_stickX / 4)), 0)
        # up/down
        if(abs(joy_stickY)>1):
            self.move_y = round(self.speed * (joy_stickY / 4))
            # self.move_ip(0, round(self.speed * (joy_stickY / 4)))


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)
