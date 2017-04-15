#!/usr/bin/env python3

from flask import Flask, request, render_template, url_for, make_response, redirect
from hashlib import sha256


SALT = 'AT9RJPm1HckeBKKv'
MAX_IMAGES_ON_PAGE = 20
USERS_FILE_LOCATION = 'users.txt'


class Image:
    def __init__(self, author, src):
        self.author = author
        self.src = src
        


class User:
    def __init__(self, username, passwd, motto):
        self.username = username
        self.passwds = [ passwd ]
        self.images = []
        self.motto = motto


def load_users(users_file):
    result = dict()
    with open(users_file, 'rt') as f:
        lines = f.readlines()
    for line in lines:
        username, passwd, motto = line.strip().split(':')
        result[username] = User(username, passwd, motto)
    return result


users = load_users(USERS_FILE_LOCATION)
app = Flask(__name__, static_folder='static', static_url_path='')


def get_username():
    salted_username = request.cookies.get('username')
    if salted_username is None:
        return salted_username

    username, hmac = salted_username.split(':')
    if sha256((username + SALT).encode('utf-8')).hexdigest() != hmac:
        return None
    return username


def set_username(resp, username):
    salted_username = sha256((username + SALT).encode('utf-8')).hexdigest()
    resp.set_cookie('username', '%s:%s' % (username, salted_username))


def get_images(username):
    images = [] + users[username].images
    if username.startswith('m00t_'):
        images = users[username.lstrip('m00t_')].images + images
    else:
        images = users['m00t_' + username].images + images
    return images[:MAX_IMAGES_ON_PAGE]


@app.route("/")
def root():
    username = get_username()
    if not username in users:
        return render_template("signin.html", content={})

    return render_template("index.html", content={
        'username': username,
        'images': get_images(username),
        'motto': users[username].motto,
    })


@app.route("/signin")
def signin():
    username = request.args.get('username')
    passwd = request.args.get('passwd')

    if not username or not passwd:
        return render_template("signin.html", content={
            'error': 'Login or password are not specified',
        })

    if not username in users or not passwd in users[username].passwds:
        return render_template("signin.html", content={
            'error': 'Login or password are invalid',
        })

    resp = make_response(redirect(url_for('root')))
    set_username(resp, username)
    return resp


@app.route("/chpasswd")
def chpasswd():
    username = get_username()
    if not username in users:
        return render_template("signin.html", content={})

    new_passwd = request.args.get('new_passwd')
    if new_passwd:
        users[username].passwds.append(new_passwd)

    return redirect(url_for('root'))


@app.route("/addimg")
def addimg():
    username = get_username()
    if not username in users:
        return render_template("signin.html", content={})

    src = request.args.get('src')
    if src:
        users[username].images.append(Image(username, src))

    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
