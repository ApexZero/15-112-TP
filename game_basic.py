from cmu_112_graphics import *
import math

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

from cmu_112_graphics import *

'STARTER INFORMATION'
def appStarted(app):
    rows, cols, cellSize, margin = gameDimensions()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.margin = margin
    app.pacColor = 'yellow'
    app.pacRow = 20
    app.pacCol = 15
    app.dotColor = 'blue'
    app.dotLocations = []
    createDots(app)
    app.score = 0


def gameDimensions():
    rows = 30
    cols = 30
    cellSize = 20
    margin = 50
    return rows, cols, cellSize, margin

'PACMAN MOVE'
def pacManMove(app, drow, dcol):
    app.pacRow += drow
    app.pacCol += dcol
    if pacMoveLegal(app) != True:
        app.pacRow -= drow
        app.pacCol -= dcol
    

def pacMoveLegal(app):
    if (app.pacRow < 0 or app.pacCol < 0 or app.pacRow >= app.rows or
    app.pacCol >= app.cols):
        return False
    return True


'CREATING DOTS AND ITEMS'
def createDots(app):
    for row in range(app.rows):
        for col in range(app.cols):
            coordinate = (row, col)
            if coordinate != (20,15):
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

def ghostStart(app, row ,col):
    return 42

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

'Point System'
def calculateScore(app):
    app.score += 10

'DRAW FUNCTIONS'
def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')

def drawPacMan(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.pacRow, app.pacCol)
    canvas.create_oval(x0, y0, x1, y1, fill = app.pacColor)

def drawDot(app, canvas):
    for (row, col) in app.dotLocations:
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill = app.dotColor)

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
    rows, cols, cellSize, margin = gameDimensions()
    width = (cols*cellSize)+(margin*2)
    height = (rows*cellSize) + (margin*2)
    runApp(width=width, height=height)

playPacMan()
