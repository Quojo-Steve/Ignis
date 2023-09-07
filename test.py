from gpiozero import Button, LED, InputDevice, Buzzer
from signal import pause
import RPi.GPIO as GPIO
import time
from email.message import EmailMessage
import ssl
import smtplib
from flask import Flask
import sqlite3


def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

buzzer = Buzzer(17)
red = LED(26)
green = LED(25)
button = Button(21)
channel = 23

def send_personal_mail():
    conn = connect_to_db()
    query = "SELECT * FROM users"
    result = conn.execute(query)
    user_data = result.fetchone()
    conn.close()
    sender_email = 'ignisfiresystem@gmail.com'
    sender_password = 'zqas taxp vtlb trfk'  # Make sure to use your actual email password

    email_receiver = user_data[3]

    subject = 'A Fire Has Been Detected!!!'
    body = 'Follow this link to access your device controls:  https://8d2a-169-239-248-162.ngrok-free.app/notification'

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = email_receiver
    em['subject'] = subject 
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, email_receiver, em.as_string())


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
    send_personal_mail()
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
