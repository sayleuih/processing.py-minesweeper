add_library('minim')
minim = Minim(this)

import time 
import random 
SIDE_LENGTH = 18
SQUARES_PER_SIDE = 20
MAX_MINES = 100

class Grid(object):
    isEndGame = False
    realOver = False
    minesPlaced = 0
    soundOnce = 0
    overTime = 0
    countFlagged = 0
    
    def __init__(self, sideLength, numMines):
        self.sideLength = sideLength
        self.numMines = numMines 
        self.grid = [[(Cell(0, 0)) for i in range(self.sideLength)] for j in range(self.sideLength)]
      
    def newGame(self):
        startTime = time.time()
        Grid.realOver = False
        Grid.isEndGame = False
        Grid.minesPlaced = 0
        Grid.soundOnce = 0
        Grid.overTime = 0
        Grid.countFlagged = 0
        self.grid = [[(Cell(0, 0)) for i in range(self.sideLength)] for j in range(self.sideLength)]
        self.fillGrid()
        self.placeMines()
        
            
    def fillGrid(self):
        x = SIDE_LENGTH * 6
        y = 0
        for i in range(self.sideLength):
            for j in range(len(self.grid[0])):
                self.grid[i][j].setXCoor(x)
                self.grid[i][j].setYCoor(y)
                x += SIDE_LENGTH
            y += SIDE_LENGTH
            x = SIDE_LENGTH * 6
    
    def placeMines(self):
        for mines in range(self.numMines):
            if random.randint(1, 2) > 1.5:
                self.grid[random.randint(0, self.sideLength - 1)][random.randint(0, self.sideLength - 1)].setHasMine()
                Grid.minesPlaced += 1

    def getMineCounts(self, row, col):
        mineCount = 0
        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
            if(row + dx >= 0 and col + dy >= 0 and row + dx < self.sideLength and col + dy < self.sideLength):
                if(self.grid[row + dx][col + dy].getHasMine() == True):
                    mineCount += 1
        self.grid[row][col].setMinesAround(mineCount)
        return mineCount

    def spreadSelect(self, row, col):
        hiddenStatus = False
        if(self.getMineCounts(row, col) == 0):
            for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
                if(row + dx >= 0 and col + dy >= 0 and row + dx < self.sideLength and col + dy < self.sideLength):
                    if(self.grid[row + dx][col + dy].getHasMine() == False and self.grid[row + dx][col + dy].getFlagged() == False and self.grid[row + dx][col + dy].isHidden() == True):
                        self.grid[row + dx][col + dy].setHidden(hiddenStatus)
                        if(self.getMineCounts(row + dx, col + dy) == 0):
                            self.spreadSelect(row + dx, col + dy)
                    
    def display(self):
        maxViolator = 1
        
        rectMode(CORNER)
        fill(26, 26, 26)
        rect(0, 0, SIDE_LENGTH * 6, SIDE_LENGTH * SQUARES_PER_SIDE)
        
        for i in range(self.sideLength):
            for j in range(len(self.grid[0])):
                 if(Grid.isEndGame != True):
                    if(self.grid[i][j].select()):
                        self.spreadSelect(i, j)
                        self.getMineCounts(i, j)
                 if(Grid.overTime < 5):
                    self.grid[i][j].display()
                    self.drawTimer()
                 if(self.grid[i][j].getHasMine() == True and self.grid[i][j].isHidden() == False and self.grid[i][j].getFlagged() == False and maxViolator == 1):
                    maxViolator = 0
                    Grid.isEndGame = True
                    self.grid[i][j].setViolator(True)
                                    
                    for i in range(self.sideLength):
                        for j in range(len(self.grid[0])):
                            if(self.grid[i][j].getHasMine() == True and self.grid[i][j].isHidden() == True):
                                self.grid[i][j].setHidden(False)
                                self.grid[i][j].display()      
                    time.sleep(.3)
                    Grid.overTime += 1 
                    print(Grid.overTime)
                    if(Grid.overTime >= 5):
                        self.gameOver() 
                 if(self.winCheck() == True):
                    self.youWin()
        
    def drawTimer(self):
        currentTime = str(round(time.time() - startTime, 0))
        fill(255)
        rectMode(CORNER)
        rect(30, 10, 45, 20)
        textAlign(CENTER)
        fill(61, 89, 171)
        font = createFont("Times", 16)
        textFont(font, 16)
        text("".join(currentTime), 52, 26)
        
    def drawMinesLeft(self):
        minesLeft = str(Grid.minesPlaced - Grid.countFlagged)
        fill(255)
        rectMode(CORNER)
        rect(30, 310, 45, 20)
        textAlign(CENTER)
        fill(61, 89, 171)
        font = createFont("Times", 16)
        textFont(font, 16)
        text("".join(minesLeft), 52, 326)
                    
    def gameOver(self):
        if(Grid.soundOnce == 0):
            endSound = minim.loadFile("weakExplosion.wav")
            endSound.play()
            time.sleep(4)
            endSound.close()
        background(0)
        imageMode(CORNER)
        if(Grid.realOver == False):
            gameOverSign = loadImage("gameOver2.jpg")
            image(gameOverSign, 0, 0, SIDE_LENGTH * SQUARES_PER_SIDE + SIDE_LENGTH * 6, SIDE_LENGTH * SQUARES_PER_SIDE)
            self.clickToContinue()
        else:
            gameOverSign = loadImage("gameOver3.gif")
            image(gameOverSign, 0, 0, SIDE_LENGTH * SQUARES_PER_SIDE + SIDE_LENGTH * 6, SIDE_LENGTH * SQUARES_PER_SIDE)
        if(Grid.soundOnce < 2):
            Grid.soundOnce += 1
        
    def winCheck(self):
        Grid.countFlagged = 0
        for i in range(self.sideLength):
            for j in range(len(self.grid[0])):
                if(self.grid[i][j].getFlagged()):
                    Grid.countFlagged += 1
        if(Grid.isEndGame != True):
            self.drawMinesLeft()
        if(Grid.minesPlaced == Grid.countFlagged):
            for i in range(self.sideLength):
                for j in range(len(self.grid[0])):
                    if(self.grid[i][j].isHidden() == True):
                        return False
            return True
        else:
            return False
        
    def clickToContinue(self):
        
        if(mouseX < SIDE_LENGTH * SQUARES_PER_SIDE / 2 + SIDE_LENGTH * 3 and Grid.realOver == False):
            imageMode(CORNER)
            selectTriangle = loadImage("select.JPG")
            image(selectTriangle, SIDE_LENGTH * SQUARES_PER_SIDE / 2 + SIDE_LENGTH * 3 - 45, SIDE_LENGTH * SQUARES_PER_SIDE / 2 + 56, 13, 13)
            filter(INVERT)
            if(keyPressed == True):
               self.newGame()
               Grid.realOver = True
                                 
        elif(mouseX > SIDE_LENGTH * SQUARES_PER_SIDE / 2 + SIDE_LENGTH * 3 and Grid.realOver == False):
            imageMode(CORNER)
            selectTriangle = loadImage("select.JPG")
            image(selectTriangle, SIDE_LENGTH * SQUARES_PER_SIDE / 2 + SIDE_LENGTH * 3 + 7, SIDE_LENGTH * SQUARES_PER_SIDE / 2 + 56, 13, 13)
            filter(INVERT)
            if(keyPressed == True):
                imageMode(CORNER)
                gameOverSign = loadImage("gameOver3.gif")
                image(gameOverSign, 0, 0, SIDE_LENGTH * SQUARES_PER_SIDE + SIDE_LENGTH * 6, SIDE_LENGTH * SQUARES_PER_SIDE)
                Grid.realOver = True
        
    def youWin(self):
        Grid.isEndGame = True
        print("Winner Winner Chicken Dinner")
    
