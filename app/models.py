from dbco import db

from users import field_userId, field_email, field_password, User
from jokes import field_jokeId, field_categories, Joke

def user_by_userId(userId):
    userJson = db.users.findOne({ field_userId: userId})
    if userJson:
        user = User.from_json(userJson)
        return user

    else:
        return None


def user_by_credentials(email, password):
    userJson = db.users.find_one({
        field_email: email,
        field_password : password
    })

    if userJson:
        user = User.from_json(userJson)
        return user

    else:
        return None

def joke_by_jokeId(jokeId):
    jokeJson = db.jokes.findOne({ field_jokeId: jokeId})

    if jokeJson:
        joke = Joke.from_json(jokeJson)
        return joke
    else:
        return None


def joke_by_categories(categories):
    if type(categories) != list:
        categories = list(categories)
    jokesJson = db.jokes.find({field_categories: {'$in': categories}})
    return map(Joke.from_json, jokesJson)

def joke_by_category(category):
    jokes = joke_by_categories([category])
    if jokes:
        return jokes[0]
    else:
        return None
