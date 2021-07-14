import time
import random
import RPi.GPIO as GPIO
import wiringpi

SOUND_PORT = 2
ECHO_PORT = 3
TRIG_PORT = 4
SOUND_HIGH = 1760
SOUND_LOW = 220
DISTANCE_HIGH = 50


class Telmin:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG_PORT, GPIO.OUT)
        GPIO.setup(ECHO_PORT, GPIO.IN)
        wiringpi.wiringPiSetupGpio()
        wiringpi.softToneCreate(SOUND_PORT)
    
    def __del__(self):
        print("これほんとに呼ばれるのか？？？")
        GPIO.cleanup()

    def read_distance(self):
        GPIO.output(TRIG_PORT, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(TRIG_PORT, GPIO.HIGH)
        time.sleep(0.011)
        GPIO.output(TRIG_PORT, GPIO.LOW)
        while GPIO.input(ECHO_PORT) == GPIO.LOW:
            start = time.time()
        while GPIO.input(ECHO_PORT) == GPIO.HIGH:
            end = time.time()
        duration = end-start
        distance = duration*17000
        return distance

    @staticmethod
    def make_sound(distance: float):
        a = -DISTANCE_HIGH/(SOUND_HIGH-SOUND_LOW)
        b = -SOUND_HIGH*a
        return (distance-b)/a

    def main(self):
        try:
            while 1:
                distance = self.read_distance()
                if distance > DISTANCE_HIGH+1:
                    distance = random.randint(0, DISTANCE_HIGH)
                sound = Telmin.make_sound(distance)
                print("distance,sound", distance, sound)

                wiringpi.softToneWrite(SOUND_PORT, round(sound))
                time.sleep(0.05)
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    Telmin().main()
