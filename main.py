# http://kidscancode.org/blog/
# stackoverflow.com(specifically looking for how to constantly   spawn enemies, still looking for something that works though)
# Mr. Cozort (for the main/game base files)
# Samuel Lin (for telling me how to make enemies that fall down respawn)


# imports libraries and modules
# from platform import platform
import os
from multiprocessing.resource_sharer import stop
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from pygame import mixer

Path = "C:\github\BCPProgrammingClass\introToProgrammingFinalProject\sounds"
os.chdir(Path)

pg.mixer.init()
vec = pg.math.Vector2


#sounds & music

mixer.music.load('music.wav')
mixer.music.set_volume(0.2)
mixer.music.play()
laser = mixer.Sound('laser.wav')
health = mixer.Sound('health.wav')
beep = mixer.Sound('beep.wav')
explosion = mixer.Sound('explosion.wav')
crash = mixer.Sound('crash.wav')

# game settings 
WIDTH = 1000
HEIGHT = 750    
FPS = 30


# player settings
PLAYER_GRAV = 0
PLAYER_FRIC = 6
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# allows for text to actually be displayed on screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Times New Roman')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# important for random colors
def colorbyte():
    return random.randint(0,255)

# creates the player sprite and gives it controls
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.acc.y = -2.5
        if keys[pg.K_a]:
            self.acc.x = -2.5
        if keys[pg.K_s]:
            self.acc.y = 2.5
        if keys[pg.K_d]:
            self.acc.x = 2.5

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.3
        self.acc.y += self.vel.y * -0.3
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos

        # added borders for the game so that the sprite won't fly off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 750:
            self.rect.bottom = 750
        if SCORE >= 100:
            self.vel.y += 1.75

class Bullet(pg.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pg.Surface([4, 10])
        self.image.fill(WHITE)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 15
 


class Block(pg.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pg.Surface([30, 30])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.rect.y = 0
        if SCORE >= 100:
            self.rect.y += 3
        if SCORE >= 200:
            self.rect.y += 5
        if SCORE >= 300:
            self.rect.y += 7



        
# powerups might be added later for the final project as well as bullets. 
#class Mob(Powerup):
#    def __init__(self, x, y, w, h, color):
#        Sprite.__init__(self)
#        self.color = color
#        self.image = pg.Surface((w, h))
#        self.image.fill(RED)
#        self.rect = self.image.get_rect()
#        self.rect.x = x
#        self.rect.y = y
#    def update(self):
#        self.rect.y += 1


        
# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
    

# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
# List of each block in the game
block_list = pg.sprite.Group()
# instantiate classes
player = Player()
# List of each bullet
bullet_list = pg.sprite.Group()


# spawns in mobs

for i in range(50):
    # This represents a block
    block = Block(BLUE)
 
    # Set a random location for the block
    block.rect.x = random.randrange(WIDTH)
    block.rect.y = random.randrange(750)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites.add(block)

all_sprites.update()
all_sprites.draw(screen)


# add player to all sprites group
all_sprites.add(player)



# Game loop
start_ticks = pg.time.get_ticks()
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        # print("ive struck a plat")
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
 
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites.add(bullet)
            bullet_list.add(bullet)
            laser.play()
     # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See if it hit a block
        block_hit_list = pg.sprite.spritecollide(bullet, block_list, True)
 
        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites.remove(bullet)
            SCORE += 10
            print(SCORE)
            crash.play()
 
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites.remove(bullet)
 
    
# makes it if the sprite hits 20 asteroids, it "dies"
    mobhits = pg.sprite.spritecollide(player, block_list, True)
    if mobhits:
        print("ive struck an asteroid")
        player.health -= 20
        explosion.play()


    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
    

    if player.health == 0:
        draw_text == "you died"
        draw_text == "your final score was:"


    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
 

    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw text

    # Player Health screen that stops showing if the health is 0 or less
    if player.health > 0:
        draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)

    # draw all sprites
    all_sprites.draw(screen)

 

    # death screen that stays hidden until the health is 0 or less
    if player.health <= 0:
        draw_text("YOU HAVE DIED", 40, RED, WIDTH / 2, HEIGHT / 10)
        pg.quit
        stop

    if int(SCORE) >= 500:
        draw_text("PERFECT SCORE - YOU WON!", 40, BLUE, WIDTH / 2, HEIGHT / 3)
    if int(SCORE) == 100:
        draw_text("THE ASTEROIDS HAVE PICKED UP SPEED", 20, RED, WIDTH / 2, HEIGHT / 5)
    
    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()