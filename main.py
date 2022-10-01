from engine_files.pages import *
from gamemap import Game
from menu_pages.selection_menu import *

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

page_manager = PageManager(BG_COLOR,(WIN_WIDTH, WIN_HEIGHT))

# def start_game(page_manager,**kwargs):
#     page_manager.set_current_page(Game(page_manager))
# test_page = Page('test', page_manager,True)
# test_page.add_component(PageButton((0,0,50,50),color=(50,50,120),onclick=start_game, onclick_args=[page_manager]))
# page_manager.set_current_page(test_page)
page_manager.set_current_page(TitlePage(page_manager))
# page_manager.set_current_page(Game(page_manager))

while (run):
    #_____get inputs_____
    events = pygame.event.get()
    for event in events:
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
                        controller_inputs2=controller2_buttons,
                        events=events
                        )
    # map.update(kb_inputs=keys, controller_inputs1=controller1_buttons, controller_inputs2=controller2_buttons)

    #_____Draw_____

    page_manager.draw(window)
    # print('==================================================================')
    # map.draw(window)
    # bullet.draw(window)
    # player1.draw(window)
    # player2.draw(window)

    pygame.display.flip()
    clock.tick(FPS)

