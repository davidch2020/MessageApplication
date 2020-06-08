import os
import requests
import smtplib

from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector as msql
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = 'Domo'
socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = "david1_database"

temp_array = []
info_array = []
errors_mess = []
sign_up_errors_mess = []
username = []
one_or_zero = {}
messages = {}

mysql = MySQL(app)
bcrypt = Bcrypt(app)

if len(username) > 0:
    username = username[0]

@app.route("/<username>", methods=['GET', 'POST'])
def index1(username):

    return render_template("index.html")

@socketio.on("recieved post")
def index2(data):
    username = session.get('username', None)
    if username is None:
        return redirect(url_for('index'))
    cur2 = mysql.connection.cursor()
    cur2.execute("Select * From rooms Where Email = %s", [username])
    print("Checkpoint 1")
    data1 = cur2.fetchone()
    if data1 is None:
        room = request.sid
        cur2.execute("Insert Into rooms(Email, Room) Values (%s, %s)", (username, room))
        mysql.connection.commit()


    cur2.execute("Select Room From rooms Where Email = %s", [username])
    mysql.connection.commit()
    cur2.close()
    data1 = cur2.fetchone()
    selection = data["selection"]
    room = data["room"]
    print(room)
    join_room(room)
    print(username)
    print(selection)
    emit("upload post", {"selection": username + ": " + selection}, room=room)
    print("Checkpoint")


@app.route("/")
def index():

    if not errors_mess:
        error = ""
    else:
        error = errors_mess[0]
        errors_mess.remove(error)
    return render_template("login.html", error=error)

@app.route('/', methods=['GET', 'POST'])
def form_login():
    username = request.form['username']
    password = request.form['pass']
    cur = mysql.connection.cursor()


    #https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
    cur.execute("Select * From users1 Where email = %s AND password = %s", (username, password))
    data = cur.fetchone()
    #https://stackoverflow.com/questions/38550263/flask-python-mysql-using-where-clause-in-a-select-query-with-variable-from
    if data is None:
        return render_template('login.html', error="Password or Email is incorrect")

    else:
        session['username'] = username
        return redirect(url_for('visits'))


@app.route('/index', methods=['GET', 'POST'])
def visits():
    username = session.get('username', None)
    if username is None:
        return redirect(url_for('index'))

    return render_template('index1.html', username=username)


@app.route('/logout', methods=['GET', 'POST'])
def logout2():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/verification')
def signup():

    if not sign_up_errors_mess:
        error = ""

    else:
        error = sign_up_errors_mess[0]
        sign_up_errors_mess.remove(error)

    return render_template('signup.html', error=error)

@app.route('/verification', methods=['GET', 'POST'])
def verification():

    random_num = randint(100000, 999999)
    temp_array.append(random_num)
    username1 = request.form['user']
    password1 = request.form['pass']

    cur1 = mysql.connection.cursor()


    random_num = str(random_num)
    from_address = "davidncho11@gmail.com"
    to_address = username1

    message = MIMEMultipart('Foobar')

    message['Subject'] = 'Please Verify Your Email Address'
    message['From'] = from_address
    message['To'] = to_address
    content = MIMEText(random_num, 'plain')

    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(from_address, '1108Namwook')
    mail.sendmail(from_address, to_address, message.as_string())
    mail.close()

    info_array.append(username1)
    info_array.append(password1)

    return render_template('verification.html')


@app.route('/verification2', methods=['GET', 'POST'])

def verification2():

    random_num = temp_array[0]
    username1 = info_array[0]
    password1 = info_array[1]
    temp_array.remove(random_num)
    verification_text = request.args.get("verification-text-field")
    verification_text = int(verification_text)
    random_num = int(random_num)
    if verification_text == random_num:

        return clickedsignup(username=username1, password=password1)
        info_array.remove(username1)
        info_array.remove(password1)

@app.route('/signup', methods=['GET', 'POST'])
def clickedsignup(username, password):

    username1 = username
    password1 = password
    cur1 = mysql.connection.cursor()

    #https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
    cur1.execute("Select * From users1 Where email = %s", [username1])
    data1 = cur1.fetchone()
    #https://stackoverflow.com/questions/38550263/flask-python-mysql-using-where-clause-in-a-select-query-with-variable-from
    if data1 is None:
        cur1.execute("Insert Into users1(email, password) Values (%s, %s)", (username1, password1))
        mysql.connection.commit()
        cur1.close()
        print("It worked")
        print(type(username1))
        username1 = username1.split("@", 1)
        username1 = username1[0]
        username += username1
        session['username'] = username1
        errors_mess.append("Account created. You may now log in.")

        return redirect(url_for('index'))
    else:
        sign_up_errors_mess.append("Email already taken")
        return redirect(url_for('verification'))
