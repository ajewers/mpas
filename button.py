from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QFont

# Encapsulates a simple button
class Button():
    def __init__(self, x, y, width, height, text, small):
        # Initialise position, size and text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        
        # Small boolean indicates how to render when hovered
        self.small = small
        
        # Hover boolean is true when the mouse is over the button
        self.hover = False
	
    # Determines if the mouse is currently over this button
    def checkHover(self, mouse):
        if mouse[0] >= self.x and mouse[0] < self.x + self.width and mouse[1] >= self.y and mouse[1] < self.y + self.height:
            self.hover = True
        else:
            self.hover = False
            
    # Draws this button
    def render(self, qp, colour):
        qp.setPen(QPen(QtCore.Qt.black, 4))
        qp.setFont(QFont("Arial", 18, 1, False))
        
        if self.small:
            self.renderSmall(qp, colour)
        else:
            self.renderNormal(qp, colour)
    
    # Draws this button in normal size
    def renderNormal(self, qp, colour):
        # When hovered the button is wider, and has a black indicator box
        if self.hover:
            qp.drawRect(self.x, self.y, self.width + 60, self.height)
            qp.fillRect(self.x + self.width + 10, self.y + 10, 40, 40, colour)
        else:
            qp.drawRect(self.x, self.y, self.width, self.height)
            
        # Render the button text
        qp.setFont(QFont("Arial", 18, 1, False))
        qp.drawText(self.x + 10, self.y, self.width, self.height, 0, self.text)
        
    # Draws this button in small size
    def renderSmall(self, qp, colour):
        # When hovered the button has an extra outer line
        if self.hover:
            qp.drawRect(self.x, self.y, self.width, self.height)
            qp.drawRect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
        else:
            qp.drawRect(self.x, self.y, self.width, self.height)
            
        # Render the button text
        qp.setFont(QFont("Arial", 14, 1, False))
        qp.drawText(self.x + 10, self.y, self.width, self.height, 0, self.text)
        