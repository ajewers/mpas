from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QFont

class Button():
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        
        self.hover = False
	
    def checkHover(self, mouse):
        if mouse[0] >= self.x and mouse[0] < self.x + self.width and mouse[1] >= self.y and mouse[1] < self.y + self.height:
            self.hover = True
        else:
            self.hover = False
            
    def render(self, qp, colour):
        qp.setPen(QPen(QtCore.Qt.black, 4))
        qp.setFont(QFont("Arial", 18, 1, False))
    
        if self.hover:
            qp.drawRect(self.x, self.y, self.width + 60, self.height)
            qp.fillRect(self.x + self.width + 10, self.y + 10, 40, 40, colour)
        else:
            qp.drawRect(self.x, self.y, self.width, self.height)
            
        qp.drawText(self.x, self.y, self.width, self.height, 0, self.text)