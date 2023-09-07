from gpiozero import Button, LED, InputDevice, Buzzer
from signal import pause
import RPi.GPIO as GPIO
import sqlite3
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
import time
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER']=str(os.getenv('MAIL_SERVER'))
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = str(os.getenv('MAIL_USERNAME'))
app.config['MAIL_PASSWORD'] = str(os.getenv('MAIL_PASSWORD'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

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
    message = Message(
        subject=f"There seems to be a fire problem at your place",
        recipients=[f"{user_data[3]}"],
        sender="ignissystem@gmail.com"
    )
    message.body = """<html><body>
                <p>Hello,</p>
                <p>Click the link below:</p>
                <a href="localhost:8000/notification">Visit Example Website</a>
                </body></html>"""
    
    try:
        mail.send(message)
        print("sent")
    except Exception as e:
        return e


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
