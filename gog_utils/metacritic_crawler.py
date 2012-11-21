#Metacritic crawler for finding review and user scores
#copyright (c) Jukka Pietila, 2012

import urllib2

class MetacriticCrawler:
	
	_url_start = "http://metacritic.com/game/pc/"
	_filepath = "mcdata/list.txt"

	@staticmethod
	def getScores(game_id):
		"""
		Returns None, None if score couldn't be found, otherwise both review score and user score
		IMPORTANT: the review_score can still be of type None even if user score exists, so check for it!
		"""
		url = MetacriticCrawler._findurl(game_id)
		if url == "":
			return None, None
		
		game_url = MetacriticCrawler._url_start + url
		
		response = urllib2.urlopen(game_url)
		page_source = response.read()
		review_score = ""
		user_score = ""
		#first we find reviewer score
		indx = page_source.find('v:average">')
		if indx == -1:
			#no review score to be found
			review_score = None
		else:
			offset = len('v:average">')
			review_score = page_source[indx + offset] + page_source[indx + offset + 1]
		#then user score
		#first occurence holds the user score
		#for some reason user score uses X.Y notation instead of XY like review scores
		indx = page_source.find('score_value">')
		if indx == -1:
			user_score = None
		else:
			offset = len('score_value">')
			user_score = page_source[indx + offset] + "." + page_source[indx + offset + 2]

		return review_score, user_score

	@staticmethod
	def getReviewScore(game_id):
		"""
		Returns None if score couldn't be found, otherwise returns the score as string
		"""
		url = MetacriticCrawler._findurl(game_id)
		if url == "":
			return None

		game_url = MetacriticCrawler._url_start + url		

		response = urllib2.urlopen(game_url)
		page_source = response.read()
		indx = page_source.find('v:average">')
		if indx == -1:
			#there was no average score, ergo nothing to be displayed
			return None
		#the score comes after v:average"> so we need to get the offset for that
		#we assume the game has a score with two digits. If not, results can be interesting :)
		offset = len('v:average">')
		score = page_source[indx + offset] + page_source[indx + offset + 1]
		return score

	@staticmethod
	def getUserScore(game_id):
		"""
		Returns None if score couldn't be found, otherwise returns the score as string
		"""
		url = MetacriticCrawler._findurl(game_id)
		if url == "":
			return None
		
		game_url = MetacriticCrawler._url_start + url

		response = urllib2.urlopen(game_url)
		page_source = response.read()
		indx = page_source.find('score_value">')
		offset = len('score_value">')
		user_score = page_source[indx + offset] + "." + page_source[indx + offset + 2]

		return user_score

	@staticmethod
	def getLink(game_id):
		return MetacriticCrawler._url_start + MetacriticCrawler._findurl(game_id)

	@staticmethod
	def _findurl(game_id):
		f = open(MetacriticCrawler._filepath)
		"""
		Returns the url of the game's metacritic page OR an empty string if 
		"""
		url = ""
		for line in f:
			#check that the line isn't a comment line
			if line[0] == '#':
				continue
			if line.find(game_id) != -1:
				#parse the url
				line_split = line.split()
				url = line_split[2]
				if url == 'NIL':
					#game has no metacritic-page
					f.close()
					return ""
				f.close()
				return url
		#didn't find the game_id for some reason
		f.close()
		return url
