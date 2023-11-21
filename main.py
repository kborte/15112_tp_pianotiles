from cmu_graphics import *
import random as rd
import json

class Button():
    def __init__(self, app, label = "Button", x = 100, y = 100, 
                 onPress = None, navigateTo = None, width = None, 
                 height = None, labelSize = 12, 
                 labelColor = "black", font = "montserrat",
                 backgroundColor = "white", borderColor = "blue", 
                 borderWidth = 1, buttonMargin = 0, 
                 bold = False, italic = False):
        self.label = label
        self.x = x
        self.y = y
        self.onPress = onPress
        self.app = app
        self.labelSize = labelSize
        self.labelColor = labelColor
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.buttonMargin = buttonMargin
        self.font = font
        if width != None:
            self.width = width
        elif hasattr(app, "buttonsWidth"):
            self.width = app.buttonsWidth
        else:
            self.width = len(self.label) * self.labelSize + self.buttonMargin
        if height != None:
            self.height = height
        elif hasattr(app, "buttonsHeight"):
            self.height = app.buttonsHeight
        else:
            self.height = self.labelSize + self.buttonMargin
        self.bold = bold
        self.italic = italic
        self.display = False
        self.navigateTo = navigateTo

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height,
            fill = self.backgroundColor, border = self.borderColor,
            borderWidth = self.borderWidth, align = "center"
            )
        drawLabel(self.label, self.x, self.y, fill = self.labelColor,
                  size = self.labelSize, font = self.font, bold = self.bold,
                  italic = self.italic)
        
    def press(self):
        if self.onPress != None:
            if type(self.onPress) == list:
                for func in self.onPress:
                    if func == changeMode and self.navigateTo != None:
                        func(self.app, self.navigateTo)
                    else:
                        func(self.app)
            else:
                if self.navigateTo != None:
                    self.onPress(self.app, self.navigateTo)
                else:
                    self.onPress(self.app)

def changeMode(app, newMode):
    if app.mode[:2] != ["infinite", "game"]:
        if app.buttons.get(f"{app.mode[0]}-{app.mode[1]}") != None:
            for button in app.buttons[f"{app.mode[0]}-{app.mode[1]}"].values():
                button.display = False
    else:
        if app.buttons.get(f"{app.mode[0]}-{app.mode[1]}-{app.mode[2]}") != None:
            for button in app.buttons[f"{app.mode[0]}-{app.mode[1]}-{app.mode[2]}"].values():
                button.display = False

    app.mode = newMode

    if app.mode[:2] != ["infinite", "game"]:
        setClassicGameVariables(app)
        if app.buttons.get(f"{app.mode[0]}-{app.mode[1]}") != None:
            for button in app.buttons[f"{app.mode[0]}-{app.mode[1]}"].values():
                button.display = True
    else:
        if app.mode[2] == "solo":
            setInfiniteSoloGameVariables(app)
        elif app.mode[2] == "multiplayer":
            setInfiniteMultiplayerGameVariables(app)
        if app.buttons.get(f"{app.mode[0]}-{app.mode[1]}-{app.mode[2]}") != None:
            for button in app.buttons[f"{app.mode[0]}-{app.mode[1]}-{app.mode[2]}"].values():
                button.display = True

def loadNewRowRandom(app):
    newRow = rd.choices([-1, 0, 1, 2, 3, 4], 
                            weights = [1, 8, 6, 1, 1, 1], k = 3)
    
    while newRow == [0, 0, 0] or newRow == [-1, -1, 1]:
        newRow = rd.choices([-1, 0, 1, 2, 3, 4],
                       weights = [1, 8, 6, 1, 1, 1], k = 3)
    app.board.append(newRow)

def drawCell(app, row, col, rowHeight = None):
    colors = ["blue", "green", "yellow", "orange"]
    if app.board[row][col] == -1:
        color = "red"
    else:
        color = colors[app.board[row][col] - 1]

    if rowHeight != None:
        x = app.margin + app.cellSize * col
        y = app.startingHeight - app.cellSize * (row + 1)
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

