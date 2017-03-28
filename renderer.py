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
            
            qp.drawLine(160 + i * 10, 800, 160 + i * 10, 800 - 100 * e)
        
        # Render the average energy bar
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(680, 800, 680, 800 - 200 * energyAverage)
        
        # Set the font
        qp.setFont(QFont("Arial", 48, 2, False))
        
        # Render the detected BPM, or 'Listening...' if none detected
        if bpm > 0:
            qp.drawText(850, 400, 1000, 1000, 0, "BPM: " + "{0:.1f}".format(bpm))
        else:
            qp.drawText(850, 400, 1000, 1000, 0, "Listening...")
            
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
        qp.setFont(QFont("Arial", 20, 1, False))
        qp.drawText(950, 45, 1000, 1000, 0, "BPM: " + str(metro.bpm))
        
        # Render the energy waveform in grey. Do this first so it is behind the rest.
        qp.setPen(QPen(QtCore.Qt.gray, 10))
        for i, e in enumerate(metro.energyQueue):
            height = 8 * e
            if height > 150:
                height = 150
            
            qp.drawLine(800 - (i * 10), 500, 800 - (i * 10), 500 - height)
        
        # Draw parallel horizontal lines for timeline
        qp.setPen(QPen(QtCore.Qt.black, 10))
        qp.drawLine(10, 500, 1590, 500)
        qp.drawLine(10, 600, 1590, 600)
        
        # Draw current instant dotted line
        qp.setPen(QPen(QtCore.Qt.black, 10, QtCore.Qt.DashLine))
        qp.drawLine(800, 350, 800, 500)
        qp.drawLine(800, 600, 800, 750)

        # Render each of the detected peaks in black
        qp.setPen(QPen(QtCore.Qt.black, 10))
        for i, p in enumerate(metro.peakQueue):
            if i > 85:
                break
        
            if p:
                x = 800 - (i * 10)
                qp.drawLine(x, 350, x, 500)
                
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
                    qp.drawLine(x, 510, x, 540)
                    qp.drawLine(x - (diff * 10), 560, x - (diff * 10), 600)
                    
                    # Return to black pen
                    qp.setPen(QPen(QtCore.Qt.black, 10))
        
        # Render a line for each of the metronome beats on the lower line
        beatQueue = copy.deepcopy(metro.beatQueue)
        for i, b in enumerate(beatQueue):
            if b:
                qp.drawLine(800 - ((i - 86) * 10), 600, 800 - ((i - 86) * 10), 750)
                
        
