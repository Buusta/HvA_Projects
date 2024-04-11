#imports
import pyaudio
import numpy as np
import statistics as stats
import time

#audio bestand specs
Chunk=1024
Format = pyaudio.paInt16
Rate = 44100
seconds = 3
loops = 3
averages = []

time.sleep(0.25)
#geeft aan via welke channel je opneemt zorg dat je weet welk getal de microfoon is
Channels = 1

for  i in range(loops):
    print(i+1)
    #start opnamen
    p = pyaudio.PyAudio( )
    stream = p.open(format=Format,
                  channels=Channels,
                  rate=Rate,
                  input=True,
                  frames_per_buffer=Chunk)
    frames = []
    for i in range(0,int(Rate/Chunk*seconds)):
        data = stream.read(Chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    
    # Convert byte data to integers
    int_frames = [np.frombuffer(frame, 'int16') for frame in frames]
    
    # Calculate the absolute values
    abs_frames = [np.abs(i) for i in int_frames]
    
    # Calculate the average amplitude
    average_amplitude = np.mean(abs_frames)
    
    # Convert amplitude to dB
    average_amplitude_db = 20 * np.log10(average_amplitude)
    
    averages.append(average_amplitude_db)

# Print average measured decibels
print("average =", stats.mean(averages))
    
    
