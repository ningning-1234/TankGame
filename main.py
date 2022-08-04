import pygame
from tank import *
from pages import PageManager
from gamemap import *
from bullet import *
from wall import *
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

'''
map = Map((50,50,500,500))
player1 = Player(1, (100, 275, 50, 50), (100, 275, 50, 50), [(100, 175, 255),  (25, 100, 255)], map,
                 {pygame.K_d: 'BODY RIGHT',
                  pygame.K_s: 'BODY DOWN',
                  pygame.K_a: 'BODY LEFT',
                  pygame.K_w: 'BODY UP'}
                 )
map.player1 = player1
player2 = Player(2, (450, 275, 50, 50), (320, 275, 50, 50), [(255, 100, 100), (255, 25, 25)],  map,
                 {pygame.K_RIGHT: 'BODY RIGHT',
                  pygame.K_DOWN: 'BODY DOWN',
                  pygame.K_LEFT: 'BODY LEFT',
                  pygame.K_UP: 'BODY UP'}
                 )
map.player2 = player2


# bullet = Bullet((250, 250), map, 5, 0)
# map.bullet_lst.append(bullet)

block1 = Block((50, 50), 1)
map.block_lst.append(block1)
block2 = Block((200, 0), 2)
map.block_lst.append(block2)
block3 = Block((50, 150), 3)
map.block_lst.append(block3)
block4 = Block((50, 250), 2)
map.block_lst.append(block4)
'''

page_manager = PageManager(BG_COLOR)
page_manager.set_current_page(Game())

while (run):
    #_____get inputs_____
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse_inputs = {
        'mouse_btn':pygame.mouse.get_pressed(),
        # 'mouse_btn_release': pygame.mouse.get_rel(),
        'mouse_coords':pygame.mouse.get_pos()
    }

    if (controller_conected1):
        controller1_buttons = controller1
    else:
        controller1_buttons = None

    if (controller_conected2):
        controller2_buttons = controller2
    else:
        controller2_buttons = None
    #_____Update_____
    page_manager.update(kb_inputs=keys,
                        mouse_inputs=mouse_inputs,
                        controller_inputs1=controller1_buttons,
                        controller_inputs2=controller2_buttons)
    # map.update(kb_inputs=keys, controller_inputs1=controller1_buttons, controller_inputs2=controller2_buttons)

    #_____Draw_____

    page_manager.draw(window)

    # map.draw(window)
    # bullet.draw(window)
    # player1.draw(window)
    # player2.draw(window)

    pygame.display.flip()
    clock.tick(FPS)

