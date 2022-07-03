import math
import pygame


def get_angle(point1, point2, degrees=True):
    xdist = point2[0] - point1[0]
    ydist = point2[1] - point1[1]
    angle_r = math.atan2(ydist, xdist)
    if (degrees):
        return math.degrees(angle_r) % 360
    return angle_r


def get_hyp(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def get_rotate_point(image, pos, originPos, angle):
    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    print(pivot_move)

    origin = (pos[0] - pivot_move[0]/2, #- originPos[0],
              pos[1] - pivot_move[1]/2 )#- originPos[1])
    # print(origin)
    return origin

