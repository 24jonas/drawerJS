#Version history
#0.1: Movement and select color implemented
#0.2: Read and color board implemented
#0.3: Paint on board implemented
#0.4: 2P multiplayer implemented, and start from last sesion state
#0.5: Clear background button with selected color implemented



#Needs Pyxel to be installed, and run this file on shell/terminal with python
import pyxel
from collections import namedtuple

#Defined constants and variables
Point = namedtuple("Point", ["x", "y"])

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)
IDLE = Point(0, 0)

#Read player1 info to start
p1 = open("Player2.txt", "r")         # open file for reading
p1info = []                              # initialize empty array
for line in p1:
    p1info.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                  # thus creating an array of arrays.
p1.close()                          # close file.
START = Point(int(p1info[0][0]), int(p1info[0][1]))
SELECTEDCOL = int(p1info[0][2])

#Game
class drawer:
    #Runs when booted
    def __init__(self):
        pyxel.init(32,32,caption="JS Draw", fps=10)
        self.reset()
        pyxel.run(self.update, self.draw)
    
    #Runs when indicated by init or update
    def reset(self):
        self.direction = RIGHT
        self.snake = START
        
        
        
        
    #Runs repeatedly, as indicated by init. Manages game logic
    def update(self):
        self.update_direction()
        self.update_snake()
        self.update_color()

        if pyxel.btnp(pyxel.KEY_R):
            self.background()
    
    #Updates direction on button press
    def update_direction(self):
    
        if pyxel.btn(pyxel.KEY_UP):
            self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = RIGHT
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
            
            #Update player2 info
            p1 = open("Player2.txt", "w")
            p1.write(str(self.snake.x) + " " + str(self.snake.y) + " " + str(SELECTEDCOL))
            p1.close
              
    #Changes selected color on button press
    def update_color(self):
        global SELECTEDCOL
        if pyxel.btn(pyxel.KEY_E):
            SELECTEDCOL = SELECTEDCOL + 1
            if SELECTEDCOL > 15:
                SELECTEDCOL = 0
            #Update player2 info
            p1 = open("Player2.txt", "w")
            p1.write(str(self.snake.x) + " " + str(self.snake.y) + " " + str(SELECTEDCOL))
            p1.close
            
    #Clears and changes background color on button press
    def background(self):
        if pyxel.btn(pyxel.KEY_R):
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
        pyxel.cls(col=7)
        self.draw_snake()
        self.draw_board()
    
    #Shows player position and color
    def draw_snake(self):
        pyxel.pset(self.snake.x, self.snake.y, col=SELECTEDCOL)
        
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
        if pyxel.btn(pyxel.KEY_W):
            var[self.snake.x][self.snake.y] = str(SELECTEDCOL)
            with open("Board.txt", "w") as txt_file:
                for line in var:
                    txt_file.write(" ".join(line) + "\n")
            txt_file.close
            
        #Read player1 info
        p2 = open("Player1.txt", "r")         # open file for reading
        p2info = []                              # initialize empty array
        for line in p2:
            p2info.append(line.strip().split(' ')) # split each line on the <space>, and turn it into an array
                                          # thus creating an array of arrays.
        p2.close()                          # close file.
        var[int(p2info[0][0])][int(p2info[0][1])] = str(p2info[0][2])    
            
        #Show board
        for i in range(0,32):
            for j in range(0,32):
                if i is not self.snake.x or j is not self.snake.y:
                    pyxel.pset(i,j,var[i][j])
                    
            
        
    
drawer()