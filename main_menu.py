import pygame
import pygame_gui
import os
from Settings import settings_main

pygame.init()
path = os.path.dirname(os.path.abspath(__file__))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption('Dino Game')
screen = pygame.display.set_mode((1200, 800))

manager = pygame_gui.UIManager((1200, 800))
font = pygame.font.Font(None, 36)


play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 170), (100, 50)),
                                            text='Play',
                                            manager=manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 230), (100, 50)),
                                           text="Shop",
                                           manager=manager)


clock = pygame.time.Clock()
is_running = True
run = False
def main_menu():
    global run, is_running, mute
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    run = True
                    is_running = False
                    
                if event.ui_element == settings_button:
                    settings_main(screen, True)


            manager.process_events(event)
        
        manager.update(time_delta)

        screen.fill(WHITE)
        manager.draw_ui(screen)

        pygame.display.update()
    
    return run
    

if __name__ == "__main__":
    main_menu()
    