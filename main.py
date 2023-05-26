import pygame
import os
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
chest_closed_img = pygame.transform.scale(chest_closed_img, (55, 35))
chest_open_img = pygame.transform.scale(chest_open_img, (55, 35))

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
        
    def update(self):
        dx= 0
        dy= 0
        walk_cooldown = 7
        
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

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_right_openchest = []
        self.images_left_openchest = []
        self.index = 0
        self.counter = 0
        self.grounded = False
        
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
        
    def update(self):
        dx= 0
        dy= 0
        walk_cooldown = 7
        
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
                col_count += 1
            row_count += 1
                
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
    
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
chest = Chest(965, 614.5, chest_closed_img, chest_open_img)         

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

         
chest2 = Chest(185, 614.5, chest_closed_img, chest_open_img)    
                   
                
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


player2 = Player2(100, screen_height - 120)
player = Player(100, screen_height - 120)
world = World(world_data)


run = True
def main():
    global run
    while run: 
        clock.tick(fps)
        screen.blit(BG_img, (0, 0))
        
        chest2.draw(screen)
        chest.draw(screen)
        world.draw()
        player.update()
        player2.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()
main()