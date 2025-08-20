import pygame
import os

# need this for resizing images
def ratio(img_size, width, height):
    r = height/width
    return int(r*img_size)

# resize an image function
def transform(img, img_size):
    return pygame.transform.scale(img, (img_size, ratio(img_size, img.get_width(), img.get_height())))


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        # player variables
        self.frame = 0
        self.speed = 4
        self.in_air = 0
        self.xvel, self.yvel = 0, 0
        self.direction = 'left'
        self.scrollx = 0

        # player walking images
        self.left_images, self.right_images = [], []
        img_size = 130
        for i in range(1, 7):
            img = pygame.image.load(os.path.join('images/fox_left', 'fox' + str(i) + '.png')).convert_alpha()
            self.left_images.append(transform(img, img_size))
        for i in range(1, 7):
            img = pygame.image.load(os.path.join('images/fox_right', 'fox' + str(i) + '.png')).convert_alpha()
            self.right_images.append(transform(img, img_size))
        
        # other imgs
        self.other_costumes = {}
        stand = pygame.image.load('stand_left.png').convert_alpha()
        self.other_costumes['stand_left'] = transform(stand, img_size)
        stand = pygame.image.load('stand_right.png').convert_alpha()
        self.other_costumes['stand_right'] = transform(stand, img_size)
        
        jumping = pygame.image.load('fox_jump.png').convert_alpha()
        self.other_costumes['jump'] = transform(jumping, 60)
            
        # set image and rectangle  
        self.image = self.left_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 100

    # set animation for the character
    def check_costume(self):
        # moving costumes (running)
        if self.xvel != 0:
            self.frame = round(self.frame + .15, 2)
        if self.xvel > 0:
            self.image = self.right_images[round(self.frame)%6]
        else:
            self.image = self.left_images[round(self.frame)%6]
        
        # still frames (standing)
        if self.xvel == 0:
            if self.direction == 'left':
                self.image = self.other_costumes['stand_left']
            else:
                self.image = self.other_costumes['stand_right']
        
        # jumping
        if self.in_air > 2:
            self.frame = round(self.frame + .15, 2)
            self.image = self.other_costumes['jump']
            self.rect.x = 520
        else:
            self.rect.x = 500

    def move(self, direction, scrollx):
        # move character and set direction for animation
        if direction == 'right': # right
            if self.direction == 'left':
                self.direction = 'right'
            if scrollx >= -4000:
                self.xvel += self.speed
        else: # left
            if self.direction == 'right':
                self.direction = 'left'
            if scrollx <= 0:
                self.xvel -= self.speed
    
    # create gravity if there's no collision
    def gravity(self, collision):
            gravityacc = .5
            if not collision:
                self.yvel = self.yvel - (gravityacc)
                self.rect.y -= self.yvel
                self.in_air += 1
            else:
                self.yvel = 0
                self.in_air = 0
                self.rect.y += 1
		
    # self explanatory
    def jump(self):
        if self.in_air < 2:
            self.yvel = 10

    # slows player to a stop
    def friction(self):
        self.xvel = self.xvel*.7
        if self.xvel < .3 and self.direction == 'right':
            self.xvel = 0
        if self.xvel > -.3 and self.direction == 'left':
            self.xvel = 0
    