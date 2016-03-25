from app import app
from flask import render_template, request, url_for
from jokes import Joke
import json
import logging

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
    password = str(content.get(key_password))

    user = models.user_by_credentials(email, password)

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
