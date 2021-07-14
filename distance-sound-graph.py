import distance
import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,distance.DISTANCE_HIGH)
y=distance.make_sound(x)
plt.plot(x,y)
plt.show()