# HGP Web App
This is the front-facing web app for the  Georgia Tech Humor Genome project.

## Dependencies
This web app runs on the Flask framework and MongoDB. You'll need the following:

- Python 2.7
- MongoDB
- Flask
- PyMongo

Python dependencies:
```
pip install flask pymongo
```

## Running the App
```
python run.py
```


### Structure
Right now, the application is still in the development phase, so much is likely to change. Here are some of the basics though:

1. __Jokes:__ These are python representations of jokes stored in our MongoDB collections. They each _must_ contain a title (reel) and content (the punchline). These will be visible to users. For house-keeping on the server-side (including for the recommendation system aspect of this project), a Joke also consists of categories and a jokeId. See __jokes.py__ for more details.


2. __Users__: These are the actual users that will interact with the site. We will have two types of users: _privileged_ and _regular_. Privileged users are internal to the project that are helping clean up jokes (separating reel from punchlines, categorizing, etc). Regular users can only rate jokes and discover jokes based on their rating preferences or queries for certain content/categories. For house-keeping, there are userIds.


### Initialize Your DB
To even begin working with this project, you'll likely want a few sample jokes and users in your database. Run the following commands in a terminal to get up and running:

You must have mongo installed properly for this portion

In one terminal:
```bash
mongod  # This sets up the MongoDB server
```

While that runs, in another terminal:
```bash
mongo
use hgp_webapp
# The content we will insert here is taken from ex_jokes.json
# However, you can copy everything here directly over
db.jokes.insert(
[
    {
        "jokeId": 54321,
        "title": "Why did the chicken cross the road?",
        "content": "To get away from this joke.",
        "categories": [
            "Animals",
            "Slapstick"
        ]
    },
    {
        "jokeId": 54322,
        "title": "How do you make holy water?",
        "content": "You boil the hell out of it.",
        "categories": [
            "Religion",
            "Pun"
        ]
    }
]
)
# The content we will insert here is taken from ex_users.json
db.users.insert(
[
    {
        "fname": "Osama",
        "lname": "Sakhi",
        "email": "derp@example.com",
        "password": "gojackets",
        "userId": 12345,
        "ratings": {
            "54321": 3,
            "54322": 5
        }
    },
    {
        "fname": "Eric",
        "lname": "S",
        "email": "dude@example.com",
        "password": "hackers",
        "userId": 12346,
        "ratings": {
            "54321": 4,
            "54322": 2
        }
    },
    {
        "fname": "Matt",
        "lname": "I",
        "email": "bro@example.com",
        "password": "stuff",
        "userId": 12347,
        "ratings": {
            "54321": 2,
            "54322": 4
        }
    }
]
)
```
