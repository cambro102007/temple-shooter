import pygame
import pygame_gui

pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

fps = 60
screen_width = 1200
screen_height = 800

pygame.display.set_caption('Shrine Of Explosions™')

manager = pygame_gui.UIManager((1200, 800))

def P1_draw_controls(screen):
    font = pygame.font.Font(None, 48)
    text = font.render('Player One Settings', True, BLACK)
    screen.blit(text, (100, 50))
    text = font.render('W', True, BLACK)
    screen.blit(text, (230, 125))
    text = font.render('A', True, BLACK)
    screen.blit(text, (175, 175))
    text = font.render('D', True, BLACK)
    screen.blit(text, (291, 175))
    text = font.render('S', True, BLACK)
    screen.blit(text, (233, 350))
    text = font.render('SPACE', True, BLACK)
    screen.blit(text, (190, 475))  
    text = font.render('G', True, BLACK)
    screen.blit(text, (231, 600))
    text = font.render('C', True, BLACK)
    screen.blit(text, (231, 725)) 

def P2_draw_controls(screen):
    font = pygame.font.Font(None, 48)
    text = font.render('Player Two Settings', True, BLACK)
    screen.blit(text, (800, 50))
    text = font.render('UP', True, BLACK)
    screen.blit(text, (925, 125))
    text = font.render('LEFT', True, BLACK)
    screen.blit(text, (840, 175))
    text = font.render('RIGHT', True, BLACK)
    screen.blit(text, (970, 175))
    text = font.render('DOWN', True, BLACK)
    screen.blit(text, (888, 350))
    text = font.render('M', True, BLACK)
    screen.blit(text, (929, 475))
    text = font.render('G', True, BLACK)
    screen.blit(text, (929, 600))
    text = font.render('COMMA (,)', True, BLACK)
    screen.blit(text, (870, 725)) 

def draw_controls(screen):
    font = pygame.font.Font(None, 48)
    text = font.render('S TO EXIT', True, (255, 0, 0))
    screen.blit(text, (525, 2))
    text = font.render('CONTROLS', True, BLACK)
    screen.blit(text, (515, 50))
    text = font.render('Move', True, BLACK)
    screen.blit(text, (560, 175))
    text = font.render('Loot', True, BLACK)
    screen.blit(text, (565, 350))
    text = font.render('Shoot', True, BLACK)
    screen.blit(text, (555, 475))
    text = font.render('Restart', True, BLACK)
    screen.blit(text, (547, 600))  
    text = font.render('Knife', True, BLACK)
    screen.blit(text, (563, 725))  

back_to_death_screen = False
run = True
def settings_main(screen, run):
    
    while run:
        clock.tick(fps)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run
            key = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    run = False

        P1_draw_controls(screen)
        draw_controls(screen)
        P2_draw_controls(screen)
        pygame.display.update()
    return  back_to_death_screen, run
