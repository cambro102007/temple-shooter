import pygame
import pygame_gui
import os
from Settings import settings_main
from map_menu import map_main


pygame.init()
path = os.path.dirname(os.path.abspath(__file__))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption('Shrine Of Explosions™')
screen = pygame.display.set_mode((1200, 800))

manager = pygame_gui.UIManager((1200, 800))
font = pygame.font.Font(None, 72)


play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((515, 300), (200, 100)),
                                            text='Play',
                                            manager=manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((515, 500), (200, 100)),
                                           text="Settings",
                                           manager=manager)

def draw_title():
    font = pygame.font.Font(None, 72)
    text = font.render('Shrine Of Explosions™', True, BLACK)
    screen.blit(text, (360, 100))

def titles():
    font = pygame.font.Font(None, 48)
    text = font.render('SPACE OR CLICK', True, BLACK)
    screen.blit(text, (477, 400))
    text = font.render('S OR CLICK', True, BLACK)
    screen.blit(text, (518, 600))

clock = pygame.time.Clock()
is_running = True
run = False
def main_menu():
    global run, is_running
    key = pygame.key.get_pressed()
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                exit()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    map_main(screen, True)
                    
                if event.ui_element == settings_button:
                    settings_main(screen, True)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings_main(screen, True)

                if event.key == pygame.K_SPACE:
                    run = True
                    is_running = False
            
            manager.process_events(event)
        
        manager.update(time_delta)

        screen.fill(WHITE)
        manager.draw_ui(screen)
        draw_title()
        titles()
        pygame.display.update()
    
    return run
    

if __name__ == "__main__":
    main_menu()
    
