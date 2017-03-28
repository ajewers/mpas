import sys
import copy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPen, QFont
from audioHandler import AudioHandler
from renderer import Renderer
from button import Button
from activeMetronome import ActiveMetronome

# Enumeration of the different modes (states)
class Mode():
    MAIN_MENU =         1
    TEMPO_DETECT =      2
    ACTIVE_METRONOME =    3

# Main class for the PyTempo MPAS app
class MPASApp(QtGui.QMainWindow):
    def __init__(self):
        super(MPASApp, self).__init__()
        
        # Current mode variable
        self.mode = Mode.MAIN_MENU
        
        # Mouse position x/y
        self.mouse = [0, 0]
        
        # Current detected BPM
        self.bpm = 0.0
        
        # The active metronome class instance
        self.metro = ActiveMetronome()
        
        # Audio handler class instance
        self.audioHandler = AudioHandler(self.metro.newChunk)
        
        # Set metronome audio handler reference
        self.metro.setAudioHandlerRef(self.audioHandler)

        # Renderer class instance
        self.renderer = Renderer()
        
        # Main menu buttons
        self.tempoButton = Button(900, 400, 420, 60, "Tempo Detection", False)
        self.metroButton = Button(900, 500, 420, 60, "Active Metronome", False)
        self.backButton = Button(20, 20, 130, 60, "Back", False)
        
        # Initialise the GUI
        self.initUI()
        
        # Start the update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)
        
        # Enable mouse tracking
        self.setMouseTracking(True)
       
    # Initialises the GUI
    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('MPAS Visual Metronome')
        self.show()
        
    # Called when the window needs to be re-drawn
    def paintEvent(self, e):
        # Acquire the QPainter instance
        qp = QtGui.QPainter()
        qp.begin(self)
        
        # Main Menu
        if self.mode == Mode.MAIN_MENU:
            self.renderer.renderMainMenu(qp, self.tempoButton, self.metroButton)
        
        # Tempo Detection
        elif self.mode == Mode.TEMPO_DETECT:
            energyQueue = copy.deepcopy(self.audioHandler.energyQueue)
            peakQueue = copy.deepcopy(self.audioHandler.peakQueue)
            self.renderer.renderTempoDetect(qp, energyQueue, peakQueue, self.audioHandler.energyAverage, self.bpm, self.backButton)
        
        # Live Metronome
        elif self.mode == Mode.ACTIVE_METRONOME:
            self.renderer.renderActiveMetronome(qp, self.backButton, self.metro)
        
        qp.end()
        
    # Update timer fired
    def tick(self):
        # Check mouse position against buttons
        if self.mode == Mode.MAIN_MENU:
            self.tempoButton.checkHover(self.mouse)
            self.metroButton.checkHover(self.mouse)
        elif self.mode == Mode.TEMPO_DETECT:
            self.backButton.checkHover(self.mouse)
        elif self.mode == Mode.ACTIVE_METRONOME:
            self.backButton.checkHover(self.mouse)
            self.metro.checkHover(self.mouse)
    
        # Perform processing
        if self.mode == Mode.TEMPO_DETECT:
            self.audioHandler.calculateTempo(self)
        elif self.mode == Mode.ACTIVE_METRONOME:
            self.metro.peakQueue = copy.deepcopy(self.audioHandler.peakQueue)
            self.metro.energyQueue = copy.deepcopy(self.audioHandler.energyQueue)
    
        # Re-draw the UI
        self.repaint()
        
    # Called to handle window close events
    def closeEvent(self, event):
        self.audioHandler.close()
        
    # Called to handle mouse movement
    def mouseMoveEvent(self, event):
        # Update mouse x and y position values
        self.mouse = [event.pos().x(), event.pos().y()]
        
    # Called to handle mouse clicks
    def mousePressEvent(self, QMouseEvent):
        # Handle clicks in main menu mode
        if self.mode == Mode.MAIN_MENU:
            if self.tempoButton.hover:
                # Change to tempo detect mode
                self.mode = Mode.TEMPO_DETECT
                self.tempoButton.hover = False
            elif self.metroButton.hover:
                # Change to active metronome mode
                self.mode = Mode.ACTIVE_METRONOME
                self.metroButton.hover = False
                self.metro.active = True
                
        else:
            if self.backButton.hover:
                # Return to main menu mode
                self.mode = Mode.MAIN_MENU
                self.backButton.hover = False
                self.metro.active = False
                
        # If in active metronome mode, pass mouse clicks through
        if self.mode == Mode.ACTIVE_METRONOME:
            self.metro.mousePressEvent()
    
# Main function launches application
def main():
    app = QtGui.QApplication(sys.argv)
    w = MPASApp()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()