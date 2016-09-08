from app import app
from flask import render_template, request, url_for, session, redirect
from jokes import Joke
from users import User
import json
import logging
from crypt import crypt
import models
from secrets import SECRET_SALT, SECRET_SESSION
from datetime import timedelta

# Names for keys from JSON received and sent
key_email = 'email'
key_password = 'password'

key_redirect = 'redirect'
key_message = 'message'

key_jokeId = 'jokeId'

LOGIN_FAIL = 401
LOGIN_SUCCESS = 200

msg_fail = 'Failure'
msg_success = 'Success'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=2)


@app.route('/')
@app.route('/index/')
def index(title='HGP Home'):
    jokesList = [
    Joke("Just changed my Facebook name to \'No one\' so when I see stupid posts ",
        "I can click like and it will say \'No one\' likes this'.", jokeId=1),
    Joke("What's the difference between snowmen and snowladies?","Snowballs",jokeId=2),
    Joke("How do you make holy water?", "You boil the hell out of it",jokeId=3)
    ]
    return render_template('index.html',title=title, jokes=jokesList)


@app.route('/about/')
def about_page():
    return index('About Us')


@app.route('/login/')
def login():

    # If already logged in, redirect to view jokes
    if session.get(key_email):
        return redirect(url_for('view_joke'))
    return render_template('login.html')


@app.route('/signin', methods=['POST'])
def signin():

    content = request.get_json(force=True, silent=True)

    email = str(content.get(key_email))
    # Dont even look at the original password. Hash with salt immediately
    password_hashed = crypt(content.get(key_password), SECRET_SALT)

    user = models.user_by_credentials(email, password_hashed)

    if user:

        # TODO: Add session for logged in user
        session[key_email] = user.email
        redirectUrl = url_for('view_joke')
        print session
        jsonResponse = json.dumps({
            key_redirect: redirectUrl,
            key_message: msg_success
        })
        return jsonResponse

    else:
        jsonResponse = json.dumps({
            key_message: msg_fail,
            key_redirect: None
        })
        return jsonResponse


@app.route('/signup', methods=['GET'])
def signup():

    # If already logged in, redirect to view jokes
    if session.get(key_email):
        return redirect(url_for('view_joke'))

    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    content = request.get_json(force=True, silent=True)
    email = content.get(key_email)

    if email and models.email_available(email):
        # Dont even look at the original password. Hash with salt immediately
        password_hashed = crypt(content[key_password], SECRET_SALT)
        fname = content['fname']
        lname = content['lname']
        userType = content['userType']


        new_user = User(email, password_hashed, fname, lname, userType=userType)
        models.update_user(new_user)

        # TODO: Add session for logged in user
        session[key_email] = new_user.email
        redirectUrl = url_for('view_joke')
        print session

        jsonResponse = json.dumps({
            key_message: msg_success,
            key_redirect: redirectUrl
        })

        return jsonResponse

    else:
        jsonResponse = json.dumps({
            key_message: msg_fail,
            key_redirect: None,
            'email_unavailable': True
        })

        return jsonResponse


@app.route('/jokes')
@app.route('/jokes/<int:jokeId>')
@app.route('/jokes/categories/<category>')
def view_joke(jokeId=None, category=None):

    # If not logged in, redirect to login page
    if not session.get(key_email):
        return redirect(url_for('login'))

    the_joke = None
    if jokeId:
        the_joke = models.joke_by_jokeId(jokeId)
    elif category:
        the_joke = models.joke_by_category(category)
    else:
        the_joke = models.random_joke()

    title = the_joke.title
    content = the_joke.content
    categories = the_joke.categories
    jokeId = the_joke.jokeId
    privileged = False


    the_user = models.user_by_email(session.get(key_email))
    if the_user:
        privileged = the_user.is_privileged()


    return render_template('view_joke.html', joke_title=title, joke_content=content,
        privileged=privileged, jokeId=jokeId)

@app.route('/update_joke', methods=['POST'])
def update_joke():
    # TODO: implement
    joke = request.get_json(force=True, silent=True)
    print joke
    if 'jokeId' not in joke or 'title' not in joke or 'content' not in joke:
        return json.dumps({'msg': 'Joke update failed'})

    return {'redirect': url_for('view_joke')}

@app.route('/delete_joke', methods=['POST'])
def delete_joke():
    '''
    If jokeId is provided, the given joke is deleted from the database and user is
    redirected to a new joke.
    Otherwise, no jokeId is provided, a failure message is returned, with no redirect URL.
    '''
    if not session.get(key_email):
        return redirect(url_for('login'))

    content = request.get_json(force=True, silent=True)
    jokeId = int(content.get(key_jokeId))

    if jokeId:

        # TODO: ensure remove_joke actually works
        models.remove_joke(jokeId)
        jsonResponse = json.dumps( {
            key_jokeId: jokeId,
            key_message: msg_success,
            key_redirect: url_for('view_joke')
        })
        return jsonResponse

    else:
        jsonResponse = json.dumps( {
            key_message: msg_fail,
            key_redirect: None,
        })

        return jsonResponse
