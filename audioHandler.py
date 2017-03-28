from pyaudio import PyAudio, paFloat32, paContinue
import wave
import numpy as np
import time
import math
import copy

from collections import deque

# Audio handler class for managing PyAudio input and output streams
# and performing audio processing for peak detection.
class AudioHandler():
    def __init__(self, newChunk):
        # Constants
        self.CHANNLES = 1
        self.RATE = 44100
        
        # Queue of energy values, 1s @ 44.1 kHz / 1024 chunk size = 43 elements
        self.energyQueue = deque([], 43)
        
        # Queue of detected energy peaks. 10s long
        self.peakQueue = deque([], 430)
        
        # Energy average and threshold values
        self.energyAverage = 0
        self.energyThreshold = 0
        
        # New chunk function - to be called every time a new chunk arrives
        self.newChunk = newChunk
        
        # Metronome click sound, loaded from a wav file
        self.metroClick = wave.open("MetroClick.wav", 'rb')
        
        # Fill the energy and peak queues with zeros
        for i in range(0, 42):
            self.energyQueue.appendleft(0)
            for i in range(0, 9):
                self.peakQueue.appendleft(False)

        # Initialise PyAudio instance
        self.pa = PyAudio()
        
        # Open the real time input stream in callback mode
        self.stream = self.pa.open(format = paFloat32,
                                   channels = 1,
                                   rate = 44100,
                                   input = True,
                                   output = False,
                                   frames_per_buffer = 1024,
                                   stream_callback = self.callback)
        
        # Start the input stream
        self.stream.start_stream()
        
        # Open the output stream for playing the metronome click
        self.clickStream = self.pa.open(format = self.pa.get_format_from_width(self.metroClick.getsampwidth()),
                                        channels = self.metroClick.getnchannels(),
                                        rate = self.metroClick.getframerate(),
                                        output = True)
    
    # Called to close the streams gracefully upon exit
    def close(self):
        self.stream.close()
        self.clickStream.close()
        self.pa.terminate()

    # Calback function for input stream
    def callback(self, in_data, frame_count, time_info, flag):
        # Check error flag
        if flag:
            print("Playback Error: %i" % flag)
        
        # Get the raw audio data
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
            
        # Call the new chunk function
        self.newChunk()
        
        return (audio_data, paContinue)
        
    # Calculates an estimate of the tempo based on detected peaks
    def calculateTempo(self, parent):
        # Deep copy to avoid threading issues
        peaks = copy.deepcopy(self.peakQueue)
        
        # Array of interval lengths
        intervals = []
        
        # Loop through peaks measuring intervals
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
                
        # Calculate the average interval
        avg = 0.0
        for i in intervals:
            avg += i
            
        if len(intervals) > 0:
            avg = avg / len(intervals)
        
        # Calculate the BPM based on the average inter-peak interval
        if avg > 0:
            parent.bpm = 60.0 / ((avg * 1024.0)/44100.0)
        else:
            parent.bpm = -1
            
    # Plays the metronome click sound
    def playClick(self):
        # Ensure reading starts from beggining of file
        self.metroClick.rewind()
    
        # Read one chunk of data from the wav file
        data = self.metroClick.readframes(1024)

        # While data remains in the file write it into the stream and read the next chunk
        while data != '':
            self.clickStream.write(data)
            data = self.metroClick.readframes(1024)
