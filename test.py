from gpiozero import Button, LED, InputDevice, Buzzer
from signal import pause
import RPi.GPIO as GPIO
import time

buzzer = Buzzer(17)
red = LED(26)
green = LED(25)
button = Button(21)
channel = 23



GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def buzzerOff():
    buzzer.off()
    red.off()
    print("Buzzer off")
 

button.when_pressed = buzzerOff

def callback(channel):
    # if GPIO.input(channel) == GPIO.HIGH:
    #     print("high")
    # else:
    #     print("low")
    # print(GPIO.input(channel))
    # print(GPIO.HIGH)
    buzzer.on()
    red.on()
    print("flame detected !")
    if button.is_pressed:
        buzzerOff()
    


def greenOn():
    green.off()
    time.sleep(1)
    green.on()
    time.sleep(1)



GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)


while True:
    greenOn()
    time.sleep(1)
