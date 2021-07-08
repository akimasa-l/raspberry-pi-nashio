import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED_PIN = 25
BUTTON_PIN = 27
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def callback(channel):
    if GPIO.input(LED_PIN) == GPIO.HIGH:
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)


GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING,
                      callback=callback, bouncetime=200)
GPIO.output(LED_PIN, GPIO.HIGH)
# print(GPIO.input(LED_PIN))
GPIO.output(LED_PIN, GPIO.LOW)
INTERVAL=10
for i in range(10*30):
    time.sleep(1/INTERVAL)
GPIO.cleanup()
