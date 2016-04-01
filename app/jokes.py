import random
import json

field_title = 'title'
field_content = 'content'
field_jokeId = 'jokeId'
field_categories = 'categories'


class Joke(object):

    def __init__(self, title, content, jokeId=None, categories=None):


        self.title = str(title)
        self.content = str(content)

        # TODO: Use Mongo to determine appropriate jokeId
        if jokeId is None:
            jokeId = random.randint(54321, 16171617)

        self.jokeId = int(jokeId)

        if categories is None:
            categories = []

        self.categories = list(categories)


    def add_category(self, category):
        self.categories.append(category)

    def remove_category(self, out_category):
        updated_categories = [category for category in self.categories
            if category is not out_category]

        self.categories = updated_categories

    def set_categories(self, categories):
        self.categories = categories

    def to_json(self):
        '''
        '''
        my_joke = dict()

        my_joke[field_title] = self.title
        my_joke[field_content] = self.content
        my_joke[field_jokeId] = self.jokeId
        my_joke[field_categories] = self.categories

        return my_joke

    @classmethod
    def from_json(constructor, my_joke_json):

        my_joke = my_joke_json
        if type(my_joke_json) == str:
            my_joke = json.loads(my_joke_json)

        title = my_joke[field_title]
        content = my_joke[field_content]
        # Using get method in case these fields are null
        jokeId = my_joke.get(field_jokeId)
        categories = my_joke.get(field_categories)

        return constructor(title, content, jokeId, categories)
