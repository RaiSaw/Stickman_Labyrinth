# Make Stickman move using keyboard, create walls, add sprite/s and sounds
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
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Stick man")

# create Sprite group lists
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

# create instances of class sprite
# Walls
wall = Wall(0, 0, 10, 600, GREEN)
wall_list.add(wall)

wall = Wall(10, 0, 790, 10, GREEN)
wall_list.add(wall)

wall = Wall(0, 490, 790, 10, GREEN)
wall_list.add(wall)

wall = Wall(690, 0, 10, 600, GREEN)
wall_list.add(wall)
# stairs
wall = Wall( 100, 470, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 140, 450, 50, 10, PURPLE)
wall_list.add(wall)

wall = Wall( 180, 430, 50, 10, PURPLE)
wall_list.add(wall)
# door
wall = Wall(210, 390, 20, 40, BLACK)
wall_list.add(wall)

# add instances to the list
all_sprite_list.add(wall_list)
#create instance of class sprite stickman

# Sounds
# Background sound
pygame.mixer.music.load('Caketown.mp3')
pygame.mixer.music.play()

# Event/ Collide sounds
collide = pygame.mixer.Sound("collide.wav")
jump = pygame.mixer.Sound("jump.wav")

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
#pygame.mouse.set_visible(0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Current position
x_coord = 10
y_coord = 10

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0

            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0


    # --- Game Logic

    if x_coord > 690  or x_coord < 0:
        x_speed *= -1
        collide.play()
    if  y_coord > 470 or y_coord < 0:
        y_speed *= -1
        collide.play()

    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed

    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    draw_stick_figure(screen, x_coord, y_coord)
    all_sprite_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
