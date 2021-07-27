#Version history
#0.1: Movement and select color implemented
#0.2: Read and color board implemented
#0.3: Paint on board implemented
#0.4: 2P multiplayer implemented, and start from last sesion state
#0.5: Clear background button with selected color implemented



#Needs Pyxel to be installed, and run this file on shell/terminal with python
import os, sys
import pygame
from collections import namedtuple
from math import pi

#Defined constants and variables
Point = namedtuple("Point", ["x", "y"])

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)
IDLE = Point(0, 0)

#Read player1 info to start
p1 = open("Player1.txt", "r")         # open file for reading
p1info = []                              # initialize empty array
for line in p1:
    p1info.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                  # thus creating an array of arrays.
p1.close()                          # close file.
START = Point(int(p1info[0][0]), int(p1info[0][1]))
SELECTEDCOL = int(p1info[0][2])

pygame.init()

size = [0, 0]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
game_surface = pygame.Surface((32, 32))
screen_width = screen.get_width()
screen_height = screen.get_height()
smallest_side = min(screen_width, screen_height)
screen_surface = pygame.Surface((smallest_side, smallest_side))

RED     = (255,   0,   0)
ORANGE  = (255, 128,   0)
YELLOW  = (255, 255,   0)
LIME    = (128, 255,   0)
GREEN   = (0  , 255,   0)
MINT    = (0  , 255, 128)
CYAN    = (0  , 255, 255)
BLUE    = (0  , 128, 255)
INDIGO  = (0  ,   0, 255)
PURPLE  = (127,   0, 255)
MAGENTA = (255,   0, 255)
PINK    = (255,   0, 127)
WHITE   = (255, 255, 255)
LGRAY   = (192, 192, 192)
DGRAY   = ( 96,  96,  96)
BLACK   = (  0,   0,   0)

colors = [RED, ORANGE, YELLOW, LIME, GREEN, MINT, CYAN, BLUE, INDIGO, PURPLE, MAGENTA, PINK, WHITE, LGRAY, DGRAY, BLACK]





#Game
class drawer:
    #Runs when booted
    def __init__(self):
        self.reset()
        run = True
        while run:
            self.update()
            self.draw()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
    
    #Runs when indicated by init or update
    def reset(self):
        self.direction = RIGHT
        self.snake = START
        
        
        
        
    #Runs repeatedly, as indicated by init. Manages game logic
    def update(self):
        self.update_direction()
        self.update_snake()
        self.update_color()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.background()
            pygame.time.delay(100)
    
    #Updates direction on button press
    def update_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction = UP
            pygame.time.delay(100)
        elif keys[pygame.K_DOWN]:
            self.direction = DOWN
            pygame.time.delay(100)
        elif keys[pygame.K_LEFT]:
            self.direction = LEFT
            pygame.time.delay(100)
        elif keys[pygame.K_RIGHT]:
            self.direction = RIGHT
            pygame.time.delay(100)
        else:
            self.direction = IDLE
            
    #Updates position according to direction        
    def update_snake(self):
    
        if self.direction is not IDLE: #Avoids update if no button is pressed
            #Movement
            old_head = self.snake
            new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
            #Border control
            if new_head.x > 31:
                new_head = Point(new_head.x - 32, new_head.y)
            elif new_head.x < 0:
                new_head = Point(new_head.x + 32, new_head.y)
            elif new_head.y > 31:
                new_head = Point(new_head.x, new_head.y - 32)
            elif new_head.y < 0:
                new_head = Point(new_head.x, new_head.y + 32)
            #New position    
            self.snake = new_head
            
            #Update player1 info
            p1 = open("Player1.txt", "w")
            p1.write(str(self.snake.x) + " " + str(self.snake.y) + " " + str(SELECTEDCOL))
            p1.close
              
    #Changes selected color on button press
    def update_color(self):
        global SELECTEDCOL
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            SELECTEDCOL = SELECTEDCOL + 1
            if SELECTEDCOL > 15:
                SELECTEDCOL = 0
            #Update player1 info
            p1 = open("Player1.txt", "w")
            p1.write(str(self.snake.x) + " " + str(self.snake.y) + " " + str(SELECTEDCOL))
            p1.close
            pygame.time.delay(200)
            
    #Clears and changes background color on button press
    def background(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            file = open("Board.txt", "r")         # open file for reading
            var = []                              # initialize empty array
            for line in file:
                var.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                          # thus creating an array of arrays.
            file.close()                          # close file.
            
            
            for i in range(0,32):
                for j in range(0,32):
                    var[i][j] = str(SELECTEDCOL)
            with open("Board.txt", "w") as txt_file:
                for line in var:
                    txt_file.write(" ".join(line) + "\n")
            txt_file.close
    
    
        
    

    #Runs repeatedly, as indicated by init. Manages game graphics
    def draw(self):
        #pyxel.cls(col=7)
        #self.draw_snake()
        self.draw_board()
    
    #Shows player position and color  colors[int(SELECTEDCOL)]
    #def draw_snake(self):
    #    pygame.draw.rect(screen, colors[int(SELECTEDCOL)], [self.snake.x, self.snake.y, self.snake.x, self.snake.y])
    #    pygame.display.update()
        
    #Draws board
    def draw_board(self):
        #Read board
        file = open("Board.txt", "r")         # open file for reading
        var = []                              # initialize empty array
        for line in file:
            var.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                          # thus creating an array of arrays.
        file.close()                          # close file.

        #Paint on board
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            var[self.snake.y][self.snake.x] = str(SELECTEDCOL)
            with open("Board.txt", "w") as txt_file:
                for line in var:
                    txt_file.write(" ".join(line) + "\n")
            txt_file.close
            pygame.time.delay(100)
            
        #Read player2 info
        p2 = open("Player2.txt", "r")         # open file for reading
        p2info = []                              # initialize empty array
        for line in p2:
            p2info.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                          # thus creating an array of arrays.
        p2.close()                          # close file.
        var[int(p2info[0][0])][int(p2info[0][1])] = str(p2info[0][2])
        var[int(self.snake.y)][int(self.snake.x)] = str(SELECTEDCOL)
            
        #Show board
        for i in range(0,32):
            for j in range(0,32):
                #if i is not self.snake.y or j is not self.snake.x:
                pygame.draw.rect(game_surface, colors[int(var[i][j])], [j, i, j, i])
        
        pygame.transform.scale(
        game_surface,  # surface to be scaled
        (smallest_side, smallest_side),  # scale up to (width, height)
        screen_surface)  # surface that game_surface will be scaled onto
        screen.blit(
        screen_surface,
        ((screen_width - smallest_side) // 2,  # x pos
        (screen_height - smallest_side) // 2))  # y pos

        pygame.display.flip()
        #pygame.display.update() 
                    
            
        

drawer()
pygame.quit() 
