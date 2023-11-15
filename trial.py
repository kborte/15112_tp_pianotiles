import mechanics
from cmu_graphics import *
from utils import *
import random

def loadNewRow(app):
    # -1 is the bomb, 1 is a usual tile
    # while 2, 3, and 4 are "extra-press" tiles
    newRow = random.choices([-1, 0, 1, 2, 3, 4], 
                            weights=[1, 16, 12, 1, 1, 1], k = 3)
    
    while newRow == [0, 0, 0]:
        newRow = random.choices([-1, 0, 1, 2, 3, 4],
                       weights = [1, 16, 12, 2, 1, 1], k = 3)
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

def drawMenu(app):
    drawRect(app.width / 2, app.height / 2 - 50,
                 100, 50, fill = "white", border = "blue", align = "center")
    drawLabel("Classic", app.width / 2, app.height / 2 - 50)
    drawRect(app.width / 2, app.height / 2 + 50,
                 100, 50, fill = "white", border = "blue", align = "center")
    drawLabel("Infinite", app.width / 2, app.height / 2 + 50)
    
def drawClassicModeMenu(app):
    levels = ["song1", "song2", "song3"]

    for i in range(len(levels)):
        drawRect(app.width / 2, app.height / 2 - 50 + i * 50,
                 100, 50, border = "blue", align = "center")
        drawLabel(f"Level {i}", app.width / 2, 
                  app.height / 2 - 50 + i * 50)

    mechanics.play()

def gameOver(app):
    print('GameOver triggered', app.record, app.score)
    if app.record < app.score:
        app.recordFile.write(str(app.score))
        app.record = app.score
        app.newrecord = True

def drawGameOver(app):
    if app.mode == "infinite alone":
        drawLabel("Game Over!", app.width / 2, app.height / 2, fill = "red")
        drawLabel(f"Your score is {app.score}", app.width / 2, app.height / 2 + 20,
                fill = "red")
        drawRect(app.width / 2, app.height / 2 + 40, 60, 20, border = "blue", align = "center")
        drawLabel("Restart", app.width / 2, app.height / 2 + 40,
                fill = "red")
        
        if app.newRecord == True:
            drawLabel("You've set a new record", app.width / 2, app.height / 2 - 50)
    
def onStep(app):
    if app.mode == "infinite alone" and app.isGameOver == False:
        app.startingHeight += 1
        app.stepsMade += 1
        if (app.startingHeight
            >= app.height - app.margin):
            gameOver(app)
            app.isGameOver = True
        if app.stepsMade % app.cellSize == 1:
            loadNewRow(app)

def onKeyPress(app, key):
    keyLanes = {"a": 0, "s": 1, "d": 2,
                "left": 0, "down": 1, "right": 2}
    if app.mode == "infinite alone":
        if app.isGameOver == True:
            if key == "r":
                restart(app)
        else:
            if app.board[0][keyLanes[key]] >= 1:
                app.board[0][keyLanes[key]] -= 1
                app.score += 1
            else:
                gameOver(app)
                app.isGameOver = True

            if app.board[0] == [0, 0, 0]:
                app.board.pop(0)
                app.startingHeight -= app.cellSize

def infiniteModeMenu(app):
    drawRect(app.width / 2, app.height / 2 - 50,
             100, 50, fill = "white", 
             border = "blue", align = "center")
    drawLabel("Solo", app.width / 2, app.height / 2 - 50)
    drawRect(app.width / 2, app.height / 2 + 50, 
             100, 50, fill = "white",
             border = "blue", align = "center")
    drawLabel("Multiplayer", app.width / 2, app.height / 2 + 50)

def drawLayout(app):
    drawLabel("Piano tiles: the new realm", app.width / 2, app.margin / 2, fill = "red")
    drawMenu(app)

def drawInfiniteSoloLayout(app):
    drawBoard(app)
    drawRect(0, 0, app.width, app.margin, fill = "white")
    drawLabel(f'Your score is {app.score}', app.width / 2, app.margin / 2, fill = "red")

def onMousePress(app, mouseX, mouseY):
    if app.mode == "menu":
        if (app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and
            app.height / 2 - 75 <= mouseY <= app.height / 2 - 25):
            app.mode = "classic"
        elif (app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and
              app.height / 2 + 25 <= mouseY <= app.height / 2 + 75):
            app.mode = "infinite"
    elif app.mode == "infinite":
        if (app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and
            app.height / 2 - 75 <= mouseY <= app.height / 2 - 25):
            setDefaultValues(app)
            app.mode = "infinite alone"
        elif (app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and
              app.height / 2 + 25 <= mouseY <= app.height / 2 + 75):
            app.mode = "infinite multiplayer"
    if app.mode == "infinite alone" and app.isGameOver == True:
        if (app.width / 2 - 30 <= mouseX <= app.width / 2 + 30 and
            app.height / 2 + 30 <= mouseY <= app.height / 2 + 50):
            restart(app)
    # elif app.mode == "classic":

def redrawAll(app):
    if app.mode == "menu":
        drawLayout(app)
    elif app.mode == "classic":
        drawClassicModeMenu(app)
    elif app.mode == "infinite":
        infiniteModeMenu(app)
    elif app.mode == "infinite alone":
        if app.isGameOver == True:
            drawGameOver(app)
        else:
            drawInfiniteSoloLayout(app)
    elif app.mode == "infinite multiplayer":
        drawLabel("Coming soon", app.width / 2, app.height / 2)
    else:
        drawLabel("Classic mode coming soon", app.width / 2, app.height / 2)

def setDefaultValues(app):
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
    print(app.record)
    app.newRecord = False
    app.board = []
    loadNewRow(app)
    loadNewRow(app)
    app.startingHeight = app.margin + app.cellSize * len(app.board)

def onAppStart(app):
    app.background = "white"
    app.mode = "menu"
    app.margin = 60

if __name__ == "__main__":
    runApp(width = 360, height = 560)