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
        self.move_angle = 0
        self.next_pos_rect = pygame.Rect(self)

        self.ignore_walls = False
        self.ignore_map_bounds = False
        self.active = True

    def update(self, *args, **kwargs):
        self.move_dir = [0, 0]
        self.move_angle = 0
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
        self.next_pos_rect = pygame.Rect(self[0] + self.move_x, self[1] + self.move_y, self.width, self.height)
        self.move()
        self.move_x = 0
        self.move_y = 0

    def move(self):
        # map bounds check
        self.bounds_check()
        # colliding_blocks = []
        # for block in self.map.block_lst:
        #     if(self.colliderect(block)):
        #         colliding_blocks.append(block)
        self.wall_check()

        dist = get_hyp([0,0],[self.move_x, self.move_y])
        if(dist>self.speed):
            exceed_ratio = self.speed / dist
            self.move_x = exceed_ratio * self.move_x
            self.move_y = exceed_ratio * self.move_y

        self.position[0] = self.position[0] + self.move_x
        self.position[1] = self.position[1] + self.move_y
        self.move_ip(round(self.position[0]-self[0]), round(self.position[1]-self[1]))


    def bounds_check(self):
        # left wall
        if (self.next_pos_rect.left < self.game_map.bounds[0]):
            self.bound_collide(2)
        # right wall
        if (self.next_pos_rect.right-1 > self.game_map.bounds[2]):
            self.bound_collide(0)
        # top wall
        if (self.next_pos_rect.top < self.game_map.bounds[1]):
            self.bound_collide(3)
        # bottom wall
        if (self.next_pos_rect.bottom-1 > self.game_map.bounds[3]):
            self.bound_collide(1)

    def wall_check(self):
        # for block in self.game_map.block_lst:
        #     for wall in block.wall_lst:
        #         if (wall.entity_move_collide(self)):
        #             self.wall_collide(wall)

        for block in self.game_map.block_lst:
            if(block.colliderect(self.next_pos_rect)):
                self.block_collide(block)
                for wall in block.wall_lst:
                    if (wall.entity_move_collide(self)):
                        self.wall_collide(wall)

                    if (not block.colliderect(self.next_pos_rect)):
                        # print('over')
                        break

    def bound_collide(self, bound):
        '''
        Actions taken when colliding with a map bound
        :param bound:
        :return:
        '''
        if (self.ignore_map_bounds):
            return
        if(bound == 0):
            self.move_x = self.game_map.bounds[2] - (self.position[0] + self.width)
        if(bound == 1):
            self.move_y = self.game_map.bounds[3] - (self.position[1] + self.height)
        if(bound == 2):
            self.move_x = self.game_map.bounds[0] - self.position[0]
        if(bound == 3):
            self.move_y = self.game_map.bounds[1] - self.position[1]
        self.next_pos_rect = pygame.Rect(self[0] + self.move_x, self[1] + self.move_y, self.width, self.height)

    def block_collide(self, block):
        pass

    def wall_collide(self, wall):
        if(self.ignore_walls):
            return
        # push right
        if (wall.dir == 0):
            print('right')
            self.move_x = wall.point1[0] - self.position[0] + 1
        # push down
        if (wall.dir == 1):
            print('down')
            self.move_y = wall.point1[1] - (self.position[1]) + 1
        # push left
        if (wall.dir == 2):
            print('left')
            self.move_x = wall.point1[0] - (self.position[0] + self.width)
        # push up
        if (wall.dir == 3):
            print('up')
            self.move_y = wall.point1[1] - (self.position[1] + self.height)
        self.next_pos_rect = pygame.Rect(self[0] + self.move_x, self[1] + self.move_y, self.width, self.height)

