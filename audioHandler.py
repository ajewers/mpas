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
        
        for i in range(0, 42):
            self.energyQueue.appendleft(0)
            for i in range(0, 9):
                self.beatQueue.appendleft(False)

        self.pa = PyAudio()
        self.full_data = np.array([])
        
        self.stream = self.pa.open(format = paFloat32,
                                   channels = 2,
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
        energy = 0;
    
        for i in xrange(0, len(audio_data) - 1):
            energy += audio_data[i]**2
            
        self.energyQueue.appendleft(math.sqrt(energy))
        
        total = 0
        for v in self.energyQueue:
            total += v
            
        self.energyAverage = total / 43
        
        if energy > self.energyAverage * 3 and self.energyQueue[1] < self.energyAverage * 1.5 and not self.beatQueue[1] and not self.beatQueue[2]:
            self.beatQueue.appendleft(True)
        else:
            self.beatQueue.appendleft(False)
        
        return (audio_data, paContinue)