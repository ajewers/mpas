import sys
import math
from collections import deque
from button import Button

# Encapsulates the Active Metronome mode
class ActiveMetronome():#
    # Constructor
    def __init__(self):
        # Create queues for detected peaks, energy values and metronome beats
        self.peakQueue = deque([], 430)
        self.energyQueue = deque([], 43)
        self.beatQueue = deque([], 172)
        
        # Fill the metronome beat queue
        for i in range(0, 171):
            self.beatQueue.appendleft(False)
        
        # Target tempo value
        self.bpm = 100
        
        # Interval between metronome beats for the target bpm
        self.beatInterval = int((60.0 / self.bpm) * (44100.0 / 1024.0))
        
        # Counter variable for spacing metronome beats
        self.count = self.beatInterval
        
        # Tempo adjust buttons
        self.tempoUpButton = Button(1250, 30, 70, 40, "+ 1", True)
        self.tempoUpPlusButton = Button(1330, 30, 90, 40, "+ 10", True)
        self.tempoDownButton = Button(1250, 80, 70, 40, "- 1", True)
        self.tempoDownPlusButton = Button(1330, 80, 90, 40, " - 10", True)
        
        # Active flag to enable/disable metronome
        self.active = False
        
    # Function for setting the audio handler reference
    def setAudioHandlerRef(self, audioHandler):
        self.audioHandler = audioHandler
    
    # Function to be called when a new chunk arrives
    def newChunk(self):
        # Decrement the counter
        self.count -= 1
        
        # If the counter is zero add a metronome beat and reset it
        if self.count == 0:
            self.count = self.beatInterval
            self.beatQueue.appendleft(self.active)
        else:
            self.beatQueue.appendleft(False)
        
        # If active, and a metronome beat is at the instant line, play the sound
        if self.beatQueue[81] and self.active:
            self.audioHandler.playClick()
        
    # Calculate the accuracy of a given peak compared to the metronome beats
    def getAccuracy(self, peakIndex):
        # Find the nearest beat to the peak at the given index.
        # Indexes higher than 85 are out of range
        if peakIndex > 85:
            return -1000
        
        # Look for the closest beat with a positive difference
        index = peakIndex + 85
        poscount = 0
        while index < len(self.beatQueue) and not self.beatQueue[index]:
            index += 1
            poscount += 1
            
        # Look for the closest beat with a negative difference
        index = peakIndex + 85
        negcount = 0
        while index >= 0 and not self.beatQueue[index]:
            index -= 1
            negcount -= 1
            
        # Determine the smaller difference
        if math.fabs(negcount) < poscount:
            return negcount
        else:
            return poscount
        
    # Check the hover states of the tempo buttons
    def checkHover(self, mouse):
        self.tempoUpButton.checkHover(mouse)
        self.tempoDownButton.checkHover(mouse)
        self.tempoUpPlusButton.checkHover(mouse)
        self.tempoDownPlusButton.checkHover(mouse)
       
    # Check if a tempo button has been pressed
    def mousePressEvent(self):
        # Get previous tempo
        old = self.bpm
    
        # Change tempo if necessary
        if self.tempoUpButton.hover:
            self.bpm += 1
        elif self.tempoDownButton.hover:
            self.bpm -= 1
        elif self.tempoUpPlusButton.hover:
            self.bpm += 10
        elif self.tempoDownPlusButton.hover:
            self.bpm -= 10
            
        # Limits
        if self.bpm < 40:
            self.bpm = 40
        elif self.bpm > 220:
            self.bpm = 220
            
        # If changed, recalculate interval and reset count
        if self.bpm != old:
            self.beatInterval = int((60.0 / self.bpm) * (44100.0 / 1024.0))
            self.count = self.beatInterval