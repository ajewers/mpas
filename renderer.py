import sys
import copy
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QFont

class Renderer():
    def renderMainMenu(self, qp, tempoButton, metroButton):
        qp.setFont(QFont("Arial", 48, 2, False))
        qp.drawText(200, 350, 1000, 1000, 0, "PyTempo")
        
        qp.setFont(QFont("Arial", 18, 1, False))
        qp.drawText(900, 300, 500, 500, 0, "Menu:")
        
        tempoButton.render(qp, QtCore.Qt.black)
        metroButton.render(qp, QtCore.Qt.black)
    
    def renderTempoDetect(self, qp, energyQueue, beatQueue, energyAverage, bpm, backButton):
        for i, e in enumerate(energyQueue):
            if beatQueue[i]:
                qp.setPen(QPen(QtCore.Qt.red, 10))
            else:
                qp.setPen(QPen(QtCore.Qt.black, 10))
            
            qp.drawLine(100 + i * 10, 800, 100 + i * 10, 800 - 200 * e)
        
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(560, 800, 560, 800 - 200 * energyAverage)
        qp.drawText(560, 850, 200, 40, 0, "" + str(energyAverage))
        
        qp.setFont(QFont("Arial", 48, 2, False))
        
        if bpm > 0:
            qp.drawText(700, 400, 1000, 1000, 0, "BPM: " + "{0:.1f}".format(bpm))
        else:
            qp.drawText(700, 400, 1000, 1000, 0, "Listening...")
            
        backButton.render(qp, QtCore.Qt.black)
        
    def renderLiveMetronome(self, qp, backButton):
        backButton.render(qp, QtCore.Qt.black)
