import pygame
from tank import *
from map import *
from bullet import *
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
    if (pygame.joystick.get_count() > 1):
        controller_conected2 = True
        controller2 = pygame.joystick.Joystick(1)
        controller2.init()
# print('controller_conected1 = ' + str(controller_conected1))
# print('controller_conected2 = ' + str(controller_conected2))
# print('controller1 = ' + str(controller1))
# print('controller2 = ' + str(controller2))

WIN_WIDTH = 600
WIN_HEIGHT = 600
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BG_COLOR = pygame.color.Color('0x505050')

clock = pygame.time.Clock()
FPS = 60

map = Map((50,50,500,500))
player1 = Player(1, (100, 275, 50, 50), [(100, 175, 255),  (25, 100, 255)], map,
               {pygame.K_d: 'BODY RIGHT',
                pygame.K_s: 'BODY DOWN',
                pygame.K_a: 'BODY LEFT',
                pygame.K_w: 'BODY UP'}
               )
map.player1 = player1

player2 = Player(2, (450, 275, 50, 50), [(255, 100, 100), (255, 25, 25)],  map,
               {pygame.K_RIGHT: 'BODY RIGHT',
                pygame.K_DOWN: 'BODY DOWN',
                pygame.K_LEFT: 'BODY LEFT',
                pygame.K_UP: 'BODY UP'
                }
               )
map.player2 = player2


bullet = Bullet((250, 250), map, 5, 80)
map.bullet_lst.append(bullet)


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

    # player1.update(kb_inputs=keys, controller_inputs=controller1_buttons)
    # player2.update(kb_inputs=keys, controller_inputs=controller2_buttons)
    map.update(kb_inputs=keys, controller_inputs1=controller1_buttons, controller_inputs2=controller2_buttons)

    #_____Draw_____
    window.fill(BG_COLOR)
    map.draw(window)
    # bullet.draw(window)
    # player1.draw(window)
    # player2.draw(window)

    pygame.display.flip()
    clock.tick(FPS)

