from cmu_graphics import *

def drawCell(app, row, col, rowHeight = None):
    colors = ["blue", "green", "yellow", "orange"]
    if app.board[row][col] == -1:
        color = "red"
    else:
        color = colors[app.board[row][col] - 1]

    if rowHeight != None:
        x = app.margin + app.cellSize * col
        y = app.startingHeight - sum(app.rowHeights[:row + 1])
        drawRect(x, y,
                    app.cellSize,
                    rowHeight,
                    fill = color)
    else:
        x = app.margin + app.cellSize * col
        y = app.startingHeight - app.cellSize * (row + 1)
        drawRect(x, y,
                    app.cellSize,
                    app.cellSize,
                    fill = color)
    
def drawInfiniteBoard(app):
    if hasattr(app, "board"):
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if app.board[row][col] != 0:
                    drawCell(app, row, col)

def drawClassicBoard(app):
    if hasattr(app, "board"):
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if app.board[row][col] != 0:
                    drawCell(app, row, col, app.rowHeights[row])

def drawPause(app):
    drawLabel("Paused", app.width / 2, app.height / 2, fill = "red")
    drawLabel("Press any key to continue", app.width / 2, app.height / 2 - 160, fill = "red")
    drawLabel(f"Your score is {app.score}", app.width / 2, app.height / 2 - 90, fill = "red")
    for button in app.buttons["pause"].values():
        button.draw()

def drawMenu(app):
    for button in app.buttons[f"{app.mode[0]}-menu"].values():
        button.draw()

    app.buttons["instructionsButton"].draw()

def drawClassicGameOver(app):
    drawLabel(f"Level {app.mode[2]}", app.width / 2, app.height / 2 - 100, fill = "red")
    drawLabel(f'Your score is {app.score}', app.width / 2, app.margin / 2, fill = "red")

def drawInfiniteSoloGameOver(app):
    if app.newrecord == True:
        drawLabel("New Record!", app.width / 2, app.height / 2 - 100, fill = "red")
    drawLabel(f'Your score is {app.score}', app.width / 2, app.margin / 2, fill = "red")
    for button in app.buttons["gameover"].values():
        button.draw()

def drawInfiniteMultiplayerGameOver(app):
    drawLabel(f'Your score is {app.score}', app.width / 2, app.width / 2, fill = "red")
    drawLabel(f"Opponent's score is {app.opponentScore}", app.width / 2, 
              app.height / 2 + 50, fill = "red")
    if app.won == True:
        drawLabel("You won", app.width / 2, app.margin / 2, fill = "red")
    else:
        drawLabel("You lost", app.width / 2, app.margin / 2, fill = "red")

def drawGameOver(app):
    drawLabel("Game Over", app.width / 2, app.height / 2 - 150, fill = "red")
    if app.mode[0] == "classic":
        drawClassicGameOver(app)
    elif app.mode[0] == "infinite":
        if app.mode[2] == "solo":
            drawInfiniteSoloGameOver(app)
        elif app.mode[2] == "multiplayer":
            drawInfiniteMultiplayerGameOver(app)

def drawPause(app):
    drawLabel("Paused", app.width / 2, app.height / 2, fill = "red")
    drawLabel("Press any key to continue", app.width / 2, app.height / 2 - 160, fill = "red")
    drawLabel(f"Your score is {app.score}", app.width / 2, app.height / 2 - 90, fill = "red")
    for button in app.buttons["pause"].values():
        button.draw()

def drawInfiniteSoloGame(app):
    if hasattr(app, "paused") and app.paused == True:
        drawPause(app)
    else:
        drawInfiniteBoard(app)
        drawRect(0, 0, app.width, app.margin, fill = "white")
        for button in app.buttons["infinite-game-solo"].values():
            button.draw()
    drawLabel(f'Your score is {app.score}', app.width / 2, app.height - app.margin / 2, fill = "red")

def drawClassicGame(app):
    if hasattr(app, "paused") and app.paused == True:
        drawPause(app)
    else:
        drawClassicBoard(app)
        drawRect(0, 0, app.width, app.margin, fill = "white")
        for button in app.buttons["classic-game"].values():
            button.draw()
    drawLabel(f'Your score is {app.score}', app.width / 2, app.height - app.margin / 2, fill = "red")

def drawGame(app):
    if hasattr(app, "isGameOver") == False or app.isGameOver == False:
        if app.mode[0] == "classic":
            drawClassicGame(app)
        elif app.mode[0] == "infinite":
            if app.mode[2] == "solo":
                drawInfiniteSoloGame(app)
            elif app.mode[2] == "multiplayer":
                for button in app.buttons["infinite-game-multiplayer"].values():
                   button.draw()
    else:
        drawGameOver(app)