
import pygame
import os

# need this for resizing images
def ratio(img_size, width, height):
    r = height/width
    return int(r*img_size)

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        # initialize variables
        new_img_width = 50
        self.image = pygame.image.load(os.path.join('images/lava', "lava.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (new_img_width, ratio(new_img_width, self.image.get_width(), self.image.get_height())))
        self.rect = self.image.get_rect()
        self.xpos = x
        self.rect.x, self.rect.y = 0, 600 - y
    
    # update position on screen
    def move(self, scrollx):
        self.rect.x = scrollx + self.xpos