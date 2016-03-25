from app import app
from flask import render_template, request, url_for
import jokes
import json
import logging


# Field names -- so we aren't remembering constants all over the place
username = 'username'
password = 'password'
userField = 'userField'
passwordField = 'password'


@app.route('/')
@app.route('/index')
def index(title='Joke Review'):
    jokesList = [jokes.Joke("Just changed my Facebook name to \'No one\' so when I see stupid posts "
                        "I can click like and it will say \'No one\' likes this'.", 1),
             jokes.Joke("What's the difference between snowmen and snowladies? Snowballs",2),
             jokes.Joke("How do you make holy water? You boil the hell out of it",3)]
    return render_template('index.html',title=title, jokes=jokesList)

@app.route('/login')
def login():
    # Uses the fields described above
    return render_template('login.html', username=username, password=password, userField=userField, passwordField=passwordField)


@app.route('/signin', methods=['POST'])
def signin():

    content = request.get_json(force=True, silent=True)

    username = str(content.get('username'))
    password = str(content.get('password'))

    print content
    redirectUrl = url_for('index', title="Signin Successful")
    print redirectUrl

    jsonResponse = json.dumps({'redirectUrl' : redirectUrl})
    return jsonResponse
    # return render_template('index.html',title ='Sigin Succesful', jokes =[])
