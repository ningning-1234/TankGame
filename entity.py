import pygame
from animation import Animation
from utils import *

class DrawableEntity(pygame.Rect):
    def __init__(self, rect, game_map):
        super().__init__(rect)
        self.game_map = game_map

class MovableEntity(DrawableEntity):
    def __init__(self, rect, game_map, speed):
        super().__init__(rect,game_map)
        self.position = [rect[0], rect[1]]
        self.speed = speed

        self.new_pos_rect = []
        self.move_x = 0
        self.move_y = 0
        self.move_dir = [0,0]

        self.ignore_walls = False
        self.ignore_map_bounds = False
        self.active = True

    def update(self, *args, **kwargs):
        self.move_dir = [0, 0]
        # moving right
        if (self.move_x > 0):
            self.move_dir[0] = 1
        # moving left
        elif (self.move_x < 0):
            self.move_dir[0] = -1
        # moving down
        if (self.move_y > 0):
            self.move_dir[1] = 1
        # moving up
        elif (self.move_y < 0):
            self.move_dir[1] = -1
        self.move()
        self.move_x = 0
        self.move_y = 0


    def move(self):
        self.new_pos_rect = (
            self.position[0] + self.move_x,                #top left x
            self.position[1] + self.move_y,                #top left y
            self.position[0] + self.width + self.move_x,   #bottom right x
            self.position[1] + self.height + self.move_y   #bottom right y
            )
        # left wall
        if (self.new_pos_rect[0] < self.game_map.bounds[0]):
            self.bound_collide(2)
        # right wall
        if (self.new_pos_rect[2] > self.game_map.bounds[2]):
            self.bound_collide(0)
        # top wall
        if (self.new_pos_rect[1] < self.game_map.bounds[1]):
            self.bound_collide(3)
        # bottom wall
        if (self.new_pos_rect[3] > self.game_map.bounds[3]):
            self.bound_collide(1)

        self.new_pos_rect = (self.position[0] + self.move_x,  # top left x
                             self.position[1] + self.move_y,  # top left y
                             self.position[0] + self.width + self.move_x,  # bottom right x
                             self.position[1] + self.height + self.move_y  # bottom right y
                             )
        # colliding_blocks = []
        # for block in self.map.block_lst:
        #     if(self.colliderect(block)):
        #         colliding_blocks.append(block)

        for block in self.game_map.block_lst:
            for wall in block.wall_lst:
                if(wall.entity_collide(self)):
                    self.wall_collide(wall)

        dist = get_hyp([0,0],[self.move_x, self.move_y])
        if(dist>self.speed):
            exceed_ratio = self.speed / dist
            self.move_x = exceed_ratio * self.move_x
            self.move_y = exceed_ratio * self.move_y

        self.position[0] = self.position[0] + self.move_x
        self.position[1] = self.position[1] + self.move_y
        self.move_ip(round(self.position[0]-self[0]), round(self.position[1]-self[1]))


    def bound_collide(self, bound):
        if (not self.ignore_map_bounds):
            if(bound == 0):
                self.move_x = self.game_map.bounds[2] - (self.position[0] + self.width)
            if(bound == 1):
                self.move_y = self.game_map.bounds[3] - (self.position[1] + self.height)
            if(bound == 2):
                self.move_x = self.game_map.bounds[0] - self.position[0]
            if(bound == 3):
                self.move_y = self.game_map.bounds[1] - self.position[1]

    # def block_collide(self, block):
    #     pass
    def wall_collide(self, wall):
        # print('collide')
        pass