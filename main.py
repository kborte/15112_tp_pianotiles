from cmu_graphics import *
from visual import drawMenu, drawGame
from control import setStarterVariables
from utils import (onClassicGameStep, onInfiniteSoloGameStep, onInfiniteMultiplayerGameStep, 
                   convertModeToString, onGameKeyPress)
import json

def onAppStart(app):
    setStarterVariables(app)

def redrawAll(app):
    if hasattr(app, "mode"):
        if app.mode[1] == "menu":
            drawMenu(app)
        elif app.mode[1] == "game":
            drawGame(app)

def onStep(app):
    if (app.mode[1] == "game" and app.paused == False 
        and app.isGameOver == False):
        if app.mode[0] == "classic":
            onClassicGameStep(app)
        elif app.mode[0] == "infinite":
            if app.mode[2] == "solo":
                onInfiniteSoloGameStep(app)
            if app.mode[2] == "multiplayer":
                onInfiniteMultiplayerGameStep(app)

def onMousePress(app, mouseX, mouseY):
    modeStr = convertModeToString(app)
    for button in app.buttons[modeStr].values():
        bordersX = [button.x - button.width / 2, button.x + button.width / 2]
        bordersY = [button.y - button.height / 2, button.y + button.height / 2]
        # print(button.label)
        if (button.display and 
            bordersX[0] <= mouseX <= bordersX[1]
            and bordersY[0] <= mouseY <= bordersY[1]):
            button.press()

def onKeyPress(app, key):
    onGameKeyPress(app, key)

runApp(width = 360, height = 560)