def setInfiniteSoloGameVariables(app):
    app.score = 0
    app.stepsPerSecond = 30
    app.stepsMade = 0
    app.width, app.height = 360, 560
    app.margin = 60
    app.cellSize = (app.width - app.margin * 2) // 3
    app.background = "white"
    app.isGameOver = False
    app.recordFile = open("record.txt", "r+")
    app.record = int(app.recordFile.read())
    app.newrecord = False
    app.board = []
    loadNewRowRandom(app)
    loadNewRowRandom(app)
    app.startingHeight = app.margin + app.cellSize * len(app.board)
    app.paused = False

def setInfiniteMultiplayerGameVariables(app):
    pass

def loadNewRowClassic(app):
    newRow = [0, 0, 0]
    newRow[random.randint(0, 2)] = 1
    rowHeight = app.songBeats[app.beatsPassed]
    app.board.append(newRow)
    app.rowHeights.append(rowHeight)

def setClassicGameVariables(app):
    app.rowHeights = []
    songBeatsFile = open("songbeats.json")
    dataBeats = json.load(songBeatsFile)["songs"]
    app.songBeats = dataBeats[app.mode[2]]["beats"]

    app.score = 0
    app.board = []
    loadNewRowClassic(app)
    loadNewRowClassic(app)
    app.previousScore = app.classicLevels[app.mode[2]]["score"]
    app.startingHeight = app.margin + app.cellSize * len(app.board)
    app.paused = False
    app.isGameOver = False

def pauseGame(app):
    if hasattr(app, "pause") and app.pause == True:
        for button in app.buttons["pause"].values():
            button.display = False

    app.paused = not app.paused

    if hasattr(app, "paused") and app.paused == True:
        for button in app.buttons["pause"].values():
            button.display = True

def setStarterMenuButtons(app):
    app.buttons["starter-menu"] = dict()
    app.buttons["starter-menu"]["starter-classic"] = Button(app = app, label = "Classic",
                                x = app.width / 2, y = app.buttonsHeightStart,
                                onPress = changeMode, navigateTo = ["classic", "menu"])
    app.buttons["starter-menu"]["starter-infinite"] = Button(app = app, label = "Infinite",
                                x = app.width / 2, y = app.height / 2 + app.buttonsHeight + app.menuButtonMargin,
                                width = 100, height = 50,
                                onPress = changeMode, navigateTo = ["infinite", "menu"])
    
