import random
import json

field_fname = 'fname'
field_lname = 'lname'
field_email = 'email'
field_password = 'password'
field_userId = 'userId'
field_ratings = 'ratings'
field_userType = 'userType'

user_regular = 'regular'
user_privileged = 'privileged'

class User(object):

    def __init__(self, email, password, fname, lname, userId=None, userType=None, ratings=None):

        # If any of the following are None, raise error
        if not all([fname, lname, email, password]):
                raise ValueError

        self.fname = str(fname)
        self.lname = str(lname)
        self.email = str(email)
        self.password = str(password)

        # TODO: Use Mongo to determine appropriate userId
        if userId is None:
            userId = random.randint(12345, 998765)

        self.userId = int(userId)

        if userType is None or userType != user_privileged:
            userType = user_regular

        self.userType = str(userType)

        if ratings is None:
            ratings = {}

        self.ratings = dict(ratings)

    def get_joke_rating(self, jokeId):
        '''
        If a rating is found for a given jokeId, returns the rating.
        Otherwise, returns a -1 to indicate no rating.
        '''
        rating = self.ratings.get(jokeId)
        if rating is None:
            rating = -1

        return rating


    def set_joke_rating(self, jokeId, rating):
        self.ratings[jokeId] = rating


    def is_privileged(self):
        return self.userType == user_privileged

    def find_all_rated_jokes(self):
        jokeIds = list(self.ratings.keys())
        return jokeIds

    def to_json(self):
        '''
        Serializes the python object into JSON.
        '''

        my_user = dict()

        my_user[field_fname] = self.fname
        my_user[field_lname] = self.lname
        my_user[field_email] = self.email
        my_user[field_password] = self.password
        my_user[field_userId] = self.userId
        my_user[field_userType] = self.userType
        my_user[field_ratings] = self.ratings

        return my_user

    @classmethod
    def from_json(constructor, my_user_json):
        '''
        Given a JSON representation of a User object, this function will deserialize it into a proper python User object.
        '''
        my_user = my_user_json
        if type(my_user_json) == str:
            my_user = json.loads(my_user_json)


        fname = my_user[field_fname]
        lname = my_user[field_lname]
        email = my_user[field_email]
        password = my_user[field_password]

        # Using get method in case these fields are null
        userId = my_user.get(field_userId)
        userType = my_user.get(field_userType)
        ratings = my_user.get(field_ratings)

        return constructor(email, password, fname, lname, userId, userType, ratings)


    def __str__(self):
        contents = "{} {} : {}".format(self.fname, self.lname, self.email)
        return contents
