import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('GeluidsmetingDeviatie.xlsx')

df1 = pd.DataFrame()
df1 = df * 2.4


plt.figure(dpi=600)

plt.imshow(df1, cmap ="Greys", interpolation='none')


plt.xticks(np.arange(0, df1.shape[1], step=2))

yticks = np.arange(0, df1.shape[0], step=2)

plt.yticks(yticks)
plt.colorbar() 

plt.yticks(yticks, yticks[::-1])


plt.show()