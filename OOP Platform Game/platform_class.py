import pygame
import os

# need this for resizing images
def ratio(img_size, width, height):
    r = height/width
    return int(r*img_size)

class Platform(pygame.sprite.Sprite):
    
    # initialize variables
    def __init__(self, x, y, img_file) -> None:
        super().__init__()

        # the ground
        if img_file == 'ground.png':
            new_img_width = 1000
        #the platforms
        elif img_file == 'basic_plat.png':
            new_img_width = 100
        else:
            new_img_width = 500

        # set image and scale it, initialize the rectangle and position
        self.image = pygame.image.load(os.path.join('images/platforms', img_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (new_img_width, ratio(new_img_width, self.image.get_width(), self.image.get_height())))
        self.rect = self.image.get_rect()
        self.rect.y = 600 - y
        self.rect.x = 0
        self.xpos = x

    # change location based on scrollx
    def move(self, scrollx):
        self.rect.x = scrollx + self.xpos