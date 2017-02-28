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
        
        return (audio_data, paContinue)