def setClassicMenuButtons(app):
    starterX = app.margin 
    starterY = app.margin * 2
    columns = (app.width - app.margin * 2) // app.buttonsWidth
    app.buttons["classic-menu"] = dict()
    for levelNumber in range(len(app.classicLevels)):
        level = app.classicLevels[levelNumber]
        app.buttons["classic-menu"][levelNumber] = Button(app = app, label = level["label"],
                                x = starterX + (levelNumber % columns) * (app.buttonsWidth + app.buttonsMargin),
                                y = starterY + (levelNumber // columns) * (app.buttonsWidth + app.buttonsMargin),
                                onPress = changeMode, navigateTo = ["classic", "game", levelNumber])
    app.buttons["classic-menu"]["classic-back"] = Button(app = app, label = "Back",
                                x = app.margin / 2, y = app.margin / 2,
                                onPress = changeMode, navigateTo = ["starter", "menu"])
    
def setClassicGameButtons(app):
    app.buttons["classic-game"] = dict()
    app.buttons["classic-game"]["classic-back"] = Button(app = app, label = "Back",
                                x = app.margin / 2, y = app.margin / 2,
                                onPress = changeMode, navigateTo = ["classic", "menu"])
    app.buttons["classic-game"]["classic-pause"] = Button(app = app, label = "Pause",
                                x = app.width - app.margin / 2, y = app.margin / 2,
                                onPress = pauseGame)
    
def setInfiniteMenuButtons(app):
    app.buttons["infinite-menu"] = dict()
    app.buttons["infinite-menu"]["infinite-solo"] = Button(app = app, label = "Solo",
                                x = app.width / 2, y = app.buttonsHeightStart, 
                                onPress = changeMode, navigateTo = ["infinite", "game", "solo"])
    app.buttons["infinite-menu"]["infinite-multiplayer"] = Button(app = app, label = "Multiplayer",
                                x = app.width / 2, y =  app.buttonsHeightStart + app.buttonsHeight + app.menuButtonMargin,
                                onPress = changeMode, navigateTo = ["infinite", "game", "multiplayer"])
    app.buttons["infinite-menu"]["infinite-back"] = Button(app = app, label = "Back", 
                                x = app.margin / 2, y = app.margin / 2,
                                onPress = changeMode, navigateTo = ["starter", "menu"])
    
def setInfiniteSoloGameButtons(app):
    app.buttons["infinite-game-solo"] = dict()
    app.buttons["infinite-game-solo"]["infinite-solo-back"] = Button(app = app, label = "Back",
                                x = app.margin, y = app.margin, 
                                onPress = changeMode, navigateTo = ["infinite", "menu"])
    app.buttons["infinite-game-solo"]["infinite-solo-pause"] = Button(app = app, label = "Pause", 
                                x = app.width - app.margin, y = app.margin,
                                onPress = pauseGame)
    
def setInfiniteMultiplayerGameButtons(app):
    app.buttons["infinite-game-multiplayer"] = dict()
    app.buttons["infinite-game-multiplayer"]["infinite-multiplayer-giveup"] = Button(app = app, label = "Give Up",
                                onPress = gameOver)
    
def setPauseButtons(app):
    app.buttons["pause"] = dict()
    app.buttons["pause"]["pause-continue"] = Button(app = app, label = "Continue",
                                x = app.width / 2, y = app.height / 2 - 20,
                                onPress = pauseGame)
    app.buttons["pause"]["pause-restart"] = Button(app = app, label = "Restart",
                                x = app.width / 2, y = app.height / 2 + 50,
                                onPress = [fromPause, restart])
    app.buttons["pause"]["pause-giveup"] = Button(app = app, label = "Give Up",
                                x = app.width / 2, y = app.height / 2 + 120,
                                onPress = [fromPause, gameOver])
    app.buttons["pause"]["pause-menu"] = Button(app = app, label = "Back to Menu",
                                x = app.width / 2, y = app.height / 2 + 190,
                                onPress = [fromPause, changeMode], navigateTo = [app.mode[0]] + ["menu"])
    
def setGameOverButtons(app):
    app.buttons["gameover"] = dict()
    app.buttons["gameover"]["gameover-restart"] = Button(app = app, label = "Restart",
                                x = app.width / 2, y = app.height / 2 + 50,
                                onPress = [fromGameOver, restart])
    app.buttons["gameover"]["gameover-menu"] = Button(app = app, label = "Back to Menu",
                                x = app.width / 2, y = app.height / 2 + 120,
                                onPress = [fromGameOver, changeMode], navigateTo = [app.mode[0]] + ["menu"])
    
def fromGameOver(app):
    app.isGameOver = False
    for button in app.buttons["gameover"].values():
        button.display = False

def fromPause(app):
    app.paused = False
    for button in app.buttons["pause"].values():
        button.display = False

def setInfiniteGameButtons(app):
    setInfiniteSoloGameButtons(app)
    setInfiniteMultiplayerGameButtons(app)

def setButtons(app):
    app.buttons = dict()
    app.menuButtonMargin = 20
    setStarterMenuButtons(app)
    setClassicMenuButtons(app)
    setClassicGameButtons(app)
    setInfiniteMenuButtons(app)
    setInfiniteGameButtons(app)
    setPauseButtons(app)
    setGameOverButtons(app)
    app.buttons["instructionsButton"] = Button(app = app, label = "Game Rules",
                                               x = app.width - app.margin - app.buttonsWidth / 2,
                                               y = app.height - app.margin - app.buttonsHeight / 2,
                                               onPress = changeMode, navigateTo = app.mode + ["instructions"])

def onAppStart(app):
    app.background = "white"
    app.mode = ["starter", "menu"]
    app.buttonsHeightStart = app.height / 2
    app.buttonsHeight = 50
    app.buttonsWidth = 100
    app.buttonsMargin = 20
    app.margin = 60
    classicLevelsFile = open("classiclevels.json")
    app.classicLevels = json.load(classicLevelsFile)["songs"]
    classicLevelsFile.close()
    setButtons(app)
    app.buttons["starter-menu"]["starter-classic"].display = True
    app.buttons["starter-menu"]["starter-infinite"].display = True
    app.buttons["instructionsButton"].display = True

def onMousePress(app, mouseX, mouseY):
    modeStr = "-".join(app.mode)
    if hasattr(app, "paused") and app.paused == True:
        modeStr = "pause"
    if hasattr(app, "isGameOver") and app.isGameOver == True:
        modeStr = "gameover"
    for button in app.buttons[modeStr].values():
        bordersX = [button.x - button.width / 2, button.x + button.width / 2]
        bordersY = [button.y - button.height / 2, button.y + button.height / 2]
        print(button.label)
        if (button.display and 
            bordersX[0] <= mouseX <= bordersX[1]
            and bordersY[0] <= mouseY <= bordersY[1]):
            button.press()
    
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

def onClassicGameStep(app):
    pass

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

def classicGameOver(app):
    if app.score >= app.classicLevels[app.mode[2]]["score"]:
        app.classicLevels[app.mode[2]]["score"] = app.score
        classicLevelsFile = open("classiclevels.json", "w")
        json.dump({"songs": app.classicLevels}, classicLevelsFile)
        classicLevelsFile.close()

def infiniteSoloGameOver(app):
    if app.record < app.score:
        app.recordFile = open("record.txt", "w")
        app.recordFile.write(str(app.score))
        app.recordFile.close()
        app.record = app.score
        app.newrecord = True

def infiniteMultiplayerGameOver(app):
    app.won  = False

def gameOver(app):
    app.isGameOver = True
    for button in app.buttons["gameover"].values():
        button.display = True

    if app.mode[0] == "classic":
        classicGameOver(app)
    elif app.mode[0] == "infinite":
        if app.mode[2] == "solo":
            infiniteSoloGameOver(app)
        elif app.mode[2] == "multiplayer":
            infiniteMultiplayerGameOver(app)

def onKeyPress(app, key):
    keyLanes = {"a": 0, "s": 1, "d": 2,
                "left": 0, "down": 1, "right": 2}
    if app.isGameOver == True:
        if key == "r":
            restart(app)
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

def drawPause(app):
    drawLabel("Paused", app.width / 2, app.height / 2, fill = "red")
    drawLabel("Press any key to continue", app.width / 2, app.height / 2 - 160, fill = "red")
    drawLabel(f"Your score is {app.score}", app.width / 2, app.height / 2 - 90, fill = "red")
    for button in app.buttons["pause"].values():
        button.draw()

def restart(app):
    if app.mode[:2] == ["classic", "game"]:
        setClassicGameVariables(app)
    elif app.mode == ["infinite", "game", "solo"]:
        setInfiniteSoloGameVariables(app)
    elif app.mode == ["infinite", "game", "multiplayer"]:
        setInfiniteMultiplayerGameVariables(app)

def drawInfiniteSoloGame(app):
    if hasattr(app, "paused") and app.paused == True:
        drawPause(app)
    else:
        drawBoard(app)
        drawRect(0, 0, app.width, app.margin, fill = "white")
        for button in app.buttons["infinite-game-solo"].values():
            button.draw()
    drawLabel(f'Your score is {app.score}', app.width / 2, app.height - app.margin / 2, fill = "red")

def drawGame(app):
    if hasattr(app, "isGameOver") == False or app.isGameOver == False:
        if app.mode[0] == "classic":
            for button in app.buttons["classic-game"].values():
                button.draw()
        elif app.mode[0] == "infinite":
            if app.mode[2] == "solo":
                drawInfiniteSoloGame(app)
            elif app.mode[2] == "multiplayer":
                for button in app.buttons["infinite-game-multiplayer"].values():
                   button.draw()
    else:
        drawGameOver(app)

def redrawAll(app):
    if app.mode[1] == "menu":
        drawMenu(app)
    elif app.mode[1] == "game":
        drawGame(app)

runApp(width = 360, height = 560)