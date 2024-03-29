import pygame
import os
import sys
from pygame.locals import *
from main_menu import main_menu

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Temple shooter')

path = os.path.dirname(os.path.abspath(__file__))
BG_img = pygame.image.load(path + "/res/images/temple_BG.png")
chest_closed_img = pygame.image.load(path + "/res/images/chest_closed.png")
chest_open_img = pygame.image.load(path + "/res/images/chest_open.png")
ammo_box_img = pygame.image.load(path + "/res/images/ammo_box.png")
ak47_img = pygame.image.load(path + "/res/images/ak47.png")
bullet_img = pygame.image.load(path + "/res/images/bullet.png")
chest_closed_img = pygame.transform.scale(chest_closed_img, (82.5, 52.5))
chest_open_img = pygame.transform.scale(chest_open_img, (82.5, 52.5))

dead = False
shoot = False
shoot2 = False
knife = False
knife2 = False
tile_size = 25

class Player():
    def __init__(self, x, y, player_type, keybinds):
        self.images_right = []
        self.images_left = []
        self.images_right_openchest = []
        self.images_left_openchest = []
        self.index = 0
        self.counter = 0
        self.grounded = False
        self.shoot_cooldown = 0
        self.ammo = 0
        self.knife_cooldown = 0
        self.player_type = player_type

        for num in range(1, 5):
            img_right = pygame.image.load(path + f"/res/images/man{player_type}_{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 75))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 5):
            img_right_openchest = pygame.image.load(path + f"/res/images/gun_man{player_type}_{num}.png")
            img_right_openchest = pygame.transform.scale(img_right_openchest, (40, 75))
            img_left_openchest = pygame.transform.flip(img_right_openchest, True, False)
            self.images_right_openchest.append(img_right_openchest)
            self.images_left_openchest.append(img_left_openchest)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.health = 100
        
        # Keybinds
        self.jump = keybinds['jump']
        self.left = keybinds['left']
        self.right = keybinds['right']
        self.shoot = keybinds['shoot']
        self.knife = keybinds['knife']
        self.loot = keybinds['loot']
        
    def update(self):
        global shoot, knife
        if self.player_type == 1:
            self.player = player
            self.opposite_player = player2
            self.shot_id = shoot
            self.knife_id = knife
        else:
            self.player = player2
            self.opposite_player = player
            self.shot_id = shoot2
            self.knife_id = knife2
        dx= 0
        dy= 0
        walk_cooldown = 7
        if dead == False:
            #KeyStrokes
            key = pygame.key.get_pressed()
            if key[self.jump] and not self.jumped and self.grounded:
                self.jumped = True
                self.grounded = False
                self.vel_y =- 17
            if key[self.jump] == False:
                self.jumped = False
            if key[self.left]:
                dx -= 7       
                self.counter += 1
                self.direction = -1
            if key[self.right]:
                dx += 7
                self.counter += 1
                self.direction = 1
            if key[self.left] == False and key[self.right] == False:
                self.counter = 1
                self.index = 1
            if (chest.is_open and chest.opened_by == self) or (chest2.is_open and chest2.opened_by == self):
                if key[self.shoot]:
                    self.shot_id = True
            if self.ammo == 0:
                self.shot_id = False
            if self.rect.colliderect(self.opposite_player):
                if key[self.knife]:
                    self.knife_id = True
            if not self.rect.colliderect(self.opposite_player):
                self.knife_id = False

        if (chest.is_open and chest.opened_by == self) or (chest2.is_open and chest2.opened_by == self):
            if self.direction == 1:
                self.image = self.images_right_openchest[self.index]
            if self.direction == -1:
                self.image = self.images_left_openchest[self.index]
        else:
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
            
        #animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
        # Collisions
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.rect.top = tile[1].bottom
                    self.vel_y = 0
                    dy = 0
                elif self.vel_y >= 0:    
                    self.rect.bottom = tile[1].top
                    dy = 0
                    self.vel_y = 0
                    self.grounded = True
            
        self.rect.x += dx
        self.rect.y += dy

        
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
            self.grounded = True
        
        screen.blit(self.image, self.rect)
        
        if self.rect.colliderect(chest.rect):
            key = pygame.key.get_pressed()
            if key[self.loot] and not chest.is_open:
                chest.open(self)
                self.ammo += 50
        if self.rect.colliderect(chest2.rect):
            key = pygame.key.get_pressed()
            if key[self.loot] and not chest2.is_open:
                chest2.open(self)
                self.ammo += 50
                
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shot_id:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 8
                bullet = Bullet(self.player.rect.centerx + (0.6 * self.player.rect.size[0] * self.player.direction), self.player.rect.centery, self.player.direction, self.opposite_player)
                bullet_group.add(bullet)
                self.ammo -= 1

        if self.knife_cooldown > 0:
            self.knife_cooldown -= 1
        if self.knife_id:
            if self.knife_cooldown == 0:
                self.knife_cooldown = 20
                self.opposite_player.health -= 10

class Bullet(pygame.sprite.Sprite):
    def __init__(self,  x, y, direction, opposite_player):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.opposite_player = opposite_player
    
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.colliderect(self.opposite_player):
            self.kill()
            self.opposite_player.health -= 15
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.kill()
bullet_group = pygame.sprite.Group()

teleporter_group = pygame.sprite.Group()

class TeleporterTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, tile_size, tile_size)

class World():
    def __init__(self, data):
        self.tile_list = []

        tile_img = pygame.image.load(path + '/res/images/tile.png')
        brown_tile_img = pygame.image.load(path + '/res/images/brown_tile.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(tile_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(brown_tile_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    teleporter = TeleporterTile(col_count * tile_size, row_count * tile_size)
                    teleporter_group.add(teleporter)
                col_count += 1
            row_count += 1
                
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
   
def player_update():
    teleporter_hit = pygame.sprite.spritecollide(player, teleporter_group, False)
    if teleporter_hit:
        next_teleporter = teleporter_group.sprites()[(teleporter_group.sprites().index(teleporter_hit[0]) + 1) % len(teleporter_group.sprites())]
        player.rect.topleft = next_teleporter.rect.topleft
    
class Chest():
    def __init__(self, x, y, chest_closed_img, chest_open_img):
        self.closed_image = chest_closed_img
        self.open_image = chest_open_img
        self.image = chest_closed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_open = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def open(self, player):
        self.image = self.open_image
        self.is_open = True
        self.opened_by = player 
        
chest = Chest(965, 598, chest_closed_img, chest_open_img)         
chest2 = Chest(185, 598, chest_closed_img, chest_open_img)
                                 
def P1draw_game_over():
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 72)
    text_game_over = font_big.render("Player Two Wins!", True, (0, 155, 255))
    text_restart = font.render('Press G to Restart', True, (255, 255, 255))

    screen.blit(text_game_over, (screen_width // 3, 195))
    screen.blit(text_restart, (505, 400))

def P2draw_game_over():
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 72)
    text_game_over = font_big.render('Player One Wins!', True, (255, 0, 68))
    text_restart = font.render('Press G to Restart', True, (255, 255, 255))

    screen.blit(text_game_over, (screen_width // 3, 195))
    screen.blit(text_restart, (505, 400))

def initialize_game():
    global dead, bullet_group, world, chest, chest2, player, player2, shoot, shoot2
    dead = False
    shoot = False
    shoot2 = False
    bullet_group = pygame.sprite.Group()
    world = World(world_data)
    chest = Chest(965, 598, chest_closed_img, chest_open_img)
    chest2 = Chest(185, 598, chest_closed_img, chest_open_img)
    player2 = Player(650, 25, 2, {
        "shoot": pygame.K_m,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT,
        "jump": pygame.K_UP,
        "loot": pygame.K_DOWN,
        "knife": pygame.K_COMMA
    })
    player = Player(530, 25, 1, {
        "shoot": pygame.K_SPACE,
        "right": pygame.K_d,
        "left": pygame.K_a,
        "jump": pygame.K_w,
        "loot": pygame.K_s,
        "knife": pygame.K_c
    })
    
def draw_health():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Health: {player.health}', True, (255,0, 68))
    no_health = font.render('Health: 0', True, (255, 0, 68))
    
    if player.health >= 0:
        screen.blit(text, (482,680))
    else:
        screen.blit(no_health, (482,680))
        
    text2 = font.render(f'Health: {player2.health}', True, (0, 154, 255))
    no_health2 = font.render('Health: 0', True, (0, 154, 255))
    
    if player2.health >= 0:
        screen.blit(text2, (482,720))
    else:
        screen.blit(no_health2, (482,720))

def draw_ammo():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Ammo: {player.ammo}', True, (255, 0, 68))
    no_ammo = font.render('Ammo: 0', True, (255, 0, 68))
    
    if player.ammo >= 0:
        screen.blit(text, (625,680))
    else:
        screen.blit(no_ammo, (522,680))
    
    text = font.render(f'Ammo: {player2.ammo}', True, (0, 154, 255))
    no_ammo = font.render('Ammo: 0', True, (0, 154, 255))
    
    if player2.ammo >= 0:
        screen.blit(text, (625,720))
    else:
        screen.blit(no_ammo, (522,720))

def jump_sound():
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.load(path + '/res/sounds/cartoon_jump.mp3')
    pygame.mixer.music.play(0)
    
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]

player2 = Player(650, 25, 2, {
    "shoot": pygame.K_m,
    "right": pygame.K_RIGHT,
    "left": pygame.K_LEFT,
    "jump": pygame.K_UP,
    "loot": pygame.K_DOWN,
    "knife": pygame.K_COMMA
})
player = Player(530, 25, 1, {
    "shoot": pygame.K_SPACE,
    "right": pygame.K_d,
    "left": pygame.K_a,
    "jump": pygame.K_w,
    "loot": pygame.K_s,
    "knife": pygame.K_c
})
world = World(world_data)

run = True
def main():
    global run, dead, shoot, shoot2, knife, knife2
    while main_menu() == True: 
        clock.tick(fps)
        screen.blit(BG_img, (0, 0))
        
        bullet_group.update()
        bullet_group.draw(screen)

        chest2.draw(screen)
        chest.draw(screen)
        world.draw()
        player2.update()
        player.update()
        draw_health()
        draw_ammo()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_m:
                    shoot2 = False
                if event.key == pygame.K_c:
                    knife = False
                if event.key == pygame.K_COMMA:
                    knife2 = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and dead:
                    initialize_game()
                    dead = False

                if event.key == pygame.K_w and player.grounded:
                    jump_sound()
                    
                if event.key == pygame.K_UP and player2.grounded:
                    jump_sound()

        if player.health <= 0:
            dead = True
            P1draw_game_over()
        if player2.health <= 0:
            dead = True
            P2draw_game_over()

        if not run:
            pygame.quit()
            sys.exit() 

        
        pygame.display.update()
    pygame.quit()
main()
