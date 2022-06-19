import pygame

class Animation():
    def __init__(self, frames, frame_duration, loop=0):
        self.frames = frames
        self.frame_duration=frame_duration
        self.loop = loop
        self.complete=False

        self.timer = 0
        self.timer_lim = self.frame_duration * len(self.frames)

    def animate(self, surface, image, position):
        # some transformations on image
        if(not self.complete):
            self.draw_frame(surface, image, position)
            self.timer=self.timer+1

        if(self.timer>=self.timer_lim):
            self.timer=0
            self.loop = self.loop - 1
            if(self.loop == 0):
                self.complete=True

    def draw_frame(surface, image, position):
        # some transformations on image
        surface.blit(image, position)

class MoveAnimation(Animation):
    def __init__(self, frames, frame_duration, x_y=None, loop=0):
        self.x_y = x_y
        super().__init__(frames, frame_duration, loop)

    def draw_frame(self, surface, image, position):
        # some transformations on image
        current_frame = self.frames[self.timer // self.frame_duration]
        if(self.x_y == 'x'):
            surface.blit(image, (position[0] + current_frame, position[1]))
        elif(self.x_y == 'y'):
            surface.blit(image, (position[0], position[1] + current_frame))
        else:
            surface.blit(image, (position[0] + current_frame[0], position[1] + current_frame[1]))

class ScaleAnimation(Animation):
    def __init__(self, frames, frame_duration, center=(), x_y=None, loop=0):
        self.x_y = x_y
        self.center = center
        super().__init__(frames, frame_duration, loop)

    def draw_frame(self, surface, image, position):
        # some transformations on image
        current_frame = self.frames[self.timer // self.frame_duration]
        if (self.x_y == 'x'):
            scaled_img = pygame.transform.scale(image, (current_frame, image.get_height()))
        elif (self.x_y == 'y'):
            scaled_img = pygame.transform.scale(image, (image.get_width(), current_frame))
        else:
            scaled_img = pygame.transform.scale(image, (current_frame, current_frame))

        draw_postion = [position[0], position[1]]
        if(len(self.center)==2):
            draw_postion[0] = draw_postion[0] + ((self.center[0] - draw_postion[0]) - scaled_img.get_width()//2)
            draw_postion[1] = draw_postion[1] + ((self.center[1] - draw_postion[1]) - scaled_img.get_height()//2)
        surface.blit(scaled_img, draw_postion)

class RotateAnimation(Animation):
    def __init__(self, frames,frame_duration,center=(), rotation_center=(), loop=0):
        self.center = center
        self.rotation_center = rotation_center
        super().__init__(frames, frame_duration, loop)

    def draw_frame(self, surface, image, position):
        # some transformations on image

        current_frame = self.frames[self.timer // self.frame_duration]
        rotated_img = pygame.transform.rotate(image, current_frame)

        draw_postion = [position[0], position[1]]
        if (len(self.center) == 2):
            draw_postion[0] = draw_postion[0] + ((self.center[0] - draw_postion[0]) - rotated_img.get_width() // 2)
            draw_postion[1] = draw_postion[1] + ((self.center[1] - draw_postion[1]) - rotated_img.get_height() // 2)
        surface.blit(rotated_img, draw_postion)
