from cmu_graphics import *

class button:
    def __init__(self, label, x, y, width, height, functionAtPress):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.functionAtPress = functionAtPress

        drawRect(self.x, self.y, self.width, self.height, 
                 border = "blue", align = "center")
        drawLabel(self.label, self.x, self.y)
    
    # def buttonPressed(self, onMousePress):
    #     if (self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and
    #         self.y - self.height / 2 <= mouseY <= self.y + self.height / 2):