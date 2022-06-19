import pygame
from tank import *
from map import *
from controller_mappings import *

run=True

pygame.init()
pygame.font.init()

pygame.joystick.init()
controller_conected1 = False
controller_conected2 = False
controller1 = None
controller2 = None
if(pygame.joystick.get_count() > 0):
    controller_conected1 = True
    controller1 = pygame.joystick.Joystick(0)
    controller1.init()
    print('test')
    if (pygame.joystick.get_count() > 1):
        controller_conected2 = True
        controller2 = pygame.joystick.Joystick(1)
        controller2.init()
print('controller_conected1 = ' + str(controller_conected1))
print('controller_conected2 = ' + str(controller_conected2))
print('controller1 = ' + str(controller1))
print('controller2 = ' + str(controller2))

WIN_WIDTH = 600
WIN_HEIGHT = 600
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BG_COLOR = pygame.color.Color('0x505050')

clock = pygame.time.Clock()
FPS = 60

map = Map((50,50,500,500))
player1 = Tank((100, 275, 50, 50), map, (100, 175, 255), 1,
               {pygame.K_d: 'RIGHT',
                pygame.K_s: 'DOWN',
                pygame.K_a: 'LEFT',
                pygame.K_w: 'UP'}
               )
player2 = Tank((450, 275, 50, 50), map, (255, 100, 100), 2,
               {pygame.K_RIGHT: 'RIGHT',
                pygame.K_DOWN: 'DOWN',
                pygame.K_LEFT: 'LEFT',
                pygame.K_UP: 'UP'
                }
               )
#todo
# add second controllable player
# can be controlled through any means



while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if (controller_conected1):
        controller1_buttons = controller1
    else:
        controller1_buttons = None
    if (controller_conected2):
        controller2_buttons = controller2
    else:
        controller2_buttons = None

    player1.update(kb_inputs=keys, controller_inputs=controller1_buttons)
    player2.update(kb_inputs=keys, controller_inputs=controller2_buttons)

    #_____Draw_____
    window.fill(BG_COLOR)
    map.draw(window)
    player1.draw(window)
    player2.draw(window)

    pygame.display.flip()
    clock.tick(FPS)
