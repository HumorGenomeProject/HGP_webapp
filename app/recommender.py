from dbco import db_jokerz
import random

def pickNextJoke(currentJoke):
	"""Returns the next joke
	Using this method allows the programmer to change the criteria used and implement
	different methods without needing to refer to a different method while running the code

	Keyword Argument(s):
	currentJoke -> the joke currently being displayed that is used as a baseline for the next joke
	"""

	# return pickByUpvote(currentJoke)
	return pickByCategory(currentJoke)

def pickRandom(joke_list):
	"""Picks a random joke from the list passed in

	Keyword Argument(s):
	joke_list -> the queried list of jokes from which to pick the random joke
	"""

	jokeListRef = list(joke_list)
	while len(jokeListRef) > 0:
		tempJoke = random.choice(jokeListRef)
		if str(tempJoke['_id']) not in usedJokes:
			return tempJoke
		jokeListRef.remove(tempJoke)
	return None

def pickByUpvote(currentJoke):
	"""Picks a joke from the database of jokes based on current joke's upvotes

	Keyword Argument(s):
	currentJoke -> the joke currently being displayed that is used as a baseline for the next joke
	"""

	return pickRandom(list(jokes.find({"upvotes": {"$gte": currentJoke['upvotes']}})))

def pickByCategory(currentJoke):
	"""Picks a joke from the database of jokes based on the current joke's categories


	Keyword Argument(s):
	currentJoke -> the joke currently being displayed that is used as a baseline for the next joke
	"""

	#create an empty list to add relevant jokes to
	newList = []
	#get the set of categories for comparison purposes
	categoryCheck = categorize(currentJoke)
	#checks to see if randomly generated number is consistent with user's rating of the current joke
	oppositeDomain = random.random() > getStars() / 5.0
	#goes through overall joke list and adds jokes based on the randomly generated number
	for j in jokeList:
		if categoryCheck.isdisjoint(categorize(j)) == oppositeDomain:
			newList.append(j)
	#if no jokes meet the criteria of the randomly generated number, pick a joke from the whole list
	if len(newList) == 0: pickRandom(jokeList)
	return pickRandom(newList)

def categorize(currentJoke):
	"""Returns the categories of the joke as a set

	Keyword Argument(s):
	currentJoke -> the joke currently being displayed that is used as a baseline for the next joke
	"""

	return set(str(currentJoke['categories']).split(","))

def getStars():
	"""Prompts the user with a rating request and returns with a "stars" rating
	"""

	print "Please rate the previous joke on a scale of 1 to 5"
	while True:
		stars = int(raw_input())
		if stars >= 1 and stars <= 5: return int(stars)
		print "Please give the joke a valid rating on a scale of 1 to 5"

def displayJoke(currentJoke):
	"""Displays elements of the joke for the user to see the joke

	Keyword Argument(s):
	currentJoke -> the joke currently being displayed that is used as a baseline for the next joke
	"""

	displayContents = [joke['title'], joke['content'], joke['upvotes'], joke['categories']]
	print "*******"
	for content in displayContents:
		if content != None:
			print unicode(content) + "\n"

jokes = db_jokerz['jokes']
jokeList = list(jokes.find())
usedJokes = set([])
joke = pickRandom(jokeList)

while joke != None:
	usedJokes.add(str(joke['_id']))
	displayJoke(joke)
	joke = pickNextJoke(joke)
	print "*******"
print "Done"