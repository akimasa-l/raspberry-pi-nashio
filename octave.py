import Telmin
import random
import numpy as np
a, aa, b, c, cc, d, dd, e, f, ff, g, gg = np.geomspace(
    440, 880, 12, endpoint=False)
OCTAVE = [c,cc, d,dd, e, f,ff, g,gg, a*2,aa*2,b*2]
# print(OCTAVE)


def make_sound(distance: float,base=OCTAVE):
    if distance >= Telmin.DISTANCE_HIGH:
        return 0
    for i, j in zip(range(len(base))[::-1], np.linspace(0, Telmin.DISTANCE_HIGH, len(base)-1, endpoint=True)):
        if distance < j:
            return int(round(base[i]))


def main():
    base=[]
    for i in range(-2,3):
        base+=map(lambda x:x*(2**i),OCTAVE)
    sound_function=lambda x:make_sound(x,base)
    termin = Telmin.Telmin()
    termin.main(sound_function)


if __name__ == "__main__":
    # print(np.linspace(0,Telmin.DISTANCE_HIGH,len(OCTAVE)-1,endpoint=True))
    main()
