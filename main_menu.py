import pygame
import pygame_gui

pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
manager = pygame_gui.UIManager((1200, 400))
window_surface = pygame.display.set_mode((1200, 400))
pygame.display.set_caption('Main Menu')

WHITE = (255, 255, 255)

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 170), (100, 50)),
                                            text='Play',
                                            manager=manager)

shop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 230), (100, 50)),
                                           text="Shop",
                                           manager=manager)

is_running = True
start_game = False
def main_menu():
    global start_game, is_running
    while is_running:
        time_delta = clock.tick(60)/1000.0
        clock.tick(fps)
        screen.fill(WHITE)
         
        for event in pygame.event.get():                     
            if event.type == pygame.QUIT:
                is_running = False            
            if event.type == pygame.KEYDOWN:
                if pygame.K_SPACE:
                    start_game = True
                    is_running = False
                    
                if pygame.K_s:
                    (window_surface, True)
                            

            manager.process_events(event)
            
        manager.update(time_delta)

        window_surface.fill(WHITE)
        manager.draw_ui(window_surface)
        
        pygame.display.update()
    pygame.quit()
main_menu()