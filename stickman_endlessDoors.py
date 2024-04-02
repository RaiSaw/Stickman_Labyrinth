# Make Stickman jump, add sprites gravity and maze
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)


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
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                #jump.play()
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                #jump.play()

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
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
# create instances of class sprite Wall
# walls
wall = Wall(0, 0, 10, 600, GREEN)
wall_list.add(wall)

wall = Wall(10, 0, 40, 10, BLACK)
wall_list.add(wall)

wall = Wall(40, 0, 790, 10, GREEN)
wall_list.add(wall)

wall = Wall(0, 490, 790, 10, GREEN)
wall_list.add(wall)

wall = Wall(690, 0, 10, 600, GREEN)
wall_list.add(wall)
# stairs1
wall = Wall( 160, 440, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 190, 410, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 230, 380, 70, 10, PURPLE)
wall_list.add(wall)
# door
wall = Wall(260, 340, 20, 40, BLACK)
wall_list.add(wall)
#stairs2
wall = Wall(70, 390, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(40, 360, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(10, 330, 50, 10, PURPLE)
wall_list.add(wall)
# doors
wall = Wall(10, 450, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(10, 290, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(70, 400, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(260, 160, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(310, 270, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(370, 360, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(420, 250, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(570, 340, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(570, 390, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(670, 10, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(670, 260, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall(670, 450, 20, 40, BLACK)
wall_list.add(wall)
#stairs3
wall = Wall( 330, 440, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 290, 410, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 340, 350, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 360, 320, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 390, 290, 70, 10, PURPLE)
wall_list.add(wall)
#stair4
wall = Wall( 310, 260, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 280, 230, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 230, 200, 70, 10, PURPLE)
wall_list.add(wall)
#stair5
wall = Wall( 330, 440, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 290, 410, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 360, 320, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 390, 290, 70, 10, PURPLE)
wall_list.add(wall)

#stair6
wall = Wall( 360, 320, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 460, 320, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 490, 350, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 540, 380, 70, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 620, 330, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 650, 300, 40, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 650, 410, 40, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 620, 440, 50, 10, PURPLE)
wall_list.add(wall)

#stair7
wall = Wall( 580, 190, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 610, 160, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 640, 130, 50, 10, PURPLE)
wall_list.add(wall)

#doors
wall = Wall( 530, 260, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 560, 110, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 530, 10, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 610, 200, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 670, 90, 20, 40, BLACK)
wall_list.add(wall)
# stairs8
wall = Wall( 500, 220, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 530, 250, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 560, 280, 50, 10, PURPLE)
wall_list.add(wall)

#stair9
wall = Wall( 640, 50, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 560, 100, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 520, 140, 40, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 470, 110, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 370, 80, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 340, 110, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 330, 160, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 390, 50, 70, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 420, 10, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 420, 120, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 420, 170, 20, 40, BLACK)
wall_list.add(wall)

#stairs10
wall = Wall( 440, 80, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 390, 160, 70, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 530, 50, 50, 10, PURPLE)
wall_list.add(wall)

#stairs11
wall = Wall( 150, 290, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 120, 320, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 150, 330, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 210, 270, 20, 40, BLACK)
wall_list.add(wall)

wall = Wall( 180, 260, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 210, 230, 50, 10, PURPLE)
wall_list.add(wall)
#stair12
wall = Wall( 430, 440, 50, 10, PURPLE)
wall_list.add(wall)
wall = Wall( 460, 400, 50, 10, PURPLE)
wall_list.add(wall)
wall = Wall( 490, 360, 20, 40, BLACK)
wall_list.add(wall)
wall = Wall( 520, 450, 20, 40, BLACK)
wall_list.add(wall)
#stairs13
wall = Wall(70, 250, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(40, 220, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(10, 190, 50, 10, PURPLE)
wall_list.add(wall)
wall = Wall(60, 230, 20, 40, BLACK)
wall_list.add(wall)

#stairs14
wall = Wall(150, 170, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(120, 140, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(90, 110, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(60, 140, 50, 10, PURPLE)
wall_list.add(wall)
wall = Wall(10, 60, 40, 10, PURPLE)
wall_list.add(wall)
wall = Wall(120, 150, 20, 40, BLACK)
wall_list.add(wall)
wall = Wall(10, 150, 20, 40, BLACK)
wall_list.add(wall)

#stairs15
wall = Wall(210, 110, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(180, 80, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(150, 50, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall(270, 50, 60, 10, PURPLE)
wall_list.add(wall)
#doors
wall = Wall(165, 10, 20, 40, BLACK)
wall_list.add(wall)
wall = Wall(290, 10, 20, 40, BLACK)
wall_list.add(wall)
wall = Wall(290, 60, 20, 40, BLACK)
wall_list.add(wall)
wall = Wall(270, 410, 20, 40, BLACK)
wall_list.add(wall)

# add instances to the list
all_sprite_list.add(wall_list)

# Sounds
# Background sound
pygame.mixer.music.load('Caketown.mp3')
pygame.mixer.music.play(-1) # play in indefinite loop

# Event/ Collide sounds
collide = pygame.mixer.Sound("punch.wav")
jump = pygame.mixer.Sound("whiff.wav")

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

stickman = Stickman(x_coord, y_coord, 24, 38)
stickman.walls = wall_list

all_sprite_list.add(stickman)

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