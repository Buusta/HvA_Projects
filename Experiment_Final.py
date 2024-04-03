
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import math


# recording file settings
chunk = 1024
r_format = pyaudio.paInt16
bit_rate = 44100
channels = 1

# record settings
record_time = 1
ddb_gekalibreert = 35


# smoothing paramaters
chunk_size = 1250
resolution = 500

# derivative
derivative_scale = 5
derivative_max = 10

# search paramaters
search_distance = 4
slope_threshold = 2


def record_sound(record_time, r_format, bit_rate, chunk):
    # Start recording
    p = pyaudio.PyAudio()
    stream = p.open(format=r_format, channels=channels, rate=bit_rate, input=True, frames_per_buffer=chunk)
    #print("Recording started")
    frames = [np.array([], dtype=np.int16)]
    for i in range(0, int(bit_rate / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(data)
        frames_np = np.frombuffer(b''.join(frames), dtype=np.int16)
    # save recording
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # convert to db
    db = 20 * np.log10(abs(frames_np) + 0.001)
    
    smooth_db = []
    
    #smooth db out
    for i in range(len(db)):
        # Get the current chunk
        chunk = db[i:i+chunk_size]
        
        # Calculate the average of the chunk
        chunk_average = np.sum(chunk) / len(chunk)
        
        # Append the average to the smoothed_list
        smooth_db.append(chunk_average)
        
    # convert to low resolution 
    low_res = []
    for i in range(math.floor(len(smooth_db) / resolution)):
        low_res.append(smooth_db[i*resolution])
    
    x = np.linspace(0,record_time, len(low_res))
    
    dydb = []    
    
    #derivative clalculation
    for i in range(len(low_res)-1):
        dy = (low_res[i+1] - low_res[i]) * derivative_scale
        
        if abs(dy) > derivative_max * derivative_scale:
            dy = 0
        dydb.append(dy)
    dydb.append(0)
    
    # Find the index of the peak y value
    peak_index = np.argmax(low_res)

    # Use this index to find the peak x and y values
    peak_x = x[peak_index]
    peak_y = low_res[peak_index]
    
    points = math.floor(len(low_res[peak_index:len(low_res)]) / search_distance)
    
        

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot wave
    ax.plot(x, low_res)
    ax.plot(x, dydb)
    ax.scatter(peak_x, peak_y)
    
    averages = []
    best_point = 200

    # calculate average derivative of all points
    for i in range(points - 1):
        avg = sum(dydb[peak_index+(i)*search_distance:peak_index+(i+1)*search_distance]) / search_distance
        averages.append(avg)
        ax.scatter((peak_index+(i+1)*search_distance)/len(low_res), low_res[peak_index+(i+1)*search_distance])

        
    # choose point based on threshold
    for i in range(len(averages) - 2):
        if abs(averages[i]) < slope_threshold and averages[i+1] < slope_threshold and averages[i+2] < slope_threshold:
            if i < best_point:
                best_point = i


    dt = x[best_point*search_distance]
    
    galmtijd = 60 / ddb_gekalibreert * dt
    
    print(round(galmtijd, 2))

    plt.show()


# run function
record_sound(record_time, r_format, bit_rate, chunk)

