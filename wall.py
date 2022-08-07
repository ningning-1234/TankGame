import pygame
from random import randint
from utils import *


# 0 right
# 1 down
# 2 left
# 3 up
class Wall():
    def __init__(self, point1, point2, dir):
        self.point1 = point1
        self.point2 = point2
        self.line = get_line_equ(self.point2, self.point1)
        # print(self.point1, self.point2, self.line)
        self.dir = dir
        self.angle = 0

    def entity_move_collide(self, entity):
        '''
        Check if an entity's movement will collide with a wall
        :param entity:
        :return:
        '''
        # direction check
        # right wall
        if (self.dir == 0):
            if (entity.move_dir[0] != -1):
                return False
            # print('r', entity.left  , self.point1[0])
            if (entity.left < self.point1[0]):
                return False
        # bottom wall
        if (self.dir == 1):
            if (entity.move_dir[1] != -1):
                return False
            # print('b', entity.top, self.point1[1])
            if (entity.top < self.point1[1]):
                return False
        # left wall
        if (self.dir == 2):
            if (entity.move_dir[0] != 1):
                return False
            # print('l', entity.right, self.point1[0])
            if (entity.right > self.point1[0]):
                return False
        # top wall
        if (self.dir == 3):
            if (entity.move_dir[1] != 1):
                return False
            # print('t', entity.bottom, self.point1[1])
            if (entity.bottom > self.point1[1]):
                return False
        wall_line = (self.line, self.point1, self.point2)
        # print('check ' + str(self.dir), wall_line)
        # movement lines for each corner
        move_lines = [
            # top left
            (get_line_equ(entity.topleft, entity.next_pos_rect.topleft),
             entity.topleft, entity.next_pos_rect.topleft),
            # top right
            (get_line_equ((entity.right-1, entity.top), (entity.next_pos_rect.right-1, entity.next_pos_rect.top-1)),
             (entity.right-1, entity.top), (entity.next_pos_rect.right-1, entity.next_pos_rect.top-1)),
            # bottom left
            (get_line_equ((entity.left, entity.bottom-1), (entity.next_pos_rect.left, entity.next_pos_rect.bottom-1)),
             (entity.left, entity.bottom - 1), (entity.next_pos_rect.left, entity.next_pos_rect.bottom - 1)),
            # bottom right
            (get_line_equ((entity.right-1, entity.bottom-1), (entity.next_pos_rect.right-1, entity.next_pos_rect.bottom-1)),
             (entity.right-1, entity.bottom-1), (entity.next_pos_rect.right-1, entity.next_pos_rect.bottom-1)),
        ]
        for move_line in move_lines:
            # inter = line_intersect_point(move_line, wall_line)
            i = line_segment_intersect_point(move_line, wall_line, (True, True))
            # print(move_line)
            # print(i)
            if (i[0]):
                return True
        return False


class Block(pygame.Rect):
    def __init__(self, pos, block_type):
        size = (50, 50)
        sprite_folder = '1-1_block'
        if (block_type == 1):
            size = (50, 50)
            sprite_folder = '1-1_block'
        if (block_type == 2):
            size = (100, 100)
            sprite_folder = '2-2_block'
        if (block_type == 3):
            size = (100, 50)
            sprite_folder = '2-1_block'
        super().__init__(pos, size)
        self.pos = pos
        self.size = size
        # top left
        corner1 = (self.pos[0], self.pos[1])
        # top right
        corner2 = (self.pos[0] + self.size[0]-1, self.pos[1])
        # bottom right
        corner3 = (self.pos[0] + self.size[0]-1, self.pos[1] + self.size[1]-1)
        # bottom left
        corner4 = (self.pos[0], self.pos[1] + self.size[1]-1)
        # print(self.pos, self.size)
        self.wall_lst = [
            Wall(corner3, corner2, 0),  # right
            Wall(corner3, corner4, 1),  # bottom
            Wall(corner1, corner4, 2),  # left
            Wall(corner1, corner2, 3),  # top
        ]
        self.folder = './assets/blocks/' + sprite_folder
        self.random_sprite = randint(1, 2)
        self.img = get_transparent_surface(pygame.image.load(self.folder + '/block' + str(self.random_sprite) + '.png'),
                                           (self[2], self[3]))

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface):
        surface.blit(self.img, self)

# todo
#  give the blocks an image
#  create 3 images
#  give each block a random image
#  resize the images to fit the block
