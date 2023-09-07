from flask import Flask, render_template, request, redirect
import sqlite3
import json
from urllib.request import urlopen
from dotenv import load_dotenv
import os
import geocoder
from flask_mail import Mail, Message
from gpiozero import LED, Buzzer

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER']=str(os.getenv('MAIL_SERVER'))
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = str(os.getenv('MAIL_USERNAME'))
app.config['MAIL_PASSWORD'] = str(os.getenv('MAIL_PASSWORD'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
buzzer = Buzzer(17)
red = LED(26)

def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

def buzzerOff():
    buzzer.off()
    red.off()
    print("Buzzer off")

def create_user_table():
    try:
        con = connect_to_db()
        con.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_no TEXT UNIQUE NOT NULL,
                enumber TEXT NOT NULL,
                eemail TEXT NOT NULL,
                address TEXT NOT NULL,
                coordinates TEXT NOT NULL
            );
        ''')
        con.commit()
        con.close()
    except sqlite3.Error as e:
        return str(e)

def check_user_data():
    conn = connect_to_db()
    create_user_table()
    query = "SELECT * FROM users"
    result = conn.execute(query)
    user_data = result.fetchone()
    conn.close()
    return user_data

@app.route('/', methods=['GET', 'POST'])
def index():
    user_data = check_user_data()
    if user_data:
        return redirect('/home')
    else:
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            number = request.form['number']
            emergencynumber = request.form['emergencynumber']
            emergencyemail = request.form['emergencyemail']
            address = request.form['address']

            create_user_table()
            coordinates = get_computer_location()
            print(coordinates)

            try:
                con = connect_to_db()
                con.execute('''
                    INSERT INTO users(
                        firstname, lastname, email, phone_no, enumber, eemail, address, coordinates
                    ) VALUES (?,?,?,?,?,?,?,?)
                ''',(fname, lname, email, number, emergencynumber, emergencyemail,address,coordinates))
                con.commit()
                con.close()
                return redirect('/home')
            except sqlite3.Error as e:
                return str(e)
        return render_template('index.html')

@app.route('/home')
def home():
    # send_mail_to_fire()
    # send_personal_mail()
    # get_computer_location()
    return render_template('greetings.html')

@app.route('/notification')
def notification():
    conn = connect_to_db()
    query = "SELECT * FROM users"
    result = conn.execute(query)
    user_data = result.fetchone()
    conn.close()
    number = user_data[5]
    return render_template('home.html',number=number)

def get_computer_location():
    try:
        g = geocoder.ip('me')

        if g.ok:
            location = g.json
            cor = f"{location['lat']} {location['lng']}"
            return cor
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_mail_to_fire():
    conn = connect_to_db()
    query = "SELECT * FROM users"
    result = conn.execute(query)
    user_data = result.fetchone()
    conn.close()
    message = Message(
        subject=f"There seems to be a fire problem at {user_data[1]}'s place",
        recipients=[f"{user_data[6]}"],
        sender=user_data[3]
    )
    message.body = f"These are the co-ordinates to the location {user_data[8]} \nThe location is {user_data[7]}"
    
    try:
        mail.send(message)
        print("sent")
    except Exception as e:
        return e

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



@app.post('/turnOff')
def turnOff():
    buzzerOff()
    return redirect("/notification")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
