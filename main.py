import mechanics
from cmu_graphics import *
from utils import *

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
            app.mode = "infinite alone"
        elif (app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and
              app.height / 2 + 25 <= mouseY <= app.height / 2 + 75):
            app.mode = "infinite multiplayer"
    # elif app.mode == "classic":
        

def redrawAll(app):
    if app.mode == "menu":
        drawLayout(app)
    elif app.mode == "classic":
        drawClassicModeMenu(app)
    elif app.mode == "infinite":
        infiniteModeMenu(app)
    elif app.mode == "infinite alone":
        mechanics.onAppStart(app)
        # mechanics.onStep(app)
        mechanics.redrawAll(app)
    elif app.mode == "infinite multiplayer":
        drawLabel("Coming soon", app.width / 2, app.height / 2)
    else:
        drawLabel("Classic mode coming soon", app.width / 2, app.height / 2)

def onAppStart(app):
    app.background = "white"
    app.mode = "menu"
    app.margin = 60

if __name__ == "__main__":
    runApp(width = 360, height = 560)