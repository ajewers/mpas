import sys
import copy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPen
from audioHandler import AudioHandler

class MPASApp(QtGui.QMainWindow):
    def __init__(self):
        super(MPASApp, self).__init__()
        
        self.y = 0
        
        self.bpm = 0.0
        
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
        
        queueCopy = copy.deepcopy(self.audioHandler.energyQueue)
        
        for i, e in enumerate(queueCopy):
            if self.audioHandler.beatQueue[i]:
                qp.setPen(QPen(QtCore.Qt.red, 10))
            else:
                qp.setPen(QPen(QtCore.Qt.black, 10))
            
            qp.drawLine(100 + i * 10, 800, 100 + i * 10, 800 - 200 * e)
        
        qp.setPen(QPen(QtCore.Qt.black, 3))
        qp.drawLine(1000, 800, 1000, 800 - 200 * self.audioHandler.energyAverage)
        qp.drawText(1000, 850, 200, 40, 0, "" + str(self.audioHandler.energyAverage))
        
        qp.drawText(1200, 450, 400, 40, 0, "BPM: " + str(self.bpm))
            
        qp.end()
        
    def tick(self):
        self.y = self.y + 1
        self.repaint()
        self.calculateTempo()
        
    def closeEvent(self, event):
        self.audioHandler.close()
        
    def calculateTempo(self):
        beats = copy.deepcopy(self.audioHandler.beatQueue)
        
        intervals = []
        
        count = 0
        for b in beats:
            count += 1
            
            if b:
                intervals.append(count)
                count = 0
                
        print(intervals)
                
        avg = 0
        for i in intervals:
            avg += i
            
        avg = avg / len(intervals)
        
        print(avg)
        
        seconds = avg * 0.0116
        
        bps = 1 / seconds
        
        self.bpm = bps * 60
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = MPASApp()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()