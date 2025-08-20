'''
On our honor we have neither given nor recieved unauthorized aid
Celeste van Dokkum
Isabella Wu
Dylan Hsueh
'''

# modules
import pygame
from pygame.locals import *
import os
import sys
from player_class import Player
from platform_class import Platform
from lava_class import Lava
from npc_class import Character

# setup
pygame.display.set_caption("Fox's Birthday Game")
pygame.init()
clock = pygame.time.Clock()
screenwidth, screenheight = (1000, 600)
screen = pygame.display.set_mode((screenwidth, screenheight))
main = True
scrollx = 0
lives = 5
tea_collected = 0
check_point = 0

# bg image
backdrop = pygame.image.load(os.path.join('images', 'Purplesky.JPG'))
width = int(900 * (backdrop.get_width() / backdrop.get_height()))
backdrop = pygame.transform.scale(backdrop, (width, 600))
backdropbox = screen.get_rect()

# makes a dictionary of objs which are used to access the objects easily
# and makes a set of objects which pygame uses to draw them on the screen
# ground and platforms are different so we could change which was on top
platforms = {}
ground_list = pygame.sprite.Group()
plat_list = pygame.sprite.Group()

# functions here are just to organize, not for efficiency
def create_platforms():
    # x y coords of each platform, each extend statement was to organize platforms into groups
    platform_locations = [[1300, 550], [1700, 170], [2000, 200], [2300,230], [2300, 750]]
    platform_locations.extend([[2600 + i*100, 250] for i in range(4)])
    platform_locations.extend([[2600 + i*100, 750] for i in range(4)])
    platform_locations.extend([[3100, 160], [3300, 300], [3700, 150]])

    # add all the platforms to the dictionary and set
    for i in range(len(platform_locations)):
        obj = Platform(platform_locations[i][0], platform_locations[i][1], 'basic_plat.png')
        platforms['plat' + str(i)] = obj
        plat_list.add(obj)

    # same, but this one used a different image
    obj = Platform(3800, 350, 'long_plat.png')
    platforms['special_plat'] = obj
    plat_list.add(obj)

    # same but for all the ground pieces
    for i in range(5):
        obj = Platform(0 + screenwidth * i, 100, 'ground.png')
        platforms['main' + str(i)] = obj
        ground_list.add(obj)

# very similar to the above strategy for creating objects but for lava
lavas = {}
lava_list = pygame.sprite.Group()
def create_lava():
    # x and y coords for the lava with extend used to seperate groups
    lava_locations = [[900, 120], [1000, 120], [1300, 220], [1350, 220]]
    lava_locations.extend([[1650 + i*50, 120] for i in range(19)])
    lava_locations.extend([[2300, 415], [2350, 415]])
    lava_locations.extend([[2600 + i*50, 450] for i in range(8)])
    lava_locations.extend([[3000 + i*50, 120] for i in range(6)])
    lava_locations.extend([[3250, 120 + i*50] for i in range(4)])
    lava_locations.extend([[3400 + i*50, 120] for i in range(6)])
    lava_locations.extend([[4000 + i*100, 120] for i in range(2)])

    # add em all to the dictionary and set
    for i in range(len(lava_locations)):
        obj = Lava(lava_locations[i][0], lava_locations[i][1])
        lavas['lava' + str(i)] = obj
        lava_list.add(obj)

# same strategy for the most part
characters = {}
character_list = pygame.sprite.Group()
def create_characters():
    # x y coords for everything else
    character_locations = [[300, 300], [1940, 360], [3240, 420], [4310, 360], [4400, 520]]
    character_locations.extend([[1500,300], [3135, 230], [4000, 450]]) #boba
    
    # you can kind of see through the img names what these are. It's all the extra stuff from boba to the party scene at the end.
    # the coding was really similar for all these things so we decided to combine them.
    img_files = ['text.png', 'Unicorn.png', 'Snake.png', 'Party.png', 'thanks.png', 'greenboba.png', 'orangeboba.png', 'pinkboba.png']
    keys_for_chars = ['text','unicorn','snake','party', 'thanks', 'boba1', 'boba2', 'boba3']

    # adds them to the set and dictionary
    for i in range(len(character_locations)):
        obj = Character(character_locations[i][0], character_locations[i][1], img_files[i])
        character_list.add(obj)
        characters[keys_for_chars[i]] = obj

# execute all the above functions to create all of the objects
create_characters()
create_platforms()
create_lava()

# used for displaying text that changed
def display_text(words, x, y, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(words, True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (x, 600 - y)
    return text, textRect

# calculates how many boba the player has collected
def calc_boba_collected():
    count = 0
    for name, obj in characters.items():
        if name[:4] == 'boba':
            if obj.invited == True:
                count += 1
    return count

# figures out what to display at the end. this function and the one above are to keep
# the main loop organized
def calc_score(boba_count):
    if boba_count == 3:
        score = 'that\'s a perfect score!'
    elif boba_count == 2:
        score = 'Not bad! Only missed one!'
    elif boba_count == 1:
        score = 'hmm, there\'s room for improvement :)'
    else:
        score = 'You missed all the bubble teas! D\':'
    return score

# updates platform location, lava location and character location on screen. Also checked if
# player was touching the unicorn, snake or boba
def update_all():
    for name, platform in platforms.items():
        platform.move(scrollx)
    for name, lava in lavas.items():
        lava.move(scrollx)
    for name, character in characters.items():
        character.move(scrollx)
        character.check_invited(name, player)

# checks for player touching platforms
def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

# moves player in opposite direction if there is a collision moving horizontally
def move(rect, velocity, tiles):
    rect.x += velocity[0]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if velocity[0] > 0:
            rect.right = tile.rect.left
            player.xvel = 0
        elif velocity[0] < 0:
            rect.left = tile.rect.right
            player.xvel = 0
    return rect

# checks for collision vertically 
def check_collision() -> object:
    for platform in platforms.values():
        if player.rect.colliderect(platform.rect):
            if player.yvel > 0:
                player.rect.top = platform.rect.bottom
            if player.yvel <= 0:
                player.rect.bottom >= platform.rect.top
                return True
    return False

# check if touching lava
def touching_lava():
    for lava in lavas.values():
        if player.rect.colliderect(lava.rect):
            return True
    return False

# set new checkpoints based on scrollx
def set_checkpoint():
    base_height = 430
    i = 0
    check_list = [[0, base_height], [-770, base_height], [-1785, 306], [-2400, 300], [-3170, 386], [-4700, 300]]
    for i in range(len(check_list)):
        if scrollx > check_list[i][0]:
            j = i
            break
    return check_list[j - 1]

# initializes and adds player to a list of things to be drawn
player_list = pygame.sprite.Group()
player = Player()
player_list.add(player)


# game over function
def game_over(lives, boba_count):
    if lives <= 0:
        temp_scroll = []
        temp_scroll.append(scrollx)
        scrollx = temp_scroll[0]
        screen.fill((0,0,0))
        # game over text
        texts = display_text("GAME OVER :(", 500, 300, 100)
        screen.blit(texts[0], texts[1])
        texts = display_text("Press space to start over!", 500, 200, 30)
        screen.blit(texts[0], texts[1])
        texts = display_text("You collected {} boba!".format(boba_count), 500, 200, 30)
        screen.blit(texts[0], texts[1])

        # restart when space pressed
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            lives = 5
            # reset bubble tea & unicorn & snake
            for i in characters.values():
                i.invited = False
                tea_collected = 0
            death(False)
            scrollx = 0



# MAIN LOOP
while main:
    # draw background with lives counter
    screen.blit(backdrop, backdropbox)
    texts = display_text('lives: ' + str(lives), 75, 575, 30)
    screen.blit(texts[0], texts[1])

    # draws your score at the end
    texts = display_text('Your score: ' + str(calc_boba_collected()) + '/3 bubble teas collected!', 4650 + scrollx, 420, 30)
    screen.blit(texts[0], texts[1])
    texts = display_text(calc_score(calc_boba_collected()), 4650 + scrollx, 370, 30)
    screen.blit(texts[0], texts[1])

    # check for player input
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player.move('left', scrollx)
    if keys[K_RIGHT]:
        player.move('right', scrollx)
    if keys[K_UP]:
        player.jump()

    # respawn at last checkpoint
    def death(check):
        player.xvel, player.yvel = 0, 0
        player.rect.y = set_checkpoint()[1]
        if check == True:
            scrollx = set_checkpoint()[0]
        else:
            scrollx = 0
        return scrollx

    # player death
    if touching_lava():
        scrollx = death(True)
        lives -= 1

    # if player falls of the world, respawn. shouldn't really happen but sometimes the player glitches through the floor D:
    if player.rect.y > 700:
        scrollx = death(True)

    # adds friction
    player.friction()
    # animates fox
    player.check_costume()
    
    # updates platform location, lava location, and checks if you're touching a bubble tea,
    # snake or unicorn.
    update_all()

    # horizontal collision detection
    move(player.rect, [player.xvel, player.yvel], plat_list)

    # checks vertical collision and creates gravity if there is none
    player.gravity(check_collision())
    while check_collision():
        player.yvel = 0
        player.in_air = 0
        player.rect.y -= 1

    # scrolling effect
    scrollx += -player.xvel
    if scrollx <= -4000:
        scrollx = -4000
    if scrollx >= 0:
        scrollx = 0

    # draw everything onto the screen
    plat_list.draw(screen)
    ground_list.draw(screen)
    lava_list.draw(screen)
    character_list.draw(screen)
    player_list.draw(screen)

    # if lives
    game_over(lives)

    # update the screen
    pygame.display.flip()

    # quit program when the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(70)

'''
sources:
# https://opensource.com/article/17/12/game-python-moving-player
# https://opensource.com/article/17/12/game-python-add-a-player
# https://pastebin.com/W04srBRq
# Celeste's Codecademy subscription
# https://youtu.be/a_YTklVVNoQ
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://loughton.me.uk/public/chase_tutorial.pdf
# https://redhuli.io/creating-a-game-in-pygame-health-score-and-lives/
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
'''