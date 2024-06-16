# Classes, enemies..
# To-dos: Rooms, random doors, levels, moving platform
import pygame
import time, random

# Define some colors🌈
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YG = (173, 255, 47)
OLIVE = (128, 128, 0)
#Stairs, walls
SG = (165,42,42)
DS = (47,79,79)
S = (160,82,45)
MR = (128,0,0)

def draw_stick_figure(screen, color, x, y):
  # Head
  pygame.draw.ellipse(screen,  BLACK, [1 + x, y, 10, 10], 0)
  # Legs
  pygame.draw.line(screen,  BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
  pygame.draw.line(screen,  BLACK, [5 + x, 17 + y], [x, 27 + y], 2)
  # Body
  pygame.draw.line(screen,  color, [5 + x, 17 + y], [5 + x, 7 + y], 2)
  # Arms
  pygame.draw.line(screen,  color, [5 + x, 7 + y], [9 + x, 17 + y], 2)
  pygame.draw.line(screen,  color, [5 + x, 7 + y], [1 + x, 17 + y], 2)

class Stickman(pygame.sprite.Sprite):

  def __init__(self, color, x, y, width, height):
    # Call the parent class (Sprite) constructor
    super().__init__()
    # Create an image of the block, and fill it with a color.
    self.image = pygame.Surface([width, height])
    self.image.fill(WHITE)
    self.image.set_colorkey(WHITE)

    draw_stick_figure(self.image, color, x, y)
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
    block_hit_list1 = pygame.sprite.spritecollide(self, stair_list, False)
    for block in block_hit_list1:
      # If we are moving right, set our right side to the left side of
      # the item we hit
      if self.change_x > 0:
        self.rect.right = block.rect.left
      elif self.change_x < 0:
        # Otherwise if we are moving left, do the opposite.
        self.rect.left = block.rect.right
          #collide.play()

    door_hit_list1 = pygame.sprite.spritecollide(self, door_list, False)
    for block in door_hit_list1:
      # If we are moving right, set our right side to the left side of
      # the item we hit
      if self.change_x > 0:
        self.rect.right = block.rect.left
        collide.play()
      elif self.change_x < 0:
        # Otherwise if we are moving left, do the opposite.
        self.rect.left = block.rect.right
        collide.play()
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
    self.image = pygame.Surface([
        width, height
    ])  #blank surface to draw on, no ned if you have a graphic surface
    self.image.fill(color)

    # Make our top-left corner the passed-in location.
    self.rect = self.image.get_rect()  #[x, y, w, h]
    self.rect.y = y
    self.rect.x = x

class Door(pygame.sprite.Sprite):
  """ Wall the player can run into. """

  def __init__(self, x, y):
    """ Constructor for the wall that the player can run into. """
    # Call the parent's constructor
    #pygame.sprite.Sprite.__init__(self) -initialize parent
    super().__init__()

    # Make a wall, of the size specified in the parameters
    self.image = pygame.image.load("castledoors.png").convert_alpha()#png
    self.image.set_colorkey(BLACK)
    self.image = pygame.transform.scale(self.image,(20,40))

    #self.image = pygame.Surface #blank surface to draw on, no ned if you have a graphic surface

    # Make our top-left corner the passed-in location.
    self.rect = self.image.get_rect()  #[x, y, w, h]
    self.rect.y = y
    self.rect.x = x


class Walker(Stickman):

    def update(self):
        """ Called each frame. """

        block_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for block in block_hit_list:
          # If we are moving right, set our right side to the left side of
          # the item we hit
          if self.change_x > 0:
            self.rect.right = block.rect.left
          elif self.change_x < 0:
            self.rect.left = block.rect.right
          elif self.change_y > 0:
            self.rect.bottom = block.rect.top
          elif self.change_y < 0:
            self.rect.top = block.rect.bottom

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1

class Walker2(Stickman):

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1

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
door_list = pygame.sprite.Group()
stair_list = pygame.sprite.Group()

block_list = pygame.sprite.Group()

# create instances of class sprite Wall
stairs = [
    #walls
    [0, 0, 10, 600, OLIVE],
    [40, 0, 790, 10, OLIVE],
    [0, 490, 790, 10, OLIVE],
    [690, 0, 10, 600, OLIVE],
    #entry portal
    [10, 0, 40, 10, OLIVE],
    #stairs1
    [160, 440, 50, 10, S],
    [190, 410, 50, 10, OLIVE],
    [230, 380, 70, 10, SG],
    #stairs2
    [70, 390, 50, 10, SG],
    [40, 360, 50, 10, OLIVE],
    [10, 330, 50, 10, MR],
    #stairs3
    [330, 440, 50, 10, OLIVE],
    [290, 410, 50, 10, S],
    [340, 350, 50, 10, MR],
    [360, 320, 50, 10, OLIVE],
    [390, 290, 70, 10, SG],
    #stair4
    [310, 260, 50, 10, OLIVE],
    [280, 230, 50, 10, S],
    [230, 200, 70, 10, SG],
    #stair5
    [330, 440, 50, 10, MR],
    [290, 410, 50, 10, S],
    [360, 320, 50, 10, OLIVE],
    [390, 290, 70, 10, SG],
    #stair6
    [360, 320, 50, 10, OLIVE],
    [450, 320, 50, 10, SG],
    [490, 350, 50, 10, MR],
    [540, 380, 70, 10, S],
    [620, 320, 50, 10, OLIVE],
    [650, 300, 40, 10, S],
    [650, 410, 40, 10, MR],
    [620, 440, 50, 10, S],
    #stair7
    [580, 190, 50, 10, S],
    [610, 160, 50, 10, SG],
    [640, 130, 50, 10, MR],
    # stairs8
    [510, 220, 40, 10, S],
    [490, 250, 80, 10, SG],
    [550, 280, 40, 10, MR],
    #stair9
    [640, 50, 50, 10, S],
    [560, 90, 40, 10, OLIVE],
    [520, 140, 40, 10, S],
    [470, 110, 50, 10, SG],
    [370, 80, 50, 10, MR],
    [340, 110, 50, 10, OLIVE],
    [330, 160, 50, 10, S],
    [390, 50, 70, 10, OLIVE],
    #stairs10
    [440, 80, 50, 10, S],
    [390, 160, 70, 10, OLIVE],
    [515, 50, 20, 10, MR],
    #stairs11
    [150, 290, 50, 10, MR],
    [120, 320, 50, 10, S],
    [180, 260, 50, 10, SG],
    [210, 230, 50, 10, MR],
    #stair12
    [430, 440, 50, 10, S],
    [460, 400, 50, 10, MR],
    #stairs13
    [80, 250, 40, 10, MR],
    [40, 220, 50, 10, S],
    [10, 190, 50, 10, OLIVE],
    #stairs14
    [150, 170, 50, 10, SG],
    [120, 140, 50, 10, S],
    [90, 110, 50, 10, MR],
    [60, 140, 50, 10, OLIVE],
    [10, 60, 40, 10, MR],
    #stairs15
    [210, 110, 50, 10, OLIVE],
    [180, 80, 50, 10, MR],
    [150, 50, 50, 10, S],
    [270, 50, 60, 10, SG],
]
doors = [
    #doors
    [60, 230,],
    [120, 150,],
    [10, 150,],
    [490, 360,],
    [520, 450,],
    [150, 330,],
    [210, 270,],
    [420, 10,],
    [420, 120,],
    [420, 170,],
    [10, 450,],
    [10, 290,],
    [70, 400,],
    [260, 160,],
    [310, 270,],
    [370, 360,],
    [420, 250,],
    [570, 340,],
    [570, 390,],
    [670, 260,],
    [670, 450,],
    [260, 340,],
    [530, 260,],
    [670, 10,],
    [530, 10,],
    [610, 200,],
    [670, 90,],
    [165, 10,],
    [290, 10,],
    [290, 60,],
    [270, 410,],
]

# Loop through the list. Create wall variable, add to the list
for item in doors:
  door = Door(item[0], item[1],)
  door_list.add(door)

for item in stairs:
  stair = Wall(item[0], item[1], item[2], item[3], item[4])
  stair_list.add(stair)

# add instances to the list
wall_list.add(door_list, stair_list)
all_sprite_list.add(wall_list)
#all_sprite_list.add(door_list)

door = Door(560, 100),
exit = pygame.sprite.Group()
exit.add(door)
all_sprite_list.add(exit)

# Sounds
# Background sound
pygame.mixer.music.load('Caketown.mp3')
pygame.mixer.music.play(-1)  # play in a loop

# Event/ Collide sounds
collide = pygame.mixer.Sound("door.wav")
jump = pygame.mixer.Sound("jump.wav")
nay = pygame.mixer.Sound("death.wav")
yay = pygame.mixer.Sound("foundit.mp3")

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
stickman = Stickman(BLUE, x_coord, y_coord, 24, 38)
# set attribute/field
stickman.walls = wall_list



# add player to sprite list
#all_sprite_list.add(stickman)
all_sprite_list.add(stickman)

    # This represents a block

block = Walker(BLACK, x_coord, y_coord, 24, 38)
# Set a random location for the block
block.rect.x = random.randrange(WIDTH)
block.rect.y = random.randrange(HT)

block.change_x = random.randrange(-3,3)
block.change_y = random.randrange(-3,3)
block.left_boundary = 0
block.top_boundary = 0
block.right_boundary = WIDTH
block.bottom_boundary = HT

block2 = Walker2(BLACK, x_coord, y_coord, 24, 38)
block2.rect.x = random.randrange(650)
block2.rect.y = random.randrange(450)

block2.change_x = random.randrange(-3,3)
block2.change_y = random.randrange(-3,3)
block2.left_boundary = 0
block2.top_boundary = 0
block2.right_boundary = WIDTH
block2.bottom_boundary = HT

# Add the block to the list of objects
block_list.add(block, block2)
all_sprite_list.add(block_list)

font = pygame.font.Font(
    None, 50)  #can change fontname ->e.g."C:/Windows/FontDir/SHLBKB.TTF"
bg = pygame.image.load("2.webp").convert_alpha()
#pygame.transform.smoothscale(bg, size)#smooth surface
#pygame.transform.scale_by(bg, (2,2))
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
    """ if stickman.rect.right > WIDTH:
      stickman.rect.right = WIDTH """

    # If the stickman gets near the left side, shift the world right (+x)
    """ if stickman.rect.left < 0:
      stickman.rect.left = 0"""
  # --- Game Logic

  if pygame.sprite.spritecollideany(stickman, exit):
    yay.play()
    screen.fill(YG)
    text = font.render("Hurray, you found the magic door!", True, BLUE)
    screen.blit(text, [60, HT / 2])
    #textpos = text.get_rect(centerx=screen.get_width() / 2, y=10)
    #font = pygame.font.SysFont('Calibri', 25, True, False
    pygame.display.update()
    for obj in all_sprite_list:
      obj.kill()
    time.sleep(3)
    pygame.quit()

  elif pygame.sprite.spritecollideany(stickman, block_list):
    nay.play()
    screen.fill(DS)
    text = font.render("Oh-oh, the enemy got to you first!", True, MR)
    screen.blit(text, [60, HT / 2])
    pygame.display.update()
    time.sleep(3)
    pygame.quit()

  # --- Drawing Code
  all_sprite_list.update()

  screen.blit(bg, [0, 0])

  #draw the sprites
  all_sprite_list.draw(screen)

  # Go ahead and update the screen with what we've drawn.
  pygame.display.flip()

  # Limit frames per second
  clock.tick(60)

#if pygame.mixer:
#  pygame.mixer.music.fadeout(100)
#pygame.time.wait(1000)

# Close the window and quit.
pygame.quit()