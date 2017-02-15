from pyaudio import PyAudio, paFloat32, paContinue
import numpy as np
import time

CHANNLES = 1
RATE = 44100

pa = PyAudio()
full_data = np.array([])

def callback(in_data, frame_count, time_info, flag):
  if flag:
    print("Playback Error: %i" % flag)
  global full_data
  audio_data = np.fromstring(in_data, dtype=np.float32)
  #full_data = np.append(full_data, audio_data)
  return (audio_data, paContinue)

def main():
  stream = pa.open(format = paFloat32,
                   channels = 2,
                   rate = 44100,
                   input = True,
                   output = True,
                   frames_per_buffer = 1024,
                   stream_callback = callback)
                  
  stream.start_stream()
                 
  while stream.is_active():
    time.sleep(10)
    stream.stop_stream()
  
  stream.close()
  pa.terminate()

main()