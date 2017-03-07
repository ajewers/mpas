from pyaudio import PyAudio, paFloat32, paContinue
import numpy as np
import time
import math

from collections import deque

class AudioHandler():
    def __init__(self):
        self.CHANNLES = 1
        self.RATE = 44100
        
        self.energyQueue = deque([], 43)
        self.beatQueue = deque([], 430)
        self.energyAverage = 0
        self.energyThreshold = 0
        
        for i in range(0, 42):
            self.energyQueue.appendleft(0)
            for i in range(0, 9):
                self.beatQueue.appendleft(False)

        self.pa = PyAudio()
        self.full_data = np.array([])
        
        self.stream = self.pa.open(format = paFloat32,
                                   channels = 1,
                                   rate = 44100,
                                   input = True,
                                   output = True,
                                   frames_per_buffer = 1024,
                                   stream_callback = self.callback)
                  
        self.stream.start_stream()
                     
    def close(self):
        self.stream.close()
        self.pa.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        if flag:
            print("Playback Error: %i" % flag)
        
        audio_data = np.fromstring(in_data, dtype=np.float32)
        
        # Calculate energy value for this block
        energy = 0;
        for i in xrange(0, len(audio_data) - 1):
            energy += audio_data[i]**2
        
        # Append energy value to queue
        self.energyQueue.appendleft(energy)
        
        # Calculate average energy for the values in the queue
        total = 0
        for e in self.energyQueue:
            total += e
            
        self.energyAverage = total / 43
        
        # Calculate variance
        MSE = 0
        for e in self.energyQueue:
            MSE += (e - self.energyAverage)**2
        
        variance = MSE / 43
        
        # Calculate beat detection threshold
        self.energyThreshold = (-0.0000015 * variance) + 1.5142857
        
        # If the energy exceeds the average x threshold, detect a beat
        if energy > 1.0 and energy > self.energyAverage * self.energyThreshold and not self.beatQueue[0] and not self.beatQueue[1] and not self.beatQueue[2] and not self.beatQueue[3] and not self.beatQueue[4]:
            self.beatQueue.appendleft(True)
        else:
            self.beatQueue.appendleft(False)
        
        return (audio_data, paContinue)
        