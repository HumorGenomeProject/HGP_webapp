from app import app
from flask import render_template, request, url_for
from jokes import Joke
from users import User
import json
import logging
from crypt import crypt
from secrets import SECRET_SALT, SECRET_SESSION

import models

# Names for keys from JSON received and sent
key_email = 'email'
key_password = 'password'

key_redirect = 'redirect'
key_authmessage = 'authmessage'

LOGIN_FAIL = 401
LOGIN_SUCCESS = 200

msg_fail = 'Failure'
msg_success = 'Success'


@app.route('/')
@app.route('/index')
@app.route('/index/<title>')
def index(title='HGP Home'):
    jokesList = [
    Joke("Just changed my Facebook name to \'No one\' so when I see stupid posts ",
        "I can click like and it will say \'No one\' likes this'.", jokeId=1),
    Joke("What's the difference between snowmen and snowladies?","Snowballs",jokeId=2),
    Joke("How do you make holy water?", "You boil the hell out of it",jokeId=3)
    ]
    return render_template('index.html',title=title, jokes=jokesList)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signin', methods=['POST'])
def signin():

    content = request.get_json(force=True, silent=True)

    email = str(content.get(key_email))
    # Dont even look at the original password. Hash with salt immediately
    password_hashed = crypt(content.get(key_password), SECRET_SALT)

    user = models.user_by_credentials(email, password_hashed)

    if user:
        redirectUrl = url_for('index')
        jsonResponse = json.dumps({
            key_redirect: redirectUrl,
            key_authmessage: msg_success
        })
        # TODO: Add session for logged in user
        return jsonResponse

    else:
        jsonResponse = json.dumps({
            key_authmessage: msg_fail,
            key_redirect: None
        })
        return jsonResponse

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    content = request.get_json(force=True, silent=True)
    email = content[key_email]

    if models.email_available(email):
        # Dont even look at the original password. Hash with salt immediately
        password_hashed = crypt(content[key_password], SECRET_SALT)
        fname = content['fname']
        lname = content['lname']
        userType = content['userType']


        newUser = User(email, password_hashed, fname, lname, userType=userType)
        models.update_user(newUser)

        welcome_msg = "HGP - {} {}".format(newUser.fname, newUser.lname)
        redirectUrl = url_for('index', title=welcome_msg)

        jsonResponse = json.dumps({
            key_authmessage: msg_success,
            key_redirect: redirectUrl
        })

        return jsonResponse

    else:
        jsonResponse = json.dumps({
            key_authmessage: msg_fail,
            key_redirect: None,
            'email_unavailable': True
        })

        return jsonResponse
