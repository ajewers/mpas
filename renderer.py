import sys
import copy
import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QFont, QColor

# Class for rendering the UIs of the different modes
class Renderer():
    # Renders the main menu
    def renderMainMenu(self, qp, tempoButton, metroButton):
        # Main title
        qp.setFont(QFont("Arial", 48, 2, False))
        qp.drawText(200, 350, 1000, 1000, 0, "PyTempo")
        
        # Menu label
        qp.setFont(QFont("Arial", 18, 1, False))
        qp.drawText(900, 300, 500, 500, 0, "Menu:")
        
        # Mode buttons
        tempoButton.render(qp, QtCore.Qt.black)
        metroButton.render(qp, QtCore.Qt.black)
    
    # Renders the tempo detection UI
    def renderTempoDetect(self, qp, energyQueue, peakQueue, energyAverage, bpm, backButton):
        # Render the energy waveform bars
        for i, e in enumerate(energyQueue):
            if peakQueue[i]:
                # Red if a peak is detected
                qp.setPen(QPen(QtCore.Qt.red, 10))
            else:
                qp.setPen(QPen(QtCore.Qt.black, 10))
            
            qp.drawLine(100 + i * 10, 800, 100 + i * 10, 800 - 200 * e)
        
        # Render the average energy bar
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(560, 800, 560, 800 - 200 * energyAverage)
        
        # Set the font
        qp.setFont(QFont("Arial", 48, 2, False))
        
        # Render the detected BPM, or 'Listening...' if none detected
        if bpm > 0:
            qp.drawText(700, 400, 1000, 1000, 0, "BPM: " + "{0:.1f}".format(bpm))
        else:
            qp.drawText(700, 400, 1000, 1000, 0, "Listening...")
            
        # Render the back button
        backButton.render(qp, QtCore.Qt.black)
        
    # Renders the active metronome UI
    def renderActiveMetronome(self, qp, backButton, metro):
        # Render the back button
        backButton.render(qp, QtCore.Qt.black)
        
        # Render the BPM selection buttons
        metro.tempoUpButton.render(qp, QtCore.Qt.black)
        metro.tempoDownButton.render(qp, QtCore.Qt.black)
        metro.tempoUpPlusButton.render(qp, QtCore.Qt.black)
        metro.tempoDownPlusButton.render(qp, QtCore.Qt.black)
        
        # Render the target BPM
        qp.drawText(1200, 110, 1000, 1000, 0, "BPM: " + str(metro.bpm))
        
        # Render the energy waveform in grey
        qp.setPen(QPen(QtCore.Qt.gray, 10))
        for i, e in enumerate(metro.energyQueue):
            height = 10 * e
            if height > 200:
                height = 200
            
            qp.drawLine(800 - (i * 10), 700, 800 - (i * 10), 700 - height)
        
        # Draw parallel horizontal lines for timeline
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(10, 700, 1590, 700)
        qp.drawLine(10, 800, 1590, 800)
        
        # Draw current instant dotted line
        qp.setPen(QPen(QtCore.Qt.black, 10, QtCore.Qt.DashLine))
        qp.drawLine(800, 400, 800, 700)
        qp.drawLine(800, 800, 800, 1100)
        
        # Render each of the detected peaks in black
        qp.setPen(QPen(QtCore.Qt.black, 10))
        for i, p in enumerate(metro.peakQueue):
            if i > 85:
                break
        
            if p:
                x = 800 - (i * 10)
                qp.drawLine(x, 400, x, 700)
                
                # Calculate accuracy
                diff = metro.getAccuracy(i) - 1
                if math.fabs(diff) < 20:
                    # Determine colour coding
                    if math.fabs(diff) < 3:
                        qp.setPen(QPen(QtCore.Qt.green, 10))
                    elif math.fabs(diff) < 10:
                        qp.setPen(QPen(QColor(255, 174, 0), 10))
                    else:
                        qp.setPen(QPen(QtCore.Qt.red, 10))
                        
                    # Render accuracy indicators
                    qp.drawLine(x, 710, x, 740)
                    qp.drawLine(x - (diff * 10), 760, x - (diff * 10), 800)
                    
                    # Return to black pen
                    qp.setPen(QPen(QtCore.Qt.black, 10))
        
        # Render a line for each of the metronome beats on the lower line
        beatQueue = copy.deepcopy(metro.beatQueue)
        for i, b in enumerate(beatQueue):
            if b:
                qp.drawLine(800 - ((i - 86) * 10), 800, 800 - ((i - 86) * 10), 1100)
                
        
