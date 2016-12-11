import requests
import sys
import urllib
import json

from env import env
from urlShort import urlShort
from datetime import datetime, timedelta

from email_me import email_me

class match:

	def __init__(self):
		self.env = env()
		self.urlShort = urlShort()
		self.matches = {}
		self.r = ''
		self.matchLimit = 5 
		self.body = ''

	def getMatches(self):
		urlString = 'http://gosugamers.net/api/matches?game=heroesofthestorm&apiKey=' + self.env.ggKey

		try:
		    self.r = requests.post(urlString)
		except requests.exceptions.ConnectionError:
			data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
			email = email_me()
			message = 'Heroes Bot Didnt Update\n' + 'The Bot didn\'t update because it couldn\'t get info from Gosu. Check it out.\nThe IP is ' + str(data["ip"])
			email.populate_email('Heroes Bot Fail', message)
			email.send_email()
			sys.exit("Couldn't get matches from GosuGamers")

		self.matches = self.r.json()['matches']
		return self.matches

	def formatMatches(self):
		if len(self.matches) < self.matchLimit:
			self.matchLimit = len(self.matches)

		for index in range(self.matchLimit):
			shortUrl = self.urlShort.shortenURL(self.matches[index]['pageUrl'])
			timetill = self.formatTime((datetime.strptime(self.matches[index]['datetime'], "%Y-%m-%dT%H:%M:%S+00:00") - datetime.utcnow()))

			self.body = self.body + '>>> [~~' + self.matches[index]['tournament']['name']

			if (self.matches[index]['isLive'] == True) or timetill == None:
				self.body = self.body + '~~\n~~LIVE~~\n'
			else:
				self.body = self.body + '~~\n~~' + timetill + '~~\n'

			self.body = self.body + '~~' + self.matches[index]['firstOpponent']['name'] + '~~\n~~' + self.matches[index]['secondOpponent']['name'] + '~~]\n'
			self.body = self.body + '(' + shortUrl + ')\n'
			#countryCodeOne = self.matches[index]['firstOpponent']['country']['countryCode'].encode('ascii','ignore')
			#countryCodeTwo = self.matches[index]['secondOpponent']['country']['countryCode'].encode('ascii','ignore')
			#self.body = self.body + '[](/' + countryCodeOne.lower() + ')\n[](/' + countryCodeTwo.lower() + ')\n'
			self.body = self.body + '\n[](#matchSpacer)\n\n'

		if self.body == '':
			self.body = 'No Upcoming Matches'
			
		return self.body	

	def enterDatabase(self):
		#make an entry in the database if match is live and not in database
		pass

	def formatTime(self, datetime):
		days = datetime.days
		hours = int(datetime.seconds / 60) / 60
		minutes = int((datetime.seconds - (hours * 60 * 60)) / 60)

		formatted = ''

		if days != 0:
			formatted = formatted + str(days) + 'd '
		if hours != 0:
			formatted = formatted + str(hours) + 'h '
		minutes = self.roundToFive(minutes)

		formatted = formatted + str(minutes) + 'm'

		return formatted

	def roundToFive(self, x, base=5):
	    return int(base * round(float(x)/base))



