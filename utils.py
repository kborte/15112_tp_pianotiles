from cmu_graphics import *

class Button:
    def __init__(self, app, label = "Button", x = 100, y = 100, functionAtPress = None,
                 labelSize = 12, labelColor = "black", font = "montserrat", backgroundColor = "white", 
                 borderColor = "blue", borderWidth = 1, buttonMargin = 0, bold = False, italic = False):
        self.label = label
        self.x = x
        self.y = y
        self.functionAtPress = functionAtPress
        self.app = app
        self.labelSize = labelSize
        self.labelColor = labelColor
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.buttonMargin = buttonMargin
        self.font = font
        self.width = len(self.label) * self.labelSize + self.buttonMargin
        self.height = self.labelSize + self.buttonMargin
        self.bold = bold
        self.italic = italic

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height,
            fill = self.backgroundColor, border = self.borderColor,
            borderWidth = self.borderWidth, align = "center"
            )
        drawLabel(self.label, self.x, self.y, fill = self.labelColor,
                  size = self.labelSize, font = self.font, bold = self.bold,
                  italic = self.italic)

    def press(self):
        if self.functionAtPress != None:
            self.functionAtPress(self.app)

#usage examples

# def onAppStart(app):
#     app.mode = 1
#     setMenuButtons1(app)

# def changeMode(app):
#     app.mode = 2

# def drawMenu1(app):
#     app.b.draw()
#     app.c.draw()

# def drawMenu2(app):
#     app.d.draw()
#     app.e.draw()

# def setMenuButtons1(app):
#     app.b = Button(label="test", x = 100, y = 100, functionAtPress=changeMode, app=app)
#     app.c = Button(label="menu2", x = app.width / 2, y = app.width / 2, app=app)
#     app.d = Button(app=app)
#     app.e = Button(app=app, label="Button2")

# def onMousePress(app, mouseX, mouseY):
#     if (app.mode == 1 and app.b.x - app.b.width / 2 <= mouseX <= app.b.x + app.b.width / 2
#         and app.b.y - app.b.height / 2 <= mouseY <= app.b.y + app.b.height / 2):
#         app.b.press()

# def redrawAll(app):
#     if app.mode == 1:
#         drawMenu1(app)
#     elif app.mode == 2:
#         drawMenu2(app)

# runApp()