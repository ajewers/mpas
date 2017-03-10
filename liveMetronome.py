import sys
from collections import deque
from button import Button

class LiveMetronome():
    def __init__(self):
        self.peakQueue = deque([], 430)
        self.energyQueue = deque([], 43)
        self.beatQueue = deque([], 172)
        for i in range(0, 171):
            self.beatQueue.append(False)
        
        self.bpm = 100
        self.beatInterval = int((60.0 / self.bpm) * (44100.0 / 1024.0))
        self.count = self.beatInterval
        
        self.tempoUpButton = Button(1200, 10, 60, 60, " +", True)
        self.tempoUpPlusButton = Button(1280, 10, 60, 60, "++", True)
        self.tempoDownButton = Button(1200, 210, 60, 60, " -", True)
        self.tempoDownPlusButton = Button(1280, 210, 60, 60, "--", True)
        
    def tick(self):
        donothing = 1
        
    def newBlock(self):
        self.count -= 1
        
        if self.count == 0:
            self.count = self.beatInterval
            self.beatQueue.append(True)
        else:
            self.beatQueue.append(False)
            
        self.beatQueue.popleft()
        
    def checkHover(self, mouse):
        self.tempoUpButton.checkHover(mouse)
        self.tempoDownButton.checkHover(mouse)
        self.tempoUpPlusButton.checkHover(mouse)
        self.tempoDownPlusButton.checkHover(mouse)
        
    def mousePressEvent(self):
        old = self.bpm
    
        if self.tempoUpButton.hover:
            self.bpm += 1
        elif self.tempoDownButton.hover:
            self.bpm -= 1
        elif self.tempoUpPlusButton.hover:
            self.bpm += 10
        elif self.tempoDownPlusButton.hover:
            self.bpm -= 10
            
        if self.bpm < 40:
            self.bpm = 40
        elif self.bpm > 220:
            self.bpm = 220
            
        if self.bpm != old:
            self.beatInterval = int((60.0 / self.bpm) * (44100.0 / 1024.0))
            self.count = self.beatInterval