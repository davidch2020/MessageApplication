import os
import requests
import smtplib
import string
import random
import re

from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector as msql
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date


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

temp_variable = 0
temp_array = []
info_array = []
errors_mess = []
sign_up_errors_mess = []
username = []
one_or_zero = {}
messages = {}
posts = []
saved_posts = {}
likes_for_posts = {}
current_username = []
mysql = MySQL(app)
now = datetime.now()
date = date.today()
if len(username) > 0:
    username = username[0]

@app.route("/<username>", methods=['GET', 'POST'])
def index1(username):
    current_username.append(username)
    username5 = session.get('username', None)
    cur3 = mysql.connection.cursor()
    cur3.execute("Select email From users1 Where email = %s", [username5])
    data3 = cur3.fetchone()

    username5 = username5.split("@", 1)
    username5 = username5[0]

    if username == username5:
        bool = 1

    else:
        bool = 0

    cur3.execute("Select roomid From rooms Where username = %s", [username])
    data2 = cur3.fetchone()
    socketio.emit("room_id", {"room_id":data2}, broadcast=True)

    cur3.execute("Select email from users1")
    data4 = cur3.fetchall()

    num = 0
    username_in_database = 0

    for i in data4:
        i = data4[num]

        i = i[0]
        i = i.split("@", 1)
        i = i[0]

        if username == i:
            username_in_database = 1
            break

        else:
            num += 1

    if username_in_database == 0:
        return redirect(url_for('index'))

    res = not saved_posts
    if username5 in saved_posts:
        if res == False and username == username5:
            y = len(saved_posts[username5])

    else:
        y = 0

    cur3.execute("Select post_id, liked From Likes Where username = %s AND owner = %s Order By post_id", (username5, username))
    data5 = cur3.fetchall()
    if data5 is None:
        data5 = []

    else:
        print(data5)

    return render_template("index.html", bool=bool, posts=saved_posts, username=username, y=y, likes=likes_for_posts, data=data5)

@socketio.on("recieved post")
def index2(data):
    username = session.get('username', None)
    if username is None:
        return redirect(url_for('index'))

    username = username.split("@", 1)
    username = username[0]
    selection = data["selection"]
    room = data["room"]

    if username in saved_posts:
        saved_posts[username].append(selection)

    else:
        saved_posts.update( { username:[selection] } )

    if current_username[0] in likes_for_posts:
        likes_for_posts[current_username[0]].append(0)

    else:
        likes_for_posts.update( {current_username[0]:[0]} )

    print(saved_posts)
    x = len(saved_posts[username])
    join_room(room)
    emit("upload post", {"selection": username + ": " + selection, "length": x}, room=room)
    leave_room(room)

@socketio.on("delete")
def deleteFunction(data):
    current_username_1 = current_username[0]
    button_id = data["button_id"]
    button_id = int(button_id)
    button_id_off = int(button_id)
    username = session.get('username', None)
    username = username.split('@', 1)
    username = username[0]
    if len(saved_posts[username]) == 1:
        print("Checkpoint")
        button_id = 0

    try:
        del saved_posts[username][button_id]

    except IndexError:
        button_id = button_id - 1
        del saved_posts[username][button_id]

    del likes_for_posts[username][button_id]
    print(saved_posts[username])

    cursor = mysql.connection.cursor()
    cursor.execute("Select * From Likes Where owner = %s AND post_id = %s", (current_username_1, button_id_off))
    data3 = cursor.fetchone()
    if data3 is not None:
        cursor.execute("Delete From Likes Where owner = %s AND post_id = %s", (current_username_1, button_id_off))
        mysql.connection.commit()
        print("Here")

#like_button
@socketio.on("like")
def like(data):
    current_username_1 = current_username[0]
    print(current_username_1)
    like_id = data["like_id"]
    res = [re.findall(r'(\w+?)(\d+)', like_id)[0]]
    id = res[0][1]
    id = int(id)


    try:
        if current_username_1 in likes_for_posts:
            likes_for_posts[current_username_1][id] += 1

        else:
            likes_for_posts.update( { current_username_1:[1] } )

    except IndexError:
        likes_for_posts[current_username_1][id - 1] += 1


    username = session.get('username', None)
    username = username.split('@', 1)
    username = username[0]

    cursor = mysql.connection.cursor()
    cursor.execute("Select * From Likes Where owner = %s AND post_id = %s AND username = %s", (current_username_1, id, username))
    data3 = cursor.fetchone()
    if data3 is None:
        if id != 0:
            for i in range(id):
                cursor.execute("Select * From Likes Where owner = %s AND post_id = %s AND username = %s",(current_username_1, i, username))
                cursor_data = cursor.fetchone()
                if cursor_data is None:
                    cursor.execute("Insert Into Likes(post_id, username, liked, owner) Values (%s, %s, %s, %s)", (i, username, False, current_username_1))

        cursor.execute("Insert Into Likes(post_id, username, liked, owner) Values (%s, %s, %s, %s)", (id, username, True, current_username_1))
        mysql.connection.commit()
        print("Committed")

    else:
        cursor.execute("Update Likes Set liked = %s Where username = %s AND owner = %s AND post_id = %s", (True, username, current_username_1, id))
        mysql.connection.commit()
        print("Updated")

@socketio.on("unlike")
def unlike(data):
    current_username_1 = current_username[0]
    username = session.get('username', None)
    username = username.split('@', 1)
    username = username[0]
    unlike_id = data['unlike_id']
    likes_for_posts[current_username_1][unlike_id] -= 1

    cursor = mysql.connection.cursor()
    cursor.execute("Update Likes Set liked = %s Where username = %s AND owner = %s AND post_id = %s", (False, username, current_username_1, unlike_id))
    mysql.connection.commit()

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

    cur.execute("Select * From users1 Where email = %s AND password = %s", (username, password))
    data = cur.fetchone()

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

    return render_template('index1.html', username=username, searched_user=1)

@app.route('/diff_index', methods=['GET', 'POST'])
def search_users():
    username = session.get('username', None)
    user = request.form['user']
    cursor = mysql.connection.cursor()
    print("Checkpoint Here")
    cursor.execute("Select email From users1 Where email = %s", [user])
    data = cursor.fetchall()

    data = data[0][0]
    data = data.split("@", 1)
    data = data[0]

    print(data)

    return render_template('index1.html', username=username, searched_user=[data])


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
    mail.login(from_address, 'insert_password_here')
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

    cur1.execute("Select * From users1 Where email = %s", [username1])
    data1 = cur1.fetchone()

    if data1 is None:
        cur1.execute("Insert Into users1(email, password) Values (%s, %s)", (username1, password1))
        mysql.connection.commit()
        username1 = username1.split("@", 1)
        username1 = username1[0]
        username += username1
        session['username'] = username1
        N = 7
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        cur1.execute("Insert Into rooms(username, roomid) Values (%s, %s)", (username1, res))
        mysql.connection.commit()
        cur1.close()
        errors_mess.append("Account created. You may now log in.")

        return redirect(url_for('index'))
    else:
        sign_up_errors_mess.append("Email already taken")
        return redirect(url_for('verification'))
