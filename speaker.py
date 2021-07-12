import time
import math
import wiringpi
import numpy as np
SOUND_PORT = 21
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(SOUND_PORT)
a, aa, b, c, cc, d, dd, e, f, ff, g, gg = map(
    int, np.round(np.geomspace(440, 884, 12)))
for sound in [c, d, e, f, g, a*2, b*2, c*2]:
    print(type(SOUND_PORT), type(sound))
    wiringpi.softToneWrite(SOUND_PORT, sound)
    time.sleep(0.5)
""" 
wiringpi.softToneWrite(SOUND_PORT,440)
time.sleep(1.0)
wiringpi.softToneWrite(SOUND_PORT,0)
 """
