# Classes, additions, 
import pygame
import random, time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
YG = (173,255,47) #(255, 255, 210)
ORANGE = (255, 165, 0)
OLIVE = (128,128,0)
PEACH = (246,176,146)


def draw_stick_figure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1 + x, y, 10, 10], 0)

    # Legs
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [x, 27 + y], 2)

    # Body
    pygame.draw.line(screen, BLUE, [5 + x, 17 + y], [5 + x, 7 + y], 2)

    # Arms
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [1 + x, 17 + y], 2)

class Stickman(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        draw_stick_figure(self.image, x, y)
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        # List of sprites we can bump against
        self.walls = None

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player position. """
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                #collide.play()
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                #collide.play()

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= HT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HT:
            self.change_y = -7
            jump.play()

    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -3

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 3

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height, color):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        #pygame.sprite.Sprite.__init__(self) -initialize parent
        super().__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height]) #blank surface to draw on, no ned if you have a graphic surface
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect() #[x, y, w, h]
        self.rect.y = y
        self.rect.x = x

# Setup
pygame.init()

# Set the width and height of the screen [width,height]
WIDTH = 700
HT = 500
size = [WIDTH, HT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Stickman Labyrinth")
# create a sprite group list
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
bump_list = pygame.sprite.Group()

# create instances of class sprite Wall
# walls
stairs = [
#stairs1
[ 160, 440, 50, 10, PURPLE],
[ 190, 410, 50, 10, BLUE],
[ 230, 380, 70, 10, YG],
#stairs2
[70, 390, 50, 10, PURPLE],
[40, 360, 50, 10, ORANGE],
[10, 330, 50, 10, PURPLE],
#stairs3
[ 330, 440, 50, 10, RED],
[ 290, 410, 50, 10, PURPLE],
[ 340, 350, 50, 10, RED],
[ 360, 320, 50, 10, YG],
[ 390, 290, 70, 10, ORANGE],
#stair4
[ 310, 260, 50, 10, OLIVE],
[ 280, 230, 50, 10, PURPLE],
[ 230, 200, 70, 10, ORANGE],
#stair5
[ 330, 440, 50, 10, RED],
[ 290, 410, 50, 10, PURPLE],
[ 360, 320, 50, 10, BLUE],
[ 390, 290, 70, 10, PURPLE],
#stair6
[ 360, 320, 50, 10, PURPLE],
[ 450, 320, 50, 10, BLUE],
[ 490, 350, 50, 10, RED],
[ 540, 380, 70, 10, PURPLE],
[ 620, 330, 50, 10, OLIVE],
[ 650, 300, 40, 10, YG],
[ 650, 410, 40, 10, PURPLE],
[ 620, 440, 50, 10, ORANGE],
#stair7
[ 580, 190, 50, 10, PURPLE],
[ 610, 160, 50, 10, YG],
[ 640, 130, 50, 10, BLUE],
# stairs8
[ 505, 220, 40, 10, PURPLE],
[ 490, 250, 80, 10, YG],
[ 560, 280, 50, 10, PEACH],
#stair9
[ 640, 50, 50, 10, PURPLE],
[ 560, 100, 50, 10, OLIVE],
[ 520, 150, 40, 10, ORANGE],
[ 470, 110, 50, 10, YG],
[ 370, 80, 50, 10, BLUE],
[ 340, 110, 50, 10, PEACH],
[ 330, 160, 50, 10, PURPLE],
[ 390, 50, 70, 10, ORANGE],
#stairs10
[ 440, 80, 50, 10, PURPLE],
[ 390, 160, 70, 10, OLIVE],
[ 530, 50, 50, 10, ORANGE],
#stairs11
[ 150, 290, 50, 10, BLUE],
[ 120, 320, 50, 10, PURPLE],
[ 180, 260, 50, 10, YG],
[ 210, 230, 50, 10, RED],
#stair12
[ 430, 440, 50, 10, PURPLE],
[ 460, 400, 50, 10, PEACH],
#stairs13
[80, 250, 40, 10, RED],
[40, 220, 50, 10, PURPLE],
[10, 190, 50, 10, OLIVE],
#stairs14
[150, 170, 50, 10, YG],
[120, 140, 50, 10, PURPLE],
[90, 110, 50, 10, ORANGE],
[60, 140, 50, 10, OLIVE],
[10, 60, 40, 10, PEACH],
#stairs15
[210, 110, 50, 10, OLIVE],
[180, 80, 50, 10, PURPLE],
[150, 50, 50, 10, PEACH],
[270, 50, 60, 10, YG],
]

walls = [
[0, 0, 10, 600, GREEN],
[40, 0, 790, 10, GREEN],
[0, 490, 790, 10, GREEN],
[690, 0, 10, 600, GREEN],
#entry portal
[10, 0, 40, 10, BLACK],
#doors
[60, 230, 20, 40, BLACK],
[120, 150, 20, 40, BLACK],
[10, 150, 20, 40, BLACK],
[490, 360, 20, 40, BLACK],
[520, 450, 20, 40, BLACK],
[150, 330, 20, 40, BLACK],
[210, 270, 20, 40, BLACK],
[420, 10, 20, 40, BLACK],
[420, 120, 20, 40, BLACK],
[420, 170, 20, 40, BLACK],
[10, 450, 20, 40, BLACK],
[10, 290, 20, 40, BLACK],
[70, 400, 20, 40, BLACK],
[260, 160, 20, 40, BLACK],
[310, 270, 20, 40, BLACK],
[370, 360, 20, 40, BLACK],
[420, 250, 20, 40, BLACK],
[570, 340, 20, 40, BLACK],
[570, 390, 20, 40, BLACK],
[670, 260, 20, 40, BLACK],
[670, 450, 20, 40, BLACK],
[260, 340, 20, 40, BLACK],
[530, 260, 20, 40, BLACK],
[670, 10, 20, 40, BLACK],
[530, 10, 20, 40, BLACK],
[610, 200, 20, 40, BLACK],
[670, 90, 20, 40, BLACK],
[165, 10, 20, 40, BLACK],
[290, 10, 20, 40, BLACK],
[290, 60, 20, 40, BLACK],
[270, 410, 20, 40, BLACK],
]

# Loop through the list. Create wall variable, add to the list
for item in walls:
    wall = Wall(item[0], item[1], item[2], item[3], item[4])
    wall_list.add(wall)

for item in stairs:
    stair = Wall(item[0], item[1], item[2], item[3], item[4])
    wall_list.add(stair)

# add instances to the list
all_sprite_list.add(wall_list)

door = Wall(560, 110, 20, 40, BLACK),
exit = pygame.sprite.Group()
exit.add(door)
all_sprite_list.add(exit)

# Sounds
# Background sound
pygame.mixer.music.load('Caketown.mp3')
pygame.mixer.music.play(-1) # play in a loop

# Event/ Collide sounds
collide = pygame.mixer.Sound("collide.wav")
jump = pygame.mixer.Sound("jump.wav")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Speed in pixels per frame
x_speed = 0
y_speed = 0

# Current position
x_coord = 10
y_coord = 10

# create Player instance
stickman = Stickman(x_coord, y_coord, 24, 38)
# set attribute/field
stickman.walls = wall_list

# add player to sprite list
all_sprite_list.add(stickman)

font = pygame.font.Font(None, 50)#can change fontname ->e.g."C:/Windows/FontDir/SHLBKB.TTF"

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key

        # Sprite
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    stickman.go_left()
                if event.key == pygame.K_RIGHT:
                    stickman.go_right()
                if event.key == pygame.K_UP:
                    stickman.jump()

        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and stickman.change_x < 0:
                    stickman.stop()
                if event.key == pygame.K_RIGHT and stickman.change_x > 0:
                    stickman.stop()

        # If the player gets near the right side, shift the world left (-x)
        if stickman.rect.right > WIDTH:
            stickman.rect.right = WIDTH

        # If the stickman gets near the left side, shift the world right (+x)
        if stickman.rect.left < 0:
            stickman.rect.left = 0

    # --- Game Logic

    # --- Drawing Code
    all_sprite_list.update()
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    if pygame.sprite.spritecollideany(stickman, exit):
          screen.fill(ORANGE)
          text = font.render("Hurray, you found the magic door!", True, BLUE)
          screen.blit(text, [60, HT/2])
          #textpos = text.get_rect(centerx=screen.get_width() / 2, y=10)
          #font = pygame.font.SysFont('Calibri', 25, True, False)
            #screen.blit(background_image, [0, 0])
          pygame.display.update()
          for obj in all_sprite_list:
                obj.kill()
          time.sleep(3)
          pygame.quit()

    #draw_stick_figure(screen, x_coord, y_coord)
    all_sprite_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

if pygame.mixer:
    pygame.mixer.music.fadeout(1000)
pygame.time.wait(1000)

# Close the window and quit.
pygame.quit()