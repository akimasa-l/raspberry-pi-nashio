import Telmin
import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,Telmin.DISTANCE_HIGH)
y=Telmin.make_sound(x)
plt.plot(x,y)
plt.savefig("./graph.png")
plt.show()