from cmu_112_graphics import *
import math
import time
from ghost_astar import *

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

'STARTER INFORMATION'
def appStarted(app):
    app.startGame = False
    rows, cols, cellSize, margin = gameDimensions()
    app.board = gameMap()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.margin = margin
    app.pacColor = 'yellow'
    app.pacRow = 5
    app.pacCol = 10
    app.dotColor = 'orange'
    app.dotLocations = []
    app.spawnLocation = spawnLocations()
    app.powerUpLocations = [(3,1), (3,26), (23,1), (23, 26)]
    createDots(app)
    app.score = 0
    app.wallColor = 'blue'
    app.exitLocation = [(12,13), (12,14)]
    app.pathColor = 'grey'
    app.blankColor = 'black'
    app.exitColor = 'red'
    app.ghost1Row = 14
    app.ghost1Col = 12
    app.ghost1Color = 'pink'
    app.isGameOver = False
    app.gameBeaten = False
    app.timerDelay = 250
    app.powerUpGhostColor = 'purple'
    app.timePassed = 0
    app.pacTime = 0
    app.temp = None
    app.ghostColor = False
    if app.isGameOver == True or app.gameBeaten == True:
        resetGame(app)

def resetGame(app):
    app.board = gameMap()
    app.dotLocations = []
    createDots(app)
    app.score = 0
    app.pacRow = 5
    app.pacCol = 10
    app.ghost1Row = 14
    app.ghost1Col = 12
    app.isGameOver = False
    app.gameBeaten = False

def gameDimensions():
    rows = 31
    cols = 28
    cellSize = 20
    margin = 100
    return rows, cols, cellSize, margin

def spawnLocations():
    location = ([(12,13), (12,14), (13,11), (13,12), (13,13), (13,14),
                          (13,15), (13,16), (14,11), (14,12), (14,13), (14,14),
                          (14,15), (14,16), (15,11), (15,12), (15,13), (15,14),
                          (15,15), (15,16)])
    return location

def gameMap():
    #(13,0) (13,27) should transfer
    board = ([
     ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],
     ['w','p','p','p','p','p','p','p','p','p','p','p','p','w','w','p','p','p','p','p','p','p','p','p','p','p','p','w'],
     ['w','p','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','p','w'],
     ['w','p','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','p','w'],
     ['w','p','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','p','w'],
     ['w','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','w'],
     ['w','p','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','w','w','w','p','w'],
     ['w','p','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','w','w','w','p','w'],
     ['w','p','p','p','p','p','p','w','w','p','p','p','p','w','w','p','p','p','p','w','w','p','p','p','p','p','p','w'],
     ['w','w','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','w','w'],
     ['n','n','n','n','n','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','p','p','p','p','p','p','p','p','p','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','p','p','w','w','w','p','w','w','p','w','n','n','n','n','n'],
     ['w','w','w','w','w','w','p','w','w','p','w','p','p','p','p','p','p','w','p','w','w','p','w','w','w','w','w','w'],
     ['p','p','p','p','p','p','p','p','p','p','w','p','p','p','p','p','p','w','p','p','p','p','p','p','p','p','p','p'],
     ['w','w','w','w','w','w','p','w','w','p','w','p','p','p','p','p','p','w','p','w','w','p','w','w','w','w','w','w'],
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','p','p','p','p','p','p','p','p','p','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','n','n','n','n','n'],
     ['w','w','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','w','w','w','w','w'],
     ['w','p','p','p','p','p','p','p','p','p','p','p','p','w','w','p','p','p','p','p','p','p','p','p','p','p','p','w'],
     ['w','p','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','p','w'],
     ['w','p','w','w','w','w','p','w','w','w','w','w','p','w','w','p','w','w','w','w','w','p','w','w','w','w','p','w'],
     ['w','p','p','p','w','w','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','w','w','p','p','p','w'],
     ['w','w','w','p','w','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','w','p','w','w','w'],
     ['w','w','w','p','w','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','w','p','w','w','w'],
     ['w','p','p','p','p','p','p','w','w','p','p','p','p','w','w','p','p','p','p','w','w','p','p','p','p','p','p','w'],
     ['w','p','w','w','w','w','w','w','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','w','w','p','w'],
     ['w','p','w','w','w','w','w','w','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','w','w','p','w'],
     ['w','p','p','p','p','p','p','p','p','p','p','p','p','w','w','p','p','p','p','p','p','p','p','p','p','p','p','w'],
     ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w']
     ])
    return board


'PACMAN MOVE'
def pacManMove(app, drow, dcol):
    if app.isGameOver == False:
        app.pacRow += drow
        app.pacCol += dcol
        if (app.pacRow, app.pacCol) == (13,0):
            app.pacRow = 13
            app.pacCol = 27
        elif (app.pacRow, app.pacCol) == (13,27):
            app.pacRow = 13
            app.pacCol = 0
        if pacMoveLegal(app) != True:
            app.pacRow -= drow
            app.pacCol -= dcol
    

def pacMoveLegal(app):
    if (app.pacRow < 0 or app.pacCol < 0 or app.pacRow >= app.rows or
    app.pacCol >= app.cols or app.board[app.pacRow][app.pacCol] == 'w'
    or (app.pacRow, app.pacCol) in app.exitLocation):
        return False
    return True

def powerUp(app):
    if (app.pacRow, app.pacCol) in app.powerUpLocations:
        app.temp = (app.pacRow, app.pacCol)
        point = (app.pacRow, app.pacCol)
        app.powerUpLocations.remove(point)
        return True
    return False

def checkGhostColor(app):
    if app.temp == None:
        app.ghostColor = False
    app.ghostColor = True


'CREATING DOTS AND ITEMS'
def createDots(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 'p' and (row, col) != (5,10):
                if (row, col) not in app.spawnLocation and (row, col) not in app.powerUpLocations:
                    coordinate = (row, col)
                    app.dotLocations.append(coordinate)
 
def checkDotPacCollision(app):
    if (app.pacRow, app.pacCol) in app.dotLocations:
        point = (app.pacRow, app.pacCol)
        app.dotLocations.remove(point)
        calculateScore(app)


'CREATING CELL AND BOARD'
def getCellBounds(app, row, col):
    #taken from 15-112 Website
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + col * gridWidth / app.cols
    x1 = app.margin + (col+1) * gridWidth / app.cols
    y0 = app.margin + row * gridHeight / app.rows
    y1 = app.margin + (row+1) * gridHeight / app.rows
    return (x0, y0, x1, y1)


'USER INTERFACE'
def startGame(app):
    return 42

def keyPressed(app, event):
    drow = 0
    dcol = 0
    if event.key == 'Space':
        app.startGame = True
    if app.startGame == True:
        if event.key == 'Up':
            drow = -1
            dcol = 0
        elif event.key == 'Down':
            drow = 1
            dcol = 0
        elif event.key == 'Left':
            drow = 0
            dcol = -1
        elif event.key == 'Right':
            drow = 0
            dcol = 1
        elif event.key == 'r':
            resetGame(app)
        elif event.key == 'f':
            app.dotLocations.clear()
        pacManMove(app, drow, dcol)
        checkDotPacCollision(app)


'Ghost Movement'

def ghostMove(app):
    start = (app.ghost1Row, app.ghost1Col)
    goal = (app.pacRow, app.pacCol)
    path = AStar(app.board, start, goal)
    return path

def ghostLegal(app):
    if (app.ghost1Row < 0 or app.ghost1Col < 0 or app.ghost1Row >= app.rows
    or app.ghost1Col >= app.cols or app.board[app.ghost1Row][app.ghost1Col] == 'w'):
        return False
    return True

def ghostCollision(app):
    if app.ghost1Row == app.pacRow and app.ghost1Col == app.pacCol:
        return False
    return True

def timerFired(app):
    if app.startGame == True:
        beatingGame(app)
        if app.isGameOver == False and app.gameBeaten == False:
            if ghostLegal(app) != False:
                if powerUp(app) == True or app.temp != None:
                    checkGhostColor(app)
                    app.timePassed += app.timerDelay
                    app.pacTime += app.timerDelay
                    if app.timePassed < 2000:
                        app.ghost1Row = app.ghost1Row
                        app.ghost1Col = app.ghost1Col
                    else:
                        app.timePassed = 0
                        app.pacTime = 0
                        app.temp = None
                        app.ghostColor = False
                elif powerUp(app) == False:
                    path = ghostMove(app)
                    #print(path)
                    if path != None:
                        if ghostCollision(app) != True:
                            app.isGameOver = True
                        else:
                            if len(path) == 1:
                                app.isGameOver = True
                            else:
                                nextMove = path[1]
                                app.ghost1Row = nextMove[0]
                                app.ghost1Col = nextMove[1]


'Point System'
def calculateScore(app):
    if app.temp != None:
        app.score += 20
    else:
        app.score += 10

'GAME OVER'
def beatingGame(app):
    if len(app.dotLocations) == 0:
        app.gameBeaten = True

'DRAW FUNCTIONS'
def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            if app.board[row][col] == 'w':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.wallColor)
            elif app.board[row][col] == 'p' and (row, col) not in app.exitLocation:
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.pathColor)
            elif app.board[row][col] == 'n':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.blankColor)
            elif app.board[row][col] == 's':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.pathColor)
            elif app.board[row][col] == 'p' and (row, col) in app.exitLocation:
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.exitColor)
            

