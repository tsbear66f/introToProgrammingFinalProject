# http://kidscancode.org/blog/
# stackoverflow.com(specifically looking for how to constantly   spawn enemies, still looking for something that works though)
# Mr. Cozort (for the main/game base files)
# Samuel Lin (for telling me how to make enemies that fall down respawn)


# imports libraries and modules
# from platform import platform
from multiprocessing.resource_sharer import stop
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

vec = pg.math.Vector2

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
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -20
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

class Pewpew(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20
        self.owner = ""
    def update(self):
        if self.owner == "player":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if (self.rect.y < 0):
            self.kill()
            print(pewpews)


# creates the class Mobs under sprites. 
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.rect.y = 0



        
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
pewpews = pg.sprite.Group()

# instantiate classes
player = Player()


# spawns in mobs

for i in range(30):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 100, 100, (255, 255, 255))
    all_sprites.add(m)
    mobs.add(m)
    print(m)
print(mobs)

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
    
    pewpewhits = pg.sprite.groupcollide(pewpews, mobs, True, True)

# makes it if the sprite hits 20 asteroids, it "dies"
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        print("ive struck an asteroid")
        player.health -= 20

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            p = Pewpew(player.rect.midtop[0], player.rect.midtop[1], 10, 10)
            p.owner = "player"
            all_sprites.add(p)
            pewpews.add(p)
            mpos = pg.mouse.get_pos()
            print(mpos)
            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            for m in mobs:
                if m.rect.collidepoint(mpos):
                    print(m)
                    m.kill()
                    SCORE += 10
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
    # draw all sprites
    all_sprites.draw(screen)

    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)

    # death screen that stays hidden until the health is 0 or less
    if player.health <= 0:
        draw_text("YOU HAVE DIED", 40, RED, WIDTH / 2, HEIGHT / 10)
        pg.quit
        stop

    if int(SCORE) >= 100:
        draw_text("YOU WON!", 40, BLUE, WIDTH / 2, HEIGHT / 3)
        pg.quit
        stop
    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()