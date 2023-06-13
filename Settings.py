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
    screen.blit(text, (234, 225))
    text = font.render('B', True, BLACK)
    screen.blit(text, (233, 350))
    text = font.render('SPACE', True, BLACK)
    screen.blit(text, (190, 475))  
    text = font.render('G', True, BLACK)
    screen.blit(text, (231, 600))  

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
    text = font.render('S', True, BLACK)
    screen.blit(text, (934, 230))
    text = font.render('N', True, BLACK)
    screen.blit(text, (931, 350))
    text = font.render('M', True, BLACK)
    screen.blit(text, (929, 475))
    text = font.render('G', True, BLACK)
    screen.blit(text, (929, 600)) 

def draw_controls(screen):
    font = pygame.font.Font(None, 48)
    text = font.render('CONTROLS', True, BLACK)
    screen.blit(text, (500, 50))
    text = font.render('Move', True, BLACK)
    screen.blit(text, (550, 175))
    text = font.render('Loot', True, BLACK)
    screen.blit(text, (555, 350))
    text = font.render('Shoot', True, BLACK)
    screen.blit(text, (545, 475))
    text = font.render('Restart', True, BLACK)
    screen.blit(text, (535, 600))  

run = True
def settings_main(screen, run):
    while run:
        clock.tick(fps)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run

        P1_draw_controls(screen)
        draw_controls(screen)
        P2_draw_controls(screen)
        pygame.display.update()
    return run

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Call settings_main function
settings_main(screen, run)