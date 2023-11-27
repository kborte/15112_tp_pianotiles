from cmu_graphics import *
from control import gameOver, loadNewRowRandom, restart

def onClassicGameStep(app):
    if app.isGameOver == False:
        app.startingHeight += 1
        if (app.startingHeight
            >= app.height - app.margin):
            app.isGameOver = True
            app.won = False
            gameOver(app)
    
def onInfiniteSoloGameStep(app):
    if app.isGameOver == False:
        app.startingHeight += 1
        app.stepsMade += 1
        if (app.startingHeight
            >= app.height - app.margin):
            app.isGameOver = True
        if app.stepsMade % app.cellSize == 1:
            loadNewRowRandom(app)

def onInfiniteMultiplayerGameStep(app):
    pass

def convertModeToString(app):
    if hasattr(app, "paused") and app.paused == True:
        modeStr = "pause"
    elif hasattr(app, "isGameOver") and app.isGameOver == True:
        modeStr = "gameover"
    elif hasattr(app, "mode"):
        if app.mode[:2] == ["classic", "game"]:
            modeStr = "classic-game"
        else:
            modeStr = "-".join(app.mode)

    return modeStr

def onClassicGameKeyPress(app, key, keyLanes):
    if len(app.board) > 0:
        if key == "space":
            if sum(app.board[0]) < 0:
                app.board.pop(0)
                app.startingHeight -= app.rowHeights[0]
                app.rowHeights.pop(0)
            else:
                gameOver(app)
                app.isGameOver = True
        elif keyLanes.get(key) != None:    
            if app.board[0][keyLanes[key]] >= 1:
                app.board[0][keyLanes[key]] -= 1
                app.score += 1
            else:
                gameOver(app)
                app.isGameOver = True

            if app.board[0] == [0, 0, 0]:
                app.board.pop(0)
                app.startingHeight -= app.rowHeights[0]
                app.rowHeights.pop(0)
        if len(app.board) == 0:
            app.isGameOver = True
            app.won = True
            gameOver(app)

def onGameKeyPress(app, key):
    keyLanes = {"a": 0, "s": 1, "d": 2,
                "left": 0, "down": 1, "right": 2}
    if app.isGameOver == True:
        if key == "r":
            restart(app)
    else:
        if app.mode[:2] == ["classic", "game"]:
            onClassicGameKeyPress(app, key, keyLanes)
        else:
            if key == "space":
                if sum(app.board[0]) < 0:
                    app.board.pop(0)
                    app.startingHeight -= app.cellSize
                else:
                    gameOver(app)
                    app.isGameOver = True
            elif keyLanes.get(key) != None:    
                if app.board[0][keyLanes[key]] >= 1:
                    app.board[0][keyLanes[key]] -= 1
                    app.score += 1
                else:
                    gameOver(app)
                    app.isGameOver = True

                if app.board[0] == [0, 0, 0]:
                    app.board.pop(0)
                    app.startingHeight -= app.cellSize