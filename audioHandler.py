from pyaudio import PyAudio, paFloat32, paContinue
import wave
import numpy as np
import time
import math
import copy

from collections import deque

class AudioHandler():
    def __init__(self, newBlock):
        self.CHANNLES = 1
        self.RATE = 44100
        
        self.energyQueue = deque([], 43)
        self.peakQueue = deque([], 430)
        self.energyAverage = 0
        self.energyThreshold = 0
        
        self.newBlock = newBlock
        
        self.metroClick = wave.open("MetroClick.wav", 'rb')
        
        for i in range(0, 42):
            self.energyQueue.appendleft(0)
            for i in range(0, 9):
                self.peakQueue.appendleft(False)

        self.pa = PyAudio()
        self.full_data = np.array([])
        
        self.stream = self.pa.open(format = paFloat32,
                                   channels = 1,
                                   rate = 44100,
                                   input = True,
                                   output = False,
                                   frames_per_buffer = 1024,
                                   stream_callback = self.callback)
                  
        self.stream.start_stream()
        
        self.clickStream = self.pa.open(format = self.pa.get_format_from_width(self.metroClick.getsampwidth()),
                                        channels = self.metroClick.getnchannels(),
                                        rate = self.metroClick.getframerate(),
                                        output = True)
                     
    def close(self):
        self.stream.close()
        self.clickStream.close()
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
        self.energyThreshold = (-0.000026 * variance) + 1.5142857
        
        # If the energy exceeds the average x threshold, detect a beat
        if energy > 1.0 and energy > self.energyAverage * self.energyThreshold and not self.peakQueue[0] and not self.peakQueue[1] and not self.peakQueue[2] and not self.peakQueue[3] and not self.peakQueue[4]:
            self.peakQueue.appendleft(True)
        else:
            self.peakQueue.appendleft(False)
            
        self.newBlock()
        
        return (audio_data, paContinue)
        
    def calculateTempo(self, parent):
        peaks = copy.deepcopy(self.peakQueue)
        
        intervals = []
        
        count = 0
        first = True
        for p in peaks:
            count += 1
            
            if p:
                if count > 10:
                    if first:
                        first = False
                    else:
                        intervals.append(count)
                    
                    count = 0
                
        avg = 0.0
        for i in intervals:
            avg += i
            
        if len(intervals) > 0:
            avg = avg / len(intervals)
        
        if avg > 0:
            parent.bpm = 60.0 / ((avg * 1024.0)/44100.0)
        else:
            parent.bpm = -1
            
    def playClick(self):
        # read data (based on the chunk size)
        data = self.metroClick.readframes(1024)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            self.clickStream.write(data)
            data = self.metroClick.readframes(1024)
            
        self.metroClick.rewind()
        