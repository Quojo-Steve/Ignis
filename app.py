from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

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
                eemail TEXT NOT NULL 
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

            create_user_table()

            try:
                con = connect_to_db()
                con.execute('''
                    INSERT INTO users(
                        firstname, lastname, email, phone_no, enumber, eemail
                    ) VALUES (?,?,?,?,?,?)
                ''',(fname, lname, email, number, emergencynumber, emergencyemail))
                con.commit()
                con.close()
                return redirect('/home')
            except sqlite3.Error as e:
                return str(e)
        return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
