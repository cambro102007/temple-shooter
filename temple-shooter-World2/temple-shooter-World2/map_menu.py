import pygame
import pygame_gui
import os

pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


World_1 = True
fps = 60
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((1200, 800))

pygame.init()
path = os.path.dirname(os.path.abspath(__file__))

pygame.display.set_caption('Shrine Of Explosions™')

manager = pygame_gui.UIManager((1200, 800))
font = pygame.font.Font(None, 72)

MAP1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((515, 300), (200, 100)),
                                            text='MAP 1',
                                            manager=manager)

MAP2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((515, 500), (200, 100)),
                                           text="MAP 2",
                                           manager=manager)

def draw_title():
    font = pygame.font.Font(None, 72)
    text = font.render('Select A Map', True, BLACK)
    screen.blit(text, (360, 100))

is_runing = True
run = False
def map_main(screen, run):
    while run:
        time_delta = clock.tick(60)/1000.0
        clock.tick(fps)
        screen.fill(WHITE)
        draw_title()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == MAP1_button:
                    World_1 = True
                    run = True
                    is_runing = False
                
                if event.ui_element == MAP2_button:
                    World_1 = False
                    run = True
                    is_runing = False

            manager.process_events(event)
        
        manager.update(time_delta) 
        
        
        screen.fill(WHITE)
        manager.draw_ui(screen)
        pygame.display.update()
    
    return is_runing, run

if __name__ == "__main__":
    map_main()