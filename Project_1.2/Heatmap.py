import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
# df = pd.read_excel('GeluidsmetingDeviatie.xlsx')  # This line is commented out
df = pd.read_excel('Geluidmeting.xlsx')  # Load the data from 'Geluidmeting.xlsx'

# Create a new DataFrame and scale the original data
df1 = pd.DataFrame()  # Initialize an empty DataFrame
df1 = df * (60/25)  # Scale the data in the original DataFrame by a factor of 60/25

# Create a new figure with a high resolution
plt.figure(dpi=600)

# Display the data as an image
plt.imshow(df1, cmap="RdBu_r", interpolation='none')  # Display the data in grayscale without any interpolation

# Set the x-ticks at an interval of 2
plt.xticks(np.arange(0, df1.shape[1], step=2))

# Calculate the y-ticks
yticks = np.arange(0, df1.shape[0], step=2)

# Set the y-ticks
plt.yticks(yticks)

# Display a colorbar
plt.colorbar()

# Reverse the order of the y-ticks
plt.yticks(yticks, yticks[::-1])

# Display the plot
plt.show()
