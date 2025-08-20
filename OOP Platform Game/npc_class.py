import pygame
import os

# need this for resizing images
def ratio(img_size, width, height):
    r = height/width
    return int(r*img_size)

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file):
        super().__init__() 

        # set sizes for each character
        self.image_file = pygame.image.load(os.path.join('images', img_file)).convert_alpha() #???
        if img_file == 'text.png':
            self.size = 300
        elif img_file == 'Party.png':
            self.size = 600
        elif img_file == 'thanks.png':
            self.size = 500
        elif img_file == 'pinkboba.png' or img_file == 'orangeboba.png' or img_file == 'greenboba.png':
            self.size = 30
        else:
            self.size = 200
        
        # initialize variables
        self.invited = False
        self.xpos = x
        self.image_file = pygame.transform.scale(self.image_file, (self.size, ratio(self.size, self.image_file.get_width(), self.image_file.get_height())))
        self.image = self.image_file
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 600 - y
    
    # update position
    def move(self, new_x):
        self.rect.x = self.xpos + new_x
    
    # check if touching the player and become invited or collect boba 
    def check_invited(self, name, player_rect):
        if self.rect.colliderect(player_rect) and self.invited == False:
            # invitation
            if name == 'snake' or name == 'unicorn':
                self.invited = True
                self.image = pygame.image.load(os.path.join('images', name + '_invited.png')).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.size, ratio(self.size, self.image.get_width(), self.image.get_height())))
            # boba collection
            if name[:4] == 'boba':
                self.invited = True
                self.image = pygame.image.load(os.path.join('images', 'blank.png')).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.size, ratio(self.size, self.image.get_width(), self.image.get_height())))
        # reset to original image when restarted basically
        elif self.invited == False:
            self.image = self.image_file
    

