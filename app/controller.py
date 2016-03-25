from app import app
from flask import render_template, request, url_for
from jokes import Joke
import json
import logging

import models

# Field names -- so we aren't remembering constants all over the place
field_email = 'email'
field_password = 'password'
field_emailField = 'emailField'
field_passwordField = 'password'

field_redirect = 'redirect'
field_authmessage = 'authmessage'

LOGIN_FAIL = 401
LOGIN_SUCCESS = 200

msg_fail = 'Failure'
msg_success = 'Success'


@app.route('/')
@app.route('/index')
@app.route('/index/<title>')
def index(title='HGP Home'):
    jokesList = [Joke("Just changed my Facebook name to \'No one\' so when I see stupid posts "
                        "I can click like and it will say \'No one\' likes this'.", 1),
             Joke("What's the difference between snowmen and snowladies? Snowballs",2),
             Joke("How do you make holy water? You boil the hell out of it",3)]
    return render_template('index.html',title=title, jokes=jokesList)


@app.route('/login')
def login():
    return render_template('login.html', email=field_email, password=field_password, emailField=field_emailField, passwordField=field_passwordField)


@app.route('/signin', methods=['POST'])
def signin():

    content = request.get_json(force=True, silent=True)

    email = str(content.get(field_email))
    password = str(content.get(field_password))

    user = models.user_by_credentials(email, password)

    if user:
        redirectUrl = url_for('index')
        jsonResponse = json.dumps({
            field_redirect: redirectUrl,
            field_authmessage: msg_success
        })
        # TODO: Add session for logged in user
        return jsonResponse

    else:
        jsonResponse = json.dumps({
            field_authmessage: msg_fail
        })
        return jsonResponse
