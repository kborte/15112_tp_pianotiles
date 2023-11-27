from cmu_graphics import *
import random as rd
import json

class Button:
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
        if app.mode[:2] == ["classic", "game"]:
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

def setClassicGameVariables(app):
    app.won = None
    app.cellSize = (app.width - app.margin * 2) // 3
    app.rowHeights = []
    songBeatsFile = open("songbeats.json")
    dataBeats = dict(json.load(songBeatsFile)["songs"])
    print(dataBeats, app.mode[2])
    app.songBeats = dataBeats[str(app.mode[2])]

    app.score = 0
    app.board = []
    app.beatsPassed = 0
    i = 0

    while i < len(app.songBeats):
        loadNewRowClassic(app, i)
        i += 1

    app.previousScore = app.classicLevels[app.mode[2]]["score"]
    app.startingHeight = app.margin + app.cellSize * 3
    app.paused = False
    app.isGameOver = False
    app.stepsMade = 0

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

def loadNewRowClassic(app, beat):
    newRow = [0, 0, 0]
    newRow[rd.randint(0, 2)] = 1
    if beat == 0:
        rowHeight = app.songBeats[beat]
    else:
        rowHeight = (app.songBeats[beat] - app.songBeats[beat - 1]) * 50
    app.board.append(newRow)
    app.rowHeights.append(rowHeight)

def loadNewRowRandom(app):
    newRow = rd.choices([-1, 0, 1, 2, 3, 4], 
                            weights = [1, 8, 6, 1, 1, 1], k = 3)
    
    while newRow == [0, 0, 0] or newRow == [-1, -1, 1]:
        newRow = rd.choices([-1, 0, 1, 2, 3, 4],
                       weights = [1, 8, 6, 1, 1, 1], k = 3)
    app.board.append(newRow)

def pauseGame(app):
    if hasattr(app, "pause") and app.pause == True:
        for button in app.buttons["pause"].values():
            button.display = False

    app.paused = not app.paused

    if hasattr(app, "paused") and app.paused == True:
        for button in app.buttons["pause"].values():
            button.display = True

def restart(app):
    if app.mode[:2] == ["classic", "game"]:
        setClassicGameVariables(app)
    elif app.mode == ["infinite", "game", "solo"]:
        setInfiniteSoloGameVariables(app)
    elif app.mode == ["infinite", "game", "multiplayer"]:
        setInfiniteMultiplayerGameVariables(app)

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

def fromGameOver(app):
    app.isGameOver = False
    for button in app.buttons["gameover"].values():
        button.display = False

def fromPause(app):
    app.paused = False
    for button in app.buttons["pause"].values():
        button.display = False

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
    
def onMousePress(app, mouseX, mouseY):
    if app.mode[:2] == ["classic", "game"]:
        modeStr = "classic-game"
    else:
        modeStr = "-".join(app.mode)
    if hasattr(app, "paused") and app.paused == True:
        modeStr = "pause"
    if hasattr(app, "isGameOver") and app.isGameOver == True:
        modeStr = "gameover"
    for button in app.buttons[modeStr].values():
        bordersX = [button.x - button.width / 2, button.x + button.width / 2]
        bordersY = [button.y - button.height / 2, button.y + button.height / 2]
        # print(button.label)
        if (button.display and 
            bordersX[0] <= mouseX <= bordersX[1]
            and bordersY[0] <= mouseY <= bordersY[1]):
            button.press()

def setStarterVariables(app):
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