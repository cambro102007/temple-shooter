import pygame
import os
import sys
from pygame.locals import *

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
tile_size = 25
class Player2():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_right_openchest = []
        self.images_left_openchest = []
        self.index = 0
        self.counter = 0
        self.grounded = False
        self.direction = 0
        self.shoot2_cooldown = 0
        
        for num in range(1, 5):
            img_right = pygame.image.load(path + f"/res/images/man2_{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 75))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 5):
            img_right_openchest = pygame.image.load(path + f"/res/images/gun_man2_{num}.png")
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
        self
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.health = 100

    def update(self):
        global shoot2
        dx= 0
        dy= 0
        walk_cooldown = 7
        if dead == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_i] and not self.jumped and self.grounded:
                self.jumped = True
                self.grounded = False
                self.vel_y =- 17
            elif key[pygame.K_UP] and not self.jumped and self.grounded:
                self.jumped = True
                self.grounded = False
                self.vel_y =- 17
            if key[pygame.K_i] or key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_j] or key[pygame.K_LEFT]:
                dx -= 7
                self.counter += 1
                self.direction = -1
            if key[pygame.K_l]or key[pygame.K_RIGHT]:
                dx += 7
                self.counter += 1
                self.direction = 1
            if key[pygame.K_j] == False and key[pygame.K_l] == False and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
            if (chest.is_open and chest.opened_by == self) or (chest2.is_open and chest2.opened_by == self):
                if key[pygame.K_m]:
                    shoot2 = True


        if (chest.is_open and chest.opened_by == self) or (chest2.is_open and chest2.opened_by == self):
            if self.direction == -1:
                self.image = self.images_right_openchest[self.index]
            if self.direction == 1:
                self.image = self.images_left_openchest[self.index]
        else:
            if self.direction == -1:
                self.image = self.images_right[self.index]
            if self.direction == 1:
                self.image = self.images_left[self.index]
            
        
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == -1:
                self.image = self.images_right[self.index]
            if self.direction == 1:
                self.image = self.images_left[self.index]
        
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
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
            if key[pygame.K_n] and not chest.is_open:
                chest.open(self)
        if self.rect.colliderect(chest2.rect):
            key = pygame.key.get_pressed()
            if key[pygame.K_n] and not chest2.is_open:
                chest2.open(self)

        if self.shoot2_cooldown > 0:
            self.shoot2_cooldown -= 1
        if shoot2:
            if self.shoot2_cooldown == 0:
                self.shoot2_cooldown = 8
                bullet2 = Bullet2(player2.rect.centerx + (0.6 * player2.rect.size[0] * player2.direction), player2.rect.centery, player2.direction)
                bullet_group2.add(bullet2)

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_right_openchest = []
        self.images_left_openchest = []
        self.index = 0
        self.counter = 0
        self.grounded = False
        self.shoot_cooldown = 0
        
        for num in range(1, 5):
            img_right = pygame.image.load(path + f"/res/images/man_{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 75))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 5):
            img_right_openchest = pygame.image.load(path + f"/res/images/gun_man_{num}.png")
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
        
    def update(self):
        global shoot
        dx= 0
        dy= 0
        walk_cooldown = 7
        if dead == False:
            #KeyStrokes
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and not self.jumped and self.grounded:
                self.jumped = True
                self.grounded = False
                self.vel_y =- 17
            if key[pygame.K_w] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 7
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 7
                self.counter += 1
                self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.counter = 1
                self.index = 1
            if (chest.is_open and chest.opened_by == self) or (chest2.is_open and chest2.opened_by == self):
                if key[pygame.K_SPACE]:
                    shoot = True
          
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
            if key[pygame.K_b] and not chest.is_open:
                chest.open(self)
        if self.rect.colliderect(chest2.rect):
            key = pygame.key.get_pressed()
            if key[pygame.K_b] and not chest2.is_open:
                chest2.open(self)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if shoot:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 8
                bullet = Bullet(player.rect.centerx + (0.6 * player.rect.size[0] * player.direction), player.rect.centery, player.direction)
                bullet_group.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,  x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.colliderect(player2):
            self.kill()
            player2.health -= 15
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.kill()
bullet_group = pygame.sprite.Group()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,  x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.colliderect(player):
            self.kill()
            player.health -= 15   
        
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.kill()
bullet_group2 = pygame.sprite.Group()

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

class Chest2():
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
    global dead, bullet_group, bullet_group2, world, chest, chest2, player, player2
    dead = False
    bullet_group = pygame.sprite.Group()
    bullet_group2 = pygame.sprite.Group()
    world = World(world_data)
    chest = Chest(965, 598, chest_closed_img, chest_open_img)
    chest2 = Chest(185, 598, chest_closed_img, chest_open_img)
    player2 = Player2(650, 25)
    player = Player(530, 25)

def draw_health():
    font = pygame.font.Font(None, 48)
    text = font.render(f'Health: {player.health}', True, (255,0, 68))
    no_health = font.render('Health: 0', True, (255, 0, 68))
    
    if player.health >= 0:
        screen.blit(text, (522,680))
    else:
        screen.blit(no_health, (522,680))
        
    text2 = font.render(f'Health: {player2.health}', True, (0, 154, 255))
    no_health2 = font.render('Health: 0', True, (0, 154, 255))
    
    if player2.health >= 0:
        screen.blit(text2, (522,720))
    else:
        screen.blit(no_health2, (522,720))
    
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

player2 = Player2(650, 25)
player = Player(530, 25)
world = World(world_data)

run = True
def main():
    global run, dead, shoot, shoot2
    while run: 
        clock.tick(fps)
        screen.blit(BG_img, (0, 0))
        
        bullet_group.update()
        bullet_group.draw(screen)
        bullet_group2.update()
        bullet_group2.draw(screen)

        chest2.draw(screen)
        chest.draw(screen)
        world.draw()
        player.update()
        player2.update()
        draw_health()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_m:
                    shoot2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and dead:
                    initialize_game()
                    dead = False

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
