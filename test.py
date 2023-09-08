from gpiozero import Button, LED, InputDevice, Buzzer
from signal import pause
import RPi.GPIO as GPIO
import time
import threading
from email.message import EmailMessage
import ssl
import smtplib
from flask import Flask
import sqlite3
import middleware 
import importlib




def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

buzzer = Buzzer(17)
red = LED(26)
green = LED(25)
button = Button(21)
channel = 23

def send_mail_to_fire():
    try:
        conn = connect_to_db()
        query = "SELECT * FROM users"
        result = conn.execute(query)
        user_data = result.fetchone()
        conn.close()
        sender_email = 'ignisfiresystem@gmail.com'
        sender_password = 'zqas taxp vtlb trfk'  # Make sure to use your actual email password

        email_receiver = user_data[6]

        subject = f"A Fire Has Been Detected!!! at {user_data[1]} {user_data[2]}'s place"
        body = f"These are the co-ordinates to the location {user_data[8]} \nThe location is {user_data[7]}"

        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = email_receiver
        em['subject'] = subject 
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, email_receiver, em.as_string())
            print("mail sent to fire department")
    except Exception as e:
        print(e)
    

def send_personal_mail():
    try:
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
            print("mail sent to user")
    except Exception as e:
        print(e)


GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def buzzerOff():
    global fire_alert
    buzzer.off()
    red.off()
    print("Buzzer off")
    middleware.fire_alert = False
 

button.when_pressed = buzzerOff

def callback(channel):
    buzzer.on()
    red.on()
    print("Flame detected!")
    send_personal_mail()
    middleware.fire_alert = True
    fire_timer = threading.Timer(600, send_mail_to_fire)
    fire_timer.start()
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
    importlib.reload(middleware)
    print(middleware.fire_alert)
