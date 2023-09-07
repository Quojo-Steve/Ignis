from email.message import EmailMessage
import ssl
import smtplib
import sqlite3

def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    return conn

conn = connect_to_db()
query = "SELECT * FROM users"
result = conn.execute(query)
user_data = result.fetchone()
conn.close()
sender_email = 'ignisfiresystem@gmail.com'
sender_password = 'zqas taxp vtlb trfk'  # Make sure to use your actual email password

email_receiver = user_data[3]

subject = 'Subject of the Email'
body = 'This is the body of the email.'

em = EmailMessage()
em['From'] = sender_email
em['To'] = email_receiver
em['subject'] = subject 
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, email_receiver, em.as_string())


# import smtplib