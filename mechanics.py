from cmu_graphics import *
import random

def loadNewRow(app):
    # -1 is the bomb, 1 is a usual tile
    # while 2, 3, and 4 are "extra-press" tiles
    newRow = random.choices([-1, 0, 1, 2, 3, 4], 
                            weights=[1, 8, 6, 1, 1, 1], k = 3)
    
    while newRow == [0, 0, 0]:
        newRow = random.choices([-1, 0, 1, 2, 3, 4],
                       weights = [1, 8, 6, 1, 1, 1], k = 3)
    app.board.append(newRow)

def drawCell(app, row, col):
    # setting the color of the cell according to its type
    colors = ["blue", "green", "yellow", "orange"]
    if app.board[row][col] == -1:
        color = "red"
    else:
        color = colors[app.board[row][col] - 1]

    x = app.margin + app.cellSize * col
    y = app.startingHeight - app.cellSize * (row + 1)
    drawRect(x, y,
                    app.cellSize,
                    app.cellSize,
                    fill = color)
    
def drawBoard(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] != 0:
                drawCell(app, row, col)

def restart(app):
    app.score = 0
    app.board = []
    loadNewRow(app)
    app.startingHeight = app.margin + app.cellSize * len(app.board)
    app.isGameOver = False

def gameOver(app):
    if app.record < app.score:
        app.recordFile.write(str(app.score))
        app.record = app.score
        app.newrecord = True

def drawGameOver(app):
    drawLabel("Game Over!", app.width / 2, app.height / 2, fill = "red")
    drawLabel(f"Your score is {app.score}", app.width / 2, app.height / 2 + 20,
              fill = "red")
    drawRect(app.width / 2, app.height / 2 + 40, 60, 20, border = "blue", align = "center")
    drawLabel("Restart", app.width / 2, app.height / 2 + 40,
               fill = "red")

def onStep(app):
    if app.isGameOver == False:
        app.startingHeight += 1
        app.stepsMade += 1
        if (app.startingHeight
            >= app.height - app.margin):
            app.isGameOver = True
        if app.stepsMade % app.cellSize == 1:
            loadNewRow(app)

def onKeyPress(app, key):
    keyLanes = {"a": 0, "s": 1, "d": 2,
                "left": 0, "down": 1, "right": 2}
    if app.isGameOver == True:
        if key == "r":
            restart(app)
    else:
        if app.board[0][keyLanes[key]] >= 1:
            app.board[0][keyLanes[key]] -= 1
            app.score += 1
        else:
            app.isGameOver = True

        if app.board[0] == [0, 0, 0]:
            app.board.pop(0)
            app.startingHeight -= app.cellSize

def onMousePress(app, mouseX, mouseY):
    if app.isGameOver == True:
        if (app.width / 2 - 30 <= mouseX <= app.width / 2 + 30 and
            app.height / 2 + 30 <= mouseY <= app.height / 2 + 50):
            restart(app)

def onAppStart(app):
    app.score = 0
    app.stepsPerSecond = 30
    app.stepsMade = 0
    app.width, app.height = 360, 560
    app.background = "white"
    app.margin = 60
    app.cellSize = (app.width - app.margin * 2) // 3
    app.background = "white"
    app.isGameOver = False
    app.recordFile = open("record.txt", "r+")
    app.record = int(app.recordFile.read())
    app.newrecord = False
    # app.board = [[0 for i in range (3)] for i in range(6)]
    app.board = []
    loadNewRow(app)
    loadNewRow(app)
    app.startingHeight = app.margin + app.cellSize * len(app.board)
    print(app.startingHeight)

def drawLayout(app):
    drawBoard(app)
    drawRect(0, 0, app.width, app.margin, fill = "white")
    drawLabel(f'Your score is {app.score}', app.width / 2, app.margin / 2, fill = "red")

def redrawAll(app):
    if app.isGameOver == True:
        drawGameOver(app)
    else:
        drawLayout(app)

def play():
    runApp()