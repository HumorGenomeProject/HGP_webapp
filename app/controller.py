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
from field_names import user_privileged

# Names for keys from JSON received and sent
key_email = 'email'
key_password = 'password'
key_userType = 'userType'

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
def index():
    """
    Renders the Home page.
    """
    return render_template('index.html', title="Welcome to the Humor Genome Project")


@app.route('/about/')
def about_us():
    """
    Renders the About Us page.
    """
    return render_template('index.html', title="About Us")

@app.route('/account/')
def account():
    """
    Renders the My Account page. If there is no logged in user, redirects to
    Login page.
    """
    # If not logged in, redirect to login page
    if not session.get(key_email):
        return redirect(url_for('index'))

    return render_template('index.html', title="My Account")

@app.route('/login/')
def login():
    """
    Renders the Login page. If user already logged in, redirects to
    View Joke page.
    """
    # If already logged in, redirect to view jokes
    if session.get(key_email):
        return redirect(url_for('view_joke'))
    return render_template('login.html')

@app.route('/logout', methods=["POST"])
def logout():
    """
    Logs a user out of their session.
    """
    # TODO: Fix
    response_json = {}
    if session.get(key_email):
        print type(session)
        print str(session)
        session[key_email] = None
        session[key_userType] = None

        response_json['redirect'] = url_for('index')
        response_json['msg'] = 'Logout successful'
    else:
        response_json['redirect'] = None
        response_json['msg'] = 'Logout failed'

    return json.dumps(response_json)


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
        session[key_userType] = user.userType
        redirectUrl = url_for('view_joke')

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
        session[key_userType] = new_user.userType
        redirectUrl = url_for('view_joke')

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


@app.route('/view_joke')
@app.route('/view_joke/<int:jokeId>')
@app.route('/view_joke/categories/<category>')
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
    privileged = session.get(key_userType) == user_privileged

    return render_template('view_joke.html', joke_title=title, joke_content=content,
        privileged=privileged, jokeId=jokeId)


@app.route('/update_joke', methods=['POST'])
def update_joke():
    if not session.get(key_email):
        return redirect(url_for('login'))

    if session.get(key_userType) != user_privileged:
        return json.dumps({'msg': 'Must be an elevated user to modify or delete a joke.'})

    joke = request.get_json(force=True, silent=True)
    print joke
    print "joke_type: {}".format(type(joke))

    if 'jokeId' not in joke or 'title' not in joke or 'content' not in joke:
        return json.dumps({'msg': 'Joke update failed'})

    joke['jokeId'] = int(joke['jokeId'])

    the_joke = models.joke_by_jokeId(joke['jokeId'])
    if the_joke is None:
        return json.dumps({'msg': 'No joke found with that jokeId'})

    print "JokeId: {}".format(joke['jokeId'])

    # Now, make direct modifications to the joke content and title
    the_joke.title = joke['title']
    the_joke.content = joke['content']

    # Save new joke to database
    models.update_joke(the_joke)

    return json.dumps({'redirect': url_for('view_joke')})


@app.route('/delete_joke', methods=['POST'])
def delete_joke():
    '''
    If jokeId is provided, the given joke is deleted from the database and user is
    redirected to a new joke.
    Otherwise, no jokeId is provided, a failure message is returned, with no redirect URL.
    '''
    if not session.get(key_email):
        return redirect(url_for('login'))

    if session.get(key_userType) != user_privileged:
        return json.dumps({'msg': 'Must be an elevated user to modify or delete a joke.'})

    content = request.get_json(force=True, silent=True)

    try:
        jokeId = int(content.get(key_jokeId))
    except ValueError, e:
        print "Failed to convert jokeId to int: {}".format(e)
        jokeId = None

    # To delete, must have jokeId and user must be privileged
    if jokeId and session.get(key_userType) == user_privileged:

        # TODO: ensure remove_joke actually works
        print "Removing Joke w/ jokeId: {}".format(jokeId)
        models.remove_joke(jokeId)
        jsonResponse = json.dumps( {
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
