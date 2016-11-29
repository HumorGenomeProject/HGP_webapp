from dbco import db_jokerz
import random

def pickNextJoke(currentJoke):
	return pickByUpvote(currentJoke)

def pickRandom(joke_list):
	jokeListRef = list(joke_list)
	while len(jokeListRef) > 0:
		tempJoke = random.choice(jokeListRef)
		if str(tempJoke['_id']) not in usedJokes:
			return tempJoke
		jokeListRef.remove(tempJoke)
	return None

def pickByUpvote(currentJoke):
	return pickRandom(list(jokes.find({"upvotes": {"$gte": currentJoke['upvotes']}})))

def pickByCategory(currentJoke):
	newList = []
	categoryCheck = categorize(currentJoke)
	oppositeDomain = random.random() > getStars() / 5.0
	#print "Same Domain? " + str(not oppositeDomain)
	for j in jokeList:
		sameCategories = categoryCheck.isdisjoint(categorize(j))
		if categoryCheck.isdisjoint(categorize(j)) == oppositeDomain:
			newList.append(j)
	if len(newList) == 0: pickRandom(jokeList)
	return pickRandom(newList)

def categorize(currentJoke):
	return set(str(currentJoke['categories']).split(","))

def getStars():
	print "Please rate the previous joke on a scale of 1 to 5"
	while True:
		stars = int(raw_input())
		if stars >= 1 and stars <= 5: return int(stars)
		print "Please give the joke a valid rating on a scale of 1 to 5"

# dictionary of tuples: category -> {cumulative, quantity} *should be unique to users

####JOKE GENERATOR
jokes = db['jokes']
jokeList = list(jokes.find())
usedJokes = set([])
joke = pickRandom(jokeList)

while joke != None:
	usedJokes.add(str(joke['_id']))
	displayContents = [joke['title'], joke['content'], joke['upvotes'], joke['categories']]
	print "*******"
	for content in displayContents:
		if content != None:
			print unicode(content)
			print ""
	#joke = pickByUpvote(joke)
	joke = pickByCategory(joke)
	print "*******"

####



# for i in range(0,4):
# 	if joke != None:
# 		jokeID = str(joke['_id'])
# 		usedJokes.add(jokeID)
# 		print str(joke['upvotes'])
# 		joke = pickByUpvote(joke)

# joke = pickRandom(jokeList)
# #def jokeProcedure(self, joke):
# #while joke != None:
# for i in range(0,2):
# 	if joke != None:
# 		#for joke in jokes.find().limit(3):
# 		#print joke
# 		#jokeList = list(jokes.find())
# 		#joke = random.choice(jokeList)
# 		jokeID = str(joke['_id'])
# 		#
# 		#print joke['title']
# 		#print joke['content']
# 		#print joke['upvotes']
# 		usedJokes.add(jokeID)
# 		print "****COMPARISON****\n" + str(jokeID)
# 		pickNextJoke(joke)
# 		print joke['_id']
# 		print "**********"
# 		#return joke
# 		#get rating from user
# 		#pickNextJoke()
# 	#print collection()

print "Done"