def drawPacMan(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.pacRow, app.pacCol)
    canvas.create_oval(x0, y0, x1, y1, fill = app.pacColor)

def drawGhost1(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.ghost1Row, app.ghost1Col)
    if app.ghostColor == False:
        canvas.create_oval(x0, y0, x1, y1, fill = app.ghost1Color)
    elif app.ghostColor == True:
        canvas.create_oval(x0, y0, x1, y1, fill = app.powerUpGhostColor)

def drawDot(app, canvas):
    for (row, col) in app.dotLocations:
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        canvas.create_oval(x0+6.5, y0+6.5, x1-6.5, y1-6.5, fill = app.dotColor)

def drawPowerUp(app, canvas):
    for (row, col) in app.powerUpLocations:
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        canvas.create_oval(x0+3, y0+3, x1-3, y1-3, fill=app.dotColor)

def drawScore(app, canvas):
    x = app.width//2
    y = app.height//30
    canvas.create_text(x, y, text = f'Score = {app.score}', fill = 'White',
                        font = 'Times 20 bold')

def drawStartGame(app, canvas):
    if app.startGame == False:
        x = app.width//2
        y = app.height//2
        canvas.create_text(x, y, text ='Press SPACE to Start Game', fill = 'White',
                    font = 'Times 40 bold italic')


def drawGameOver(app, canvas):
    if app.isGameOver == True:
        x = app.width//2
        y = app.height//2
        canvas.create_text(x, y, text ='GAME OVER!', fill = 'White',
                    font = 'Times 40 bold italic')

def drawBeatenGame(app, canvas):
    if app.gameBeaten == True:
        x= app.width//2
        y = app.height//2
        canvas.create_text(x, y, text ='CONGRATS, YOU BEAT THE GAME!', fill = 'White',
                    font = 'Times 28 bold italic')

def drawUpInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.6
    canvas.create_text(x, y, text='Press UP Arrow Key to move up', fill = 'White',
                    font = 'Times 20  bold italic')

def drawDownInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.49
    canvas.create_text(x, y, text='Press DOWN Arrow Key to move down', fill = 'White',
                    font = 'Times 20  bold italic')

def drawLeftInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.38
    canvas.create_text(x, y, text='Press LEFT Arrow Key to move left', fill = 'White',
                    font = 'Times 20  bold italic')

def drawRightInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.29
    canvas.create_text(x, y, text='Press RIGHT Arrow Key to move right', fill = 'White',
                    font = 'Times 20  bold italic')

def drawRestartInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.22
    canvas.create_text(x, y, text='Press R Key to restart game', fill = 'White',
                    font = 'Times 20  bold italic')

def drawEndInstructions(app, canvas):
    x = app.width//2
    y = app.height//1.15
    canvas.create_text(x, y, text='Press F Key to end game', fill = 'White',
                    font = 'Times 20  bold italic')

def caution1(app, canvas):
    x = app.width//2
    y = app.height//16
    canvas.create_text(x, y, text='Warning 1, please wait for the ghost to start moving before moving pacman',
    fill = 'White', font = 'Time 12 bold italic')

def caution2(app, canvas):
    x = app.width//2
    y = app.height//10
    canvas.create_text(x, y, text='Warning 2, please do not spam the user inputs to prevent the game from freezing',
    fill = 'White', font = 'Time 12 bold italic')

def gameStart(app, canvas):
    drawGrid(app, canvas)
    drawPacMan(app, canvas)
    drawDot(app, canvas)
    drawPowerUp(app, canvas)
    drawScore(app, canvas)
    drawGameOver(app, canvas)
    drawBeatenGame(app, canvas)
    drawGhost1(app, canvas)
    caution1(app, canvas)
    caution2(app, canvas)

def moveInstructions(app, canvas):
    drawUpInstructions(app, canvas)
    drawDownInstructions(app, canvas)
    drawLeftInstructions(app, canvas)
    drawRightInstructions(app, canvas)
    drawRestartInstructions(app, canvas)
    drawEndInstructions(app, canvas)

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'dark blue')
    drawStartGame(app, canvas)
    moveInstructions(app, canvas)
    if app.startGame == True:
       gameStart(app, canvas)

def playPacMan():
    rows, cols, cellSize, margin = gameDimensions()
    width = (cols*cellSize) + margin *2
    height = (rows*cellSize) + margin * 2
    runApp(width=width, height=height)

playPacMan()