class Cell(object):   
    violationCount = 0 
      
    def __init__(self, xCoor, yCoor):
        self.hidden = True
        self.hasMine = False
        self.flagged = False
        self.violator = False
        self.numMinesAround = 0
        self.xCoor = xCoor 
        self.yCoor = yCoor 
        self.xSize = SIDE_LENGTH
        self.ySize = SIDE_LENGTH 
        
    def getHasMine(self):
        return self.hasMine
    
    def setHasMine(self):
        self.hasMine = True
        
    def getXCoor(self):
        return self.xCoor 
    
    def getYCoor(self):
        return self.yCoor 
        
    def setXCoor(self, xCoor):
        self.xCoor = xCoor
    
    def setYCoor(self, yCoor):
        self.yCoor = yCoor
        
    def getFlagged(self):
        return self.flagged
    
    def setFlagged(self, flagged):
        self.flagged = flagged 
    
    def isHidden(self):
        return self.hidden
    
    def setHidden(self, status):
        self.hidden = status
        
    def setMinesAround(self, minesSurrounding):
        self.numMinesAround = minesSurrounding
        
    def getMinesAround(self):
        return self.numMinesAround 
        
    def getViolator(self):
        return self.violator
    
    def setViolator(self, violation):
        self.violator = violation 
    
    def display(self):
        bpos = random.randint(1, 10000)
        
        if(self.hidden):
            rectMode(CORNER)
            fill(0, 40, noise(bpos) * 255);
            rect(self.xCoor, self.yCoor, self.xSize, self.ySize)
            bpos += 0.01
        elif(self.flagged == True):
            imageMode(CORNER)
            flagImg = loadImage("flag.jpg")
            image(flagImg, self.xCoor, self.yCoor, self.xSize, self.ySize)      
        elif(self.hasMine):
            rectMode(CORNER)
            if(self.violator):
                if(Cell.violationCount == 0):
                    imageMode(CORNER)
                    mineRed = loadImage("mineRed.jpg")
                    image(mineRed, self.xCoor, self.yCoor, self.xSize, self.ySize)
                    Cell.violationCount += 1
            else:
                imageMode(CORNER)
                mine = loadImage("mine.png")
                image(mine, self.xCoor, self.yCoor, self.xSize, self.ySize)
        
            if(self.flagged == True):
                imageMode(CORNER)
                dMine = loadImage("deadMine.JPG")
                image(dMine, self.xCoor, self.yCoor, self.xSize, self.ySize)
        elif(self.numMinesAround != 0):
            rectMode(CORNER)
            fill(193, 205, 193)
            rect(self.xCoor, self.yCoor, self.xSize, self.ySize)
            
            numMines = ""
            
            if(self.numMinesAround == 1):
                numMines = "1"
                fill(0, 0, 255)
            elif(self.numMinesAround == 2):
                numMines = "2"
                fill(0, 205, 0)
            elif(self.numMinesAround == 3):
                numMines = "3"
                fill(255, 0, 0)
            elif(self.numMinesAround == 4):
                numMines = "4"
                fill(128, 0, 128)
            elif(self.numMinesAround == 5):
                numMines = "5"
                fill(128, 0, 0)
            elif(self.numMinesAround == 6):
                numMines = "6"
                fill(72, 209, 204)
            elif(self.numMinesAround == 7):
                numMines = "7"
                fill(0, 0, 0)
            elif(self.numMinesAround == 8):
                numMines = "8"
                fill(169, 169, 169)
                
            textAlign(CORNER)
            font = createFont("Arial", 16)
            textFont(font, 16)
            text("".join(numMines), self.xCoor + 5, self.yCoor + 15)
        else:
            rectMode(CORNER)
            fill(193, 205, 193)
            rect(self.xCoor, self.yCoor, self.xSize, self.ySize)
    
    def select(self):
        selected = False
        if(mouseButton == RIGHT and mouseX > self.xCoor and mouseX < self.xCoor + (self.xSize) and 
            mouseY > self.yCoor and mouseY < self.yCoor + (self.ySize) and self.flagged == False):
            self.hidden = False
            self.flagged = True
            selected = True
            self.display()
        elif(mouseButton == LEFT and mouseX > self.xCoor and mouseX < self.xCoor + (self.xSize) and 
            mouseY > self.yCoor and mouseY < self.yCoor + (self.ySize) and self.flagged == True):
            self.hidden = True
            self.flagged = False
            selected = True
            self.display()       
        elif(mouseButton == LEFT and mouseX > self.xCoor and mouseX < self.xCoor + (self.xSize) and 
            mouseY > self.yCoor and mouseY < self.yCoor + (self.ySize)):
            self.hidden = False
            selected = True
            self.display()
        return selected

def setup():
    size(SIDE_LENGTH * SQUARES_PER_SIDE + SIDE_LENGTH * 6, SIDE_LENGTH * SQUARES_PER_SIDE)
    
#Creating the game
startTime = time.time()
mineSweeper = Grid(SQUARES_PER_SIDE, MAX_MINES)
mineSweeper.newGame()
     
def draw():
    mineSweeper.display()  
