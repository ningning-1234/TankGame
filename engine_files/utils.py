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
    '''
    Calculates the distance between two points

    :param point1:  first point as a list
    :param point2:  second point as a list
    :return:    distance betwen the two points
    '''
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# rotates about the centerof image at a certain position
def centered_rotate(img, position, angle):
    '''
    Rotates an image in place by offseting its position

    :param img: image to be rotated
    :param position: initial position of the image
    :param angle: angle the image will be rotated in degrees
    :return: tuple containing the rotated image and its new position
    '''
    # get rectangle from img
    img_rect = img.get_rect()

    # rotate
    rot_img = pygame.transform.rotate(img, angle)
    rot_img_rect = rot_img.get_rect()

    new_pos = [position[0], position[1]]
    # move to corner
    new_pos[0] = new_pos[0] - rot_img_rect.centerx
    new_pos[1] = new_pos[1] - rot_img_rect.centery

    # move to center
    new_pos[0] = new_pos[0] + img_rect.centerx
    new_pos[1] = new_pos[1] + img_rect.centery

    return rot_img, new_pos


# move a point a certain angle around a pivot
def pivot_rotate(position, pivot_point, pivot_angle):
    '''
    Moves a point around a pivot at a given angle

    :param position: coordinates of the point to be moved
    :param pivot_point: coordinates of the pivot
    :param pivot_angle: angle the point will move around the pivot in degrees
    :return:    coordinates of the new point
    '''
    if (pivot_angle % 360 == 0):
        return position
    # get distance between center of image and pivot point
    pivot_point_dist = get_hyp(position, pivot_point)
    # print(pivot_point_dist)

    # get the angle between the center of the image and the pivot point
    pivot_point_angle = math.degrees(math.atan2(pivot_point[1] - position[1], -(pivot_point[0] - position[0]))) % 360

    # get angle of new position
    new_pivot_point_angle = (pivot_point_angle + pivot_angle) % 360

    # new point relative to pivot
    new_pos_x = math.cos(math.radians(new_pivot_point_angle)) * pivot_point_dist
    new_pos_y = -math.sin(math.radians(new_pivot_point_angle)) * pivot_point_dist
    # print(new_pos_x, new_pos_y)

    # print(position[0],pivot_point[0], new_pos_x)
    # print(position[1],pivot_point[1], new_pos_y)

    return [pivot_point[0] + new_pos_x, pivot_point[1] + new_pos_y]


# move an image at a certain angle around a pivot
def img_pivot_rotate(img, position, pivot_point, pivot_angle):
    '''
    Moves an image around a pivot at a given angle

    :param img: image to be moved
    :param position: original postion of the image
    :param pivot_point: coordinates of the pivot on the surface
    :param pivot_angle: angle the point will move around the pivot in degrees
    :return: new position of the image
    '''
    if (pivot_angle % 360 == 0):
        return position
    img_rect = img.get_rect()
    # center of the image relative to the main surface
    rect_center_x = position[0] + img_rect.centerx
    rect_center_y = position[1] + img_rect.centery

    # pivot coords on main surface
    # pivot_cord_x = img_size_rect[0] + img_pivot_point[0]
    # pivot_cord_y = img_size_rect[1] + img_pivot_point[1]

    # print(img_center_x, img_center_y)
    # print(position[0]+img_rect.centerx, position[1]+img_rect.centery)
    # print(new_pos[0]+rot_img_rect.centerx, new_pos[1]+rot_img_rect.centery)

    # print(rect_center_x, rect_center_y)
    # print(pivot_cord_x, pivot_cord_y)

    # new center relative to main surface
    new_center = pivot_rotate([rect_center_x, rect_center_y], pivot_point, pivot_angle)
    # print(new_center)

    # offset original rect
    new_pos = [position[0], position[1]]
    new_pos[0] = new_pos[0] - (rect_center_x - new_center[0])
    new_pos[1] = new_pos[1] - (rect_center_y - new_center[1])
    # print(new_pos)

    return new_pos


def get_transparent_surface(img, size, scale=True):
    '''
    Creates a transparent surface containing a given image. Useful for rotating images.

    :param img: image/surface to be placed into the transparent surface
    :param size: rectangle containing the size of the surface
    :param scale: whether the image should be scaled to the surface. default true
    :return:    new surface object with a transparent color map
    '''
    img_surf = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
    if (scale):
        img = pygame.transform.scale(img, (size[0], size[1]))
    img_surf.blit(img, [0, 0])
    return img_surf


def get_line_equ(p1, p2):
    '''
    Get the equation of a line in the form y=mx+b.

    :param p1:
    :param p2:
    :return: Tuple with (m, b)
    '''
    # vertical line
    if (abs(p2[0] - p1[0]) < 0.001):
        m = math.inf
        b = p2[0]
    else:
        m = round((p2[1] - p1[1]) / (p2[0] - p1[0]))
        b = p1[1] - m * p1[0]

    return (m, round(b))


def line_intersect_point(line1, line2):
    '''
    Finds the intersection of two lines.

    :param line1:
    :param line2:
    :return:
    '''
    # parallel
    if (abs(line1[0] - line2[0]) < 0.001 or line1[0] == line2[0]):
        # no intersect
        if (abs(line1[1] - line2[1]) < 0.001):
            return None
        # same line
        else:
            return math.inf, math.inf
    else:
        # vertical line
        if (line1[0] == math.inf):
            interX = line1[1]
            interY = line2[0] * interX + line2[1]
        elif (line2[0] == math.inf):
            interX = line2[1]
            interY = line1[0] * interX + line1[1]
        else:
            interX = (line2[1] - line1[1]) / (line1[0] - line2[0])
            interY = line1[0] * interX + line1[1]

        return round(interX), round(interY)


def between_nums(num1, num2, num_between, inclusive=(False, False)):
    '''
    Check if a number is betwen two other numbers
    :param inclusive:
    :param num1:
    :param num2:
    :param num_between:
    :return:
    '''
    if (inclusive[0]):
        if (not min(num1, num2) <= num_between):
            # print(num1, num2, num_between, False, inclusive)
            return False
    else:
        if (not min(num1, num2) < num_between):
            # print(num1, num2, num_between, False, inclusive)
            return False
    if (inclusive[1]):
        if (not num_between <= max(num1, num2)):
            # print(num1, num2, num_between, False, inclusive)
            return False
    else:
        if (not num_between < max(num1, num2)):
            # print(num1, num2, num_between, False, inclusive)
            return False
    # if(min(num1,num2) <= num_between <= max(num1,num2)):
    #     return True
    # print(num1, num2, num_between, True, inclusive)
    return True


def between_points(point1, point2, point_between, inclusive=(False, False)):
    '''
    Check if a point is between two other points
    :param inclusive:
    :param point1:
    :param point2:
    :param point_between:
    :return:
    '''
    # check x value
    if (not between_nums(point1[0], point2[0], point_between[0], (inclusive[0],inclusive[0]))):
        return False
    # check x value
    if (not between_nums(point1[1], point2[1], point_between[1], (inclusive[1],inclusive[1]))):
        return False
    return True


def line_segment_intersect_point(line_seg1, line_seg2, inclusive=(False, False)):
    '''
    Finds if 2 line segments intersect
    :param inclusive:
    :param line_seg1:
    :param line_seg2:
    :return:
    '''

    # get intersection point of the lines
    inter_point = line_intersect_point(line_seg1[0], line_seg2[0])
    # print(inter_point)
    # parallel lines
    if (inter_point is None):
        return False, inter_point
    if (inter_point == math.inf):
        return True, inter_point
    # check the point is on both line segments

    # line seg 1
    if (not (between_points(line_seg1[1], line_seg1[2], inter_point, (inclusive[0],inclusive[0])))):
        return False, inter_point

    # if(not(min(line_seg1[1][0], line_seg1[2][0]) < inter_point[0] < max(line_seg1[1][0], line_seg1[2][0]))):
    #     return False, inter_point
    # if(not (min(line_seg1[1][1], line_seg1[2][1]) < inter_point[1] < max(line_seg1[1][1],line_seg1[2][1]))):
    #     return False, inter_point

    # line seg 2
    if (not (between_points(line_seg2[1], line_seg2[2], inter_point, (inclusive[1],inclusive[1])))):
        return False, inter_point
    # if(not(min(line_seg2[1][0], line_seg2[2][0]) < inter_point[0] < max(line_seg2[1][0], line_seg2[2][0]))):
    #     # return False, inter_point
    #     if(not (min(line_seg2[1][1], line_seg2[2][1]) < inter_point[1] < max(line_seg2[1][1],line_seg2[2][1]))):
    #         return False, inter_point
    return True, inter_point

def get_point_angle(p1, p2, rad = True):
    angle = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    if(rad == False):
        angle = math.degrees(angle)
    return angle

# print(between_nums(0,0,0))
# print(between_nums(50,50,50))