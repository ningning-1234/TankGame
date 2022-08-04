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
        self.dir = dir

    def entity_collide(self,entity):
        # right wall
        if(self.dir==0):
            if(entity.move_dir[0]!=-1):
                return False
        # bottom wall
        if(self.dir==1):
            if(entity.move_dir[1]!=-1):
                return False
        # left wall
        if(self.dir==2):
            if(entity.move_dir[0]!=1):
                return False
        # top wall
        if(self.dir==3):
            if(entity.move_dir[1]!=1):
                return False

        return True

class Block(pygame.Rect):
    def __init__(self, pos, block_type):
        size = (50,50)
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
        corner1 = (self.pos[0], self.pos[1])
        corner2 = (self.size[0] + self.pos[0], self.pos[1])
        corner3 = (self.size[0] + self.pos[0], self.pos[1] + self.pos[1])
        corner4 = (self.size[0], self.pos[1] + self.pos[1])
        self.wall_lst = [Wall(corner2, corner3, 0),
                         Wall(corner4, corner3, 1),
                         Wall(corner1, corner4, 2),
                         Wall(corner1, corner2, 3)]
        self.folder = './assets/blocks/'+sprite_folder
        self.random_sprite = randint(1, 2)
        self.img = get_transparent_surface(pygame.image.load(self.folder + '/block' + str(self.random_sprite) + '.png'), (self[2], self[3]))

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface):
        surface.blit(self.img, self)

# todo
#  give the blocks an image
#  create 3 images
#  give each block a random image
#  resize the images to fit the block
