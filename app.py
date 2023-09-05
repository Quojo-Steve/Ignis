from flask import Flask, render_template,request,redirect
from gpiozero import Buzzer, Button
import sqlite3
from time import sleep

app = Flask(__name__)

def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

# buzz = Buzzer(17)
# button = Button(26)

# def tryer():
#     buzz.on()
#     print("how")
#     sleep(0.5)

# button.when_pressed = buzz.on
# button.when_pressed = tryer
# button.when_released = buzz.off

@app.post('/')
@app.get('/')
def index():
    conn = connect_to_db()
    query = f"SELECT * FROM users"
    result = conn.execute(query)
    user_data = result.fetchone()
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
                        eemail TEXT NOT NULL 
                    );
                ''')
                con.execute('''
                INSERT INTO users(
                        firstname,lastname,email,phone_no,enumber,eemail
                    ) VALUES (?,?,?,?,?,?)
                ''',(fname,lname,email,number,emergencynumber,emergencyemail))
                con.commit()
                con.close()
                return redirect('/home')
            except sqlite3.Error as e:
                return str(e)
        return render_template('index.html')

@app.get('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8000)