from gpiozero import Button, LED, InputDevice, Buzzer
from signal import pause
import RPi.GPIO as GPIO
import time

# button = Button(17)
# light = LED(23)
# # flame = InputDevice(22)
# button.when_pressed = light.on
# button.when_released = light.off
# pause()
buzzer = Buzzer(17)
red = LED(26)
green = LED(25)
channel = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def callback(channel):
    buzzer.on()
    red.on()
    print("flame detected !")
    time.sleep(2)
    buzzer.off()
    red.off()


def greenOn():
    green.off()
    time.sleep(1)
    green.on()
    time.sleep(1)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
    greenOn()
