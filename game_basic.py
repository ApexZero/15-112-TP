from cmu_112_graphics import *
import math
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
    rows, cols, cellSize = gameDimensions()
    app.board = gameMap()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.pacColor = 'yellow'
    app.pacRow = 23
    app.pacCol = 14
    app.dotColor = 'orange'
    app.dotLocations = []
    createDots(app)
    app.score = 0
    app.wallColor = 'blue'
    app.pathColor = 'grey'
    app.blankColor = 'black'
    app.entranceColor = 'red'
    app.ghost1Row = 14
    app.ghost1Col = 12
    app.ghost1Color = 'pink'


def gameDimensions():
    rows = 31
    cols = 28
    cellSize = 20
    return rows, cols, cellSize


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
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','e','e','w','w','w','p','w','w','p','w','n','n','n','n','n'],
     ['w','w','w','w','w','w','p','w','w','p','w','s','s','s','s','s','s','w','p','w','w','p','w','w','w','w','w','w'],
     ['p','p','p','p','p','p','p','p','p','p','w','s','s','s','s','s','s','w','p','p','p','p','p','p','p','p','p','p'],
     ['w','w','w','w','w','w','p','w','w','p','w','s','s','s','s','s','s','w','p','w','w','p','w','w','w','w','w','w'],
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','w','w','w','w','w','p','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','p','p','p','p','p','p','p','p','p','w','w','p','w','n','n','n','n','n'],
     ['n','n','n','n','n','w','p','w','w','p','w','w','w','w','w','w','w','w','w','w','w','p','w','n','n','n','n','n'],
     ['w','w','w','w','w','w','p','w','w','p','w','w','w','w','w','w','w','w','w','w','w','p','w','w','w','w','w','w'],
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
    or app.board[app.pacRow][app.pacCol] == 'e'):
        return False
    return True


'CREATING DOTS AND ITEMS'
def createDots(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 'p':
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
    gridWidth  = app.width
    gridHeight = app.height
    x0 = col * gridWidth / app.cols
    x1 = (col+1) * gridWidth / app.cols
    y0 = row * gridHeight / app.rows
    y1 = (row+1) * gridHeight / app.rows
    return (x0, y0, x1, y1)


'USER INTERFACE'
def keyPressed(app, event):
    drow = 0
    dcol = 0
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
    pacManMove(app, drow, dcol)
    checkDotPacCollision(app)

'Ghost Movement'
def ghostMove(app):
    start = app.board[app.ghost1Row][app.ghost1Col]
    goal = app.board[app.pacRow][app.pacCol]
    AStar(app.board, start, goal)

def ghostLegal(app):
    if (app.ghost1Row < 0 or app.ghost1Col < 0 or app.ghost1Row >= app.rows
    or app.ghost1Col >= app.cols or app.board[app.ghost1Row][app.ghost1Col] == 'w'):
        return False
    return True

def timerFired(app):
    ghostMove(app)
    if ghostLegal(app) != True:
        return 42
        
'Point System'
def calculateScore(app):
    app.score += 10

'DRAW FUNCTIONS'
def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            if app.board[row][col] == 'w':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.wallColor)
            elif app.board[row][col] == 'p':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.pathColor)
            elif app.board[row][col] == 'n':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.blankColor)
            elif app.board[row][col] == 's':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.pathColor)
            elif app.board[row][col] == 'e':
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.entranceColor)

def drawPacMan(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.pacRow, app.pacCol)
    canvas.create_oval(x0, y0, x1, y1, fill = app.pacColor)

def drawDot(app, canvas):
    for (row, col) in app.dotLocations:
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        canvas.create_oval(x0+6.5, y0+6.5, x1-6.5, y1-6.5, fill = app.dotColor)

def drawScore(app, canvas):
    x = app.width//2
    y = app.height//30
    canvas.create_text(x, y, text = f'Score = {app.score}', fill = 'White',
                        font = 'Times 18 bold')

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'orange')
    drawGrid(app, canvas)
    drawDot(app, canvas)
    drawPacMan(app, canvas)
    drawScore(app, canvas)

def playPacMan():
    rows, cols, cellSize = gameDimensions()
    width = (cols*cellSize)
    height = (rows*cellSize)
    runApp(width=width, height=height)

playPacMan()
