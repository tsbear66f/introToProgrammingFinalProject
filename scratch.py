"""
 Show how to fire bullets.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/PpdJjaiLX6A
"""
import pygame
import random
from multiprocessing.resource_sharer import stop

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SCORE = WIDTH = 1000
HEIGHT = 750  
 
# allows for text to actually be displayed on screen
def draw_text(text, size, color, x, y):
        font_name = pygame.font.match_font('Arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# --- Classes
 
 
class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([30, 30])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect()
        self.health = 100
 
    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
 
        # Set the player x position to the mouse x position
        self.rect.x = pos[0]
 
 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 10
 
 
# --- Create the window
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
 
# --- Sprite lists
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
block_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()
 
# --- Create the sprites
 
for i in range(50):
    # This represents a block
    block = Block(BLUE)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(500)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a red player block
player = Player()
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
player.rect.y = 500
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
 
    # --- Game logic
 
    # Call the update() method on all the sprites
    all_sprites_list.update()
 
    # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
 
        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)
 
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
 
    # --- Draw a frame
 
    # Clear the screen
    screen.fill(WHITE)
 
    # Draw all the sprites
    all_sprites_list.draw(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 20 frames per second
    clock.tick(60)
mobhits = pygame.sprite.spritecollide(player, block_list, True)
if mobhits:
        print("ive struck an asteroid")
        player.health -= 20

for event in pygame.event.get():
        # check for closed window
        if event.type == pygame.QUIT:
            running = False
        # check for mouse

if player.health == 0:
        draw_text == "you died"
        draw_text == "your final score was:"


for event in pygame.event.get():
        # check for closed window
        if event.type == pygame.QUIT:
            running = False
 

    ############ Update ##############
    # update all sprites
all_sprites_list.update()

    ############ Draw ################
    # draw the background screen
screen.fill(BLACK)
    # draw text

    # Player Health screen that stops showing if the health is 0 or less
if player.health > 0:
        draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    # draw all sprites
all_sprites_list.draw(screen)

draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)

    # death screen that stays hidden until the health is 0 or less
if player.health <= 0:
        draw_text("YOU HAVE DIED", 40, RED, WIDTH / 2, HEIGHT / 10)
        pygame.quit
        stop

if int(SCORE) >= 100:
        draw_text("YOU WON!", 40, BLUE, WIDTH / 2, HEIGHT / 3)
        pygame.quit
        stop
    # buffer - after drawing everything, flip display
pygame.display.flip()

pygame.quit()
 
pygame.quit()