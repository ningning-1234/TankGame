import pygame
from utils import *

class MovableEntity(pygame.Rect):
    def __init__(self, pos, map, speed):
        super().__init__(pos)
        self.speed = speed
        self.map = map
        self.move_x = 0
        self.move_y = 0
        self.ignore_walls = False
        self.ignore_map_bounds = False

    def update(self, *args, **kwargs):
        self.move()
        self.move_x = 0
        self.move_y = 0

    def move(self):
        if(not self.ignore_map_bounds):
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

        dist = get_hyp([0,0],[self.move_x, self.move_y])
        if(dist>self.speed):
            exceed_ratio = self.speed / dist
            self.move_x = exceed_ratio * self.move_x
            self.move_y = exceed_ratio * self.move_y

        self.move_ip(self.move_x, self.move_y)
