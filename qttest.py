import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPen
from audioHandler import AudioHandler

class MPASApp(QtGui.QMainWindow):
    def __init__(self):
        super(MPASApp, self).__init__()
        
        self.y = 0
        
        self.audioHandler = AudioHandler()
        
        self.initUI()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)
        
    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('MPAS Visual Metronome')
        self.show()
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = QPen(QtCore.Qt.red, 3)
        qp.setPen(pen)
        
        for i, e in enumerate(self.audioHandler.energyQueue):
            qp.drawLine(100 + i * 20, 800, 100 + i * 20, 800 - 200 * e)
            
        qp.end()
        
    def tick(self):
        self.y = self.y + 1
        self.repaint()
        
    def closeEvent(self, event):
        self.audioHandler.close()
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = MPASApp()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()