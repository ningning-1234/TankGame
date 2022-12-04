from explosion import *

from engine_files.entity import *
class Bullet(MovableEntity):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner):
        super().__init__((pos[0] - 10, pos[1] - 5, 10, 10), game_map, speed)
        self.angle = angle
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/bullet.png'),(20, 10))

        self.x_shift = math.cos(math.radians(self.angle))*self.speed
        self.y_shift = math.sin(math.radians(self.angle))*self.speed
        self.explosion_size = explosion_size
        self.explosion_damage = 2

        self.owner = owner
        # whether the bullet can hit its owner
        self.self_damage = False
        self.damage = damage
        self.block_damage = self.damage
        self.collide_entities = []

    def bound_collide(self, bound):
        '''
        Explodes the bullet.
        Is called if a bound is colliding with a bullet.
        :param bound: The bound that the bullet is colliding with.
        :return: None
        '''
        if(not self.active):
            return
        self.explode()
        self.active = False

    def wall_collide(self, wall):
        '''
        Explodes the bullet.
        Is called if a wall is colliding with a bullet.
        :param wall: The wall that the bullet is colliding with.
        :return: None
        '''
        if(not self.active):
            return
        self.explode()
        self.active = False
        if (wall not in self.collide_entities):
            self.collide_entities.append(wall)

    def block_collide(self, block):
        '''
        Explodes the bullet.
        Is called if a block is colliding with a bullet.
        :param block: The bound that the bullet is colliding with.
        :return: None
        '''
        if(not self.active):
            return
        self.explode()
        self.active = False

        if (block not in self.collide_entities):
            block.entity_collide(self)
            self.collide_entities.append(block)

    def player_collide(self, player):
        '''
        Explodes the bullet.
        Is called if a player is colliding with a bullet.
        :param player: The bound that the bullet is colliding with.
        :return: None
        '''
        if(not self.active):
            return
        self.explode()
        self.active = False
        if (not self.self_damage):
            if (player == self.owner):
                return
        if(player not in self.collide_entities):
            player.take_damage(self.damage, self)
            self.collide_entities.append(player)

    def explode(self):
        '''
        Creates an explosion object in the center of the bullet object.
        :return: None
        '''
        if(self.active == True):
            pos = self.explosion_size / 2
            explosion = Explosion((self.centerx - pos, self.centery - pos),
                                  self.explosion_damage, self.explosion_size, self.game_map, 10, self.owner)
            explosion.self_damage = False
            self.game_map.entity_lst.append(explosion)

    def update(self, *args, **kwargs):
        '''
        Updates the bullet position.
        :param args:
        :param kwargs:
        :return: None
        '''
        if(not self.active):
            self.game_map.bullet_lst.remove(self)
        self.move_x = self.x_shift
        self.move_y = self.y_shift
        super().update(args, kwargs)

    def draw(self, surface):
        '''
        Draws bullets on surface.
        Bullets will be rotated if shot at different angles.
        :param surface: The surface the bullet will be drawn on.
        :return: None
        '''
        if(not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Short_Bullet(Bullet):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner, bullet_timer):
        super().__init__(pos, game_map, speed, angle, damage, explosion_size, owner)
        self.bullet_timer = bullet_timer
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/short_bullet.png'), (10, 10))

    def bullet_despawn(self):
        '''
        Explodes the bullet.
        Is called if the bullet timer hits 0.
        :return: None
        '''
        self.explode()
        self.active = False

    def update(self, *args, **kwargs):
        '''
        Updates the bullet timer.
        :param args:
        :param kwargs:
        :return: None
        '''
        self.bullet_timer = self.bullet_timer - 1
        if (self.bullet_timer <= 0):
            self.bullet_despawn()
        super().update(args, kwargs)

    def draw(self, surface):
        '''
        Draws short bullets on surface.
        Short bullets will be rotated if shot at different angles.
        :param surface: The surface the bullet will be drawn on.
        :return: None
        '''
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Ranger_Bullet(Bullet):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner, bullet_scale_timer, bullet_scale_amount, bullet_scale_cap):
        super().__init__(pos, game_map, speed, angle, damage, explosion_size, owner)
        self.bullet_scale_timer = bullet_scale_timer
        self.bullet_scale_amount = bullet_scale_amount
        self.bullet_scale_cap = bullet_scale_cap
        self.bullet_scale_time = bullet_scale_timer
        self.damage = damage
        self.explosion_size = explosion_size
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/ranger_bullet.png'), (20, 10))

    def update(self, *args, **kwargs):
        self.bullet_scale_timer = self.bullet_scale_timer - 1
        if (self.bullet_scale_timer <= 0 and self.damage < self.bullet_scale_cap):
            self.damage = self.damage + self.bullet_scale_amount
            self.explosion_size = self.explosion_size + self.bullet_scale_amount
            self.bullet_scale_timer = self.bullet_scale_time
            print(self.damage)
        super().update(args, kwargs)

    def draw(self, surface):
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Homing_Bullet(Bullet):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner, target, max_turn, turn_timer):
        super().__init__(pos, game_map, speed, angle, damage, explosion_size, owner)
        # self.speed = speed
        self.max_turn = max_turn
        self.turn_timer = turn_timer
        self.turn_time = self.turn_timer
        # self.speed_timer = 10
        self.target = target
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/homing_bullet.png'), (20, 10))

    def update(self, *args, **kwargs):
        new_angle = get_point_angle(self.center, self.target.center, False)
        angle_dif = new_angle - self.angle
        # print(str(new_angle)+' '+str(self.angle)+' '+str(angle_dif))
        if (angle_dif <-180):
            angle_dif = angle_dif+360
        if (angle_dif > self.max_turn):
            angle_dif = self.max_turn
        if (angle_dif < -self.max_turn):
            angle_dif = -self.max_turn
        self.angle = self.angle + angle_dif
        self.x_shift = math.cos(math.radians(self.angle)) * self.speed
        self.y_shift = math.sin(math.radians(self.angle)) * self.speed
        self.turn_timer = self.turn_timer - 1
        if(self.turn_timer <= 0 and self.max_turn != 0):
            self.max_turn = self.max_turn - 1
            self.turn_time = self.turn_time - 1
            self.turn_timer = self.turn_time
        # self.speed_timer = self.speed_timer -1
        # if(self.speed_timer <= 0 and self.speed > 3):
        #     self.speed = self.speed - 0.2
        #     self.speed_timer = 10
        # print(self.angle)
        super().update(args, kwargs)

    def draw(self, surface):
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Explode_Bullet(Bullet):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner, weapon):
        super().__init__(pos, game_map, speed, angle, damage, explosion_size, owner)
        self.weapon = weapon
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/explode_bullet.png'), (20, 10))
        self.explosion_damage = 8

    def bullet_explode(self):
        self.explode()
        self.active = False

    def explode(self):
        if (self.active == True):
            pos = self.explosion_size / 2
            explosion = Mine_Explosion((self.centerx - pos, self.centery - pos),
                                  self.explosion_damage, self.explosion_size, self.game_map, 10, self.owner)
            explosion.self_damage = False
            explosion.damage = self.explosion_damage
            self.game_map.entity_lst.append(explosion)
        self.weapon.last_bullet = None

    def draw(self, surface):
        if (not self.active):
            return
        rotated_img, rotated_rect = centered_rotate(self.img, self, -self.angle)
        surface.blit(rotated_img, rotated_rect)

class Target_Bullet(Homing_Bullet):
    def __init__(self, pos, game_map, speed, angle, damage, explosion_size, owner, target, max_turn, turn_timer, bullet_timer):
        super().__init__(pos, game_map, speed, angle, damage, explosion_size, owner, target, max_turn, turn_timer)
        self.img = self.img = get_transparent_surface(pygame.image.load('./assets/homing_bullet.png'), (20, 10))
        self.bullet_timer = bullet_timer

    def bullet_despawn(self):
        '''
        Explodes the bullet.
        Is called if the bullet timer hits 0.
        :return: None
        '''
        self.explode()
        self.active = False

    def update(self, *args, **kwargs):
        self.bullet_timer = self.bullet_timer - 1
        if (self.bullet_timer <= 0):
            self.bullet_despawn()
        # if(not self.active):
        #     self.owner.cannon.has_bullet = False
        super().update(args, kwargs)
