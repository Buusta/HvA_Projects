import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import math

# Settings for the recording file
chunk = 1024  # Size of chunks to read at a time
r_format = pyaudio.paInt16  # Format of the audio
bit_rate = 44100  # Bit rate of the audio
channels = 1  # Number of audio channels

# Settings for the recording
record_time = 1  # Duration of the recording in seconds
ddb_gekalibreert = 35  # Calibrated value in dB

# Parameters for smoothing the audio data
chunk_size = 1250  # Size of chunks for smoothing
resolution = 500  # Resolution for smoothing

# Parameters for calculating the derivative
derivative_scale = 5  # Scale factor for the derivative
derivative_max = 10  # Maximum value for the derivative

# Parameters for searching the audio data
search_distance = 4  # Distance for searching
slope_threshold = 2  # Threshold for the slope

def record_sound(record_time, r_format, bit_rate, chunk):
    # Start recording
    p = pyaudio.PyAudio()
    stream = p.open(format=r_format, channels=channels, rate=bit_rate, input=True, frames_per_buffer=chunk)
    frames = [np.array([], dtype=np.int16)]
    for i in range(0, int(bit_rate / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(data)
    frames_np = np.frombuffer(b''.join(frames), dtype=np.int16)
    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Convert the audio data to dB
    db = 20 * np.log10(abs(frames_np) + 0.001)
    
    smooth_db = []
    # Smooth the dB data
    for i in range(len(db)):
        chunk = db[i:i+chunk_size]  # Get the current chunk
        chunk_average = np.sum(chunk) / len(chunk)  # Calculate the average of the chunk
        smooth_db.append(chunk_average)  # Append the average to the smoothed list
        
    # Convert the smoothed data to low resolution
    low_res = []
    for i in range(math.floor(len(smooth_db) / resolution)):
        low_res.append(smooth_db[i*resolution])
    
    x = np.linspace(0,record_time, len(low_res))
    
    dydb = []    
    # Calculate the derivative
    for i in range(len(low_res)-1):
        dy = (low_res[i+1] - low_res[i]) * derivative_scale
        if abs(dy) > derivative_max * derivative_scale:
            dy = 0
        dydb.append(dy)
    dydb.append(0)
    
    # Find the peak y value
    peak_index = np.argmax(low_res)
    # Use this index to find the peak x and y values
    peak_x = x[peak_index]
    peak_y = low_res[peak_index]
    
    points = math.floor(len(low_res[peak_index:len(low_res)]) / search_distance)
    
    # Create figure and axis
    fig, ax = plt.subplots()
    # Plot the wave and its derivative
    ax.plot(x, low_res)
    ax.plot(x, dydb)
    ax.scatter(peak_x, peak_y)
    
    averages = []
    best_point = 200
    # Calculate the average derivative of all points
    for i in range(points - 1):
        avg = sum(dydb[peak_index+(i)*search_distance:peak_index+(i+1)*search_distance]) / search_distance
        averages.append(avg)
        ax.scatter((peak_index+(i+1)*search_distance)/len(low_res), low_res[peak_index+(i+1)*search_distance])

    # Choose the best point based on the slope threshold
    for i in range(len(averages) - 2):
        if abs(averages[i]) < slope_threshold and averages[i+1] < slope_threshold and averages[i+2] < slope_threshold:
            if i < best_point:
                best_point = i

    dt = x[best_point*search_distance]
    # Calculate the reverberation time
    galmtijd = 60 / ddb_gekalibreert * dt
    print(round(galmtijd, 2))

    plt.show()

# Run the function
record_sound(record_time, r_format, bit_rate, chunk)