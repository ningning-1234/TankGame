from weapons import *
from mine import *
from engine_files.controller_mappings import *
from bullet import *
from engine_files.animation import *

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
                               'L': 'SHOOT',
                               'R': 'MINE'
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
        self.mine_counter = 0
        self.mine_limit = 3
        self.place_delay = 15
        self.last_mine = -self.place_delay - 1

        # self.shooting = False
        # self.shoot_delay = 15
        # self.last_shot = 0
        self.reticle = None
        if(weapon in weapons_table):
            self.cannon = weapons_table[weapon](self.tank_body.center, 60, 20, self.folder, reticle_pos, self)
        else:
            self.cannon = TankCannon(self.tank_body.center, 60, 20, self.folder, reticle_pos, self)
        # self.mine = Mine(self.tank_body.center, self.game_map, self, 20)

        if(self.reticle is None):
            self.reticle = Reticle((reticle_pos[0] + 80, reticle_pos[1] + 15), game_map, self.folder, self)

    def update(self, *args, **kwargs):
        if (kwargs['kb_inputs'] is not None):
            self.parse_kb_inputs(kwargs['kb_inputs'])
        if (kwargs['controller_inputs'] is not None):
            self.parse_con_buttons(kwargs['controller_inputs'])
            self.parse_con_sticks(kwargs['controller_inputs'])

        # if (self.shooting):
        #     if (self.game_map.get_time() >= self.last_shot + self.shoot_delay):
        #         self.shooting = False
        #         self.reticle.img = self.reticle.default_img

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
                    self.cannon.shoot()
                    # if (not self.shooting):
                    #     self.shoot()
                if (self.kb_controls[key] == 'MINE'):
                    self.place_mine()

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
                    self.cannon.shoot()
                if (self.controller_controls[button] == 'MINE'):
                    self.place_mine()

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

    def place_mine(self):
        if (not self.game_map.get_time() >= self.last_mine + self.place_delay):
            return
        if(self.mine_counter < self.mine_limit):
            mine = Mine(self.tank_body.center, self.game_map, self, 100, 5 * 60)
            self.game_map.entity_lst.append(mine)
            self.last_mine = self.game_map.get_time()
            self.mine_counter = self.mine_counter + 1
        print(self.mine_counter)

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
