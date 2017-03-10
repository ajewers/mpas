import sys
import copy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPen, QFont
from audioHandler import AudioHandler
from renderer import Renderer
from button import Button

class Mode():
    MAIN_MENU =         1
    TEMPO_DETECT =      2
    LIVE_METRONOME =    3

class MPASApp(QtGui.QMainWindow):
    def __init__(self):
        super(MPASApp, self).__init__()
        
        self.mode = Mode.MAIN_MENU
        self.mouse = [0, 0]
        
        self.bpm = 0.0
        
        self.audioHandler = AudioHandler()
        self.renderer = Renderer()
        self.tempoButton = Button(900, 400, 400, 60, "Tempo Detection")
        self.metroButton = Button(900, 500, 400, 60, "Live Metronome")
        self.backButton = Button(10, 10, 120, 60, "Back")
        
        self.initUI()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)
        
        self.setMouseTracking(True)
        
    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('MPAS Visual Metronome')
        self.show()
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        
        # Main Menu
        if self.mode == Mode.MAIN_MENU:
            self.renderer.renderMainMenu(qp, self.tempoButton, self.metroButton)
        
        # Tempo Detection
        elif self.mode == Mode.TEMPO_DETECT:
            energyQueue = copy.deepcopy(self.audioHandler.energyQueue)
            beatQueue = copy.deepcopy(self.audioHandler.beatQueue)
            self.renderer.renderTempoDetect(qp, energyQueue, beatQueue, self.audioHandler.energyAverage, self.bpm, self.backButton)
        
        # Live Metronome
        elif self.mode == Mode.LIVE_METRONOME:
            self.renderer.renderLiveMetronome(qp, self.backButton)
        
        
        qp.end()
        
    def tick(self):
        self.repaint()
        
        if self.mode == Mode.MAIN_MENU:
            self.tempoButton.checkHover(self.mouse)
            self.metroButton.checkHover(self.mouse)
        else:
            self.backButton.checkHover(self.mouse)
        
        if self.mode == Mode.TEMPO_DETECT:
            self.audioHandler.calculateTempo(self)
        
    def closeEvent(self, event):
        self.audioHandler.close()
        
    def mouseMoveEvent(self, event):
        self.mouse = [event.pos().x(), event.pos().y()]
        
    def mousePressEvent(self, QMouseEvent):
        if self.mode == Mode.MAIN_MENU:
            if self.tempoButton.hover:
                self.mode = Mode.TEMPO_DETECT
            elif self.metroButton.hover:
                self.mode = Mode.LIVE_METRONOME#
                
        else:
            if self.backButton.hover:
                self.mode = Mode.MAIN_MENU
    
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = MPASApp()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()