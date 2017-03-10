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
    
    def renderTempoDetect(self, qp, energyQueue, peakQueue, energyAverage, bpm, backButton):
        for i, e in enumerate(energyQueue):
            if peakQueue[i]:
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
        
    def renderLiveMetronome(self, qp, backButton, metro):
        backButton.render(qp, QtCore.Qt.black)
        metro.tempoUpButton.render(qp, QtCore.Qt.black)
        metro.tempoDownButton.render(qp, QtCore.Qt.black)
        metro.tempoUpPlusButton.render(qp, QtCore.Qt.black)
        metro.tempoDownPlusButton.render(qp, QtCore.Qt.black)
        qp.drawText(1200, 110, 1000, 1000, 0, "BPM: " + str(metro.bpm))
        
        qp.setPen(QPen(QtCore.Qt.gray, 10))
        for i, e in enumerate(metro.energyQueue):
            height = 10 * e
            if height > 200:
                height = 200
            
            qp.drawLine(800 - (i * 10), 700, 800 - (i * 10), 700 - height)
        
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(10, 700, 1590, 700)
        qp.drawLine(800, 400, 800, 700)
        
        qp.drawLine(10, 800, 1590, 800)
        qp.drawLine(800, 800, 800, 1100)
        
        for i, p in enumerate(metro.peakQueue):
            if i > 85:
                break
        
            if p:
                qp.drawLine(800 - (i * 10), 400, 800 - (i * 10), 700)
                
        beatQueue = copy.deepcopy(metro.beatQueue)
        for i, b in enumerate(beatQueue):
            if b:
                qp.drawLine(800 + ((i - 86) * 10), 800, 800 + ((i - 86) * 10), 1100)
                
        
