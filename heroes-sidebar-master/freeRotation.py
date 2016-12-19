import requests
import json
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import string
from email_me import email_me


class freeRotation:

	def __init__(self):
		self.freeRotation = None;

	def scrapeRotation(self):
		try:
			forum_page = requests.get('http://us.battle.net/heroes/en/forum/topic/17936383460')
		except request.exceptions.ConnectionError:
			data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
			email = email_me()
			message = 'Heroes Bot Didnt Update\n' + 'The Bot didn\'t update because it couldn\'t get ROTATION from Blizzard Forums. Check it out.\nThe IP is ' + str(data["ip"])
			email.populate_email('Heroes Bot Fail', message)
			email.send_email()
			sys.exit("Couldn't get ROTATION from Blizzard Forums")

		tree = html.fromstring(forum_page.text)

		results = CSSSelector('div.TopicPost-bodyContent li')
		preParsedFreeRotation = results(tree)

		heroList = [Hero.text for Hero in preParsedFreeRotation]

		for i in range(10):
			heroList[i] = heroList[i].split("(", 1)[0].replace(' ','').replace('.','').replce("'",'')

		return heroList

	def buildRotation(self):
		heroList = self.scrapeRotation()

		self.freeRotation = []
		twoHeros = {
			'Samuro':'',
			'Ragnaros':'',
			'Varian':'',
		}
		subs = {
			'ltmorales': 'lt-morales',
			'thebutcher': 'the-butcher',
		}

		self.freeRotation.append("")

		count = 0
		self.freeRotation.append("[](#spacer)")

		for i in range(14):
			if i in range(0, 3) or i in range (4, 8) or i in range(9, 12):
				forURL = heroList[count].lower()

				if forURL in subs:
					forURL = subs[forURL]

				isTwoHero = ''
				if forURL in twoHeros:
					isTwoHero = '2'

				heroName = heroList[count]
				self.freeRotation.append("[](http://us.battle.net/heroes/en/heroes/{0}/#free_rotation{2}#{1})".format(forURL, heroName, isTwoHero))
				count = count + 1

			if i == 3 or i == 8 or i == 12:
				self.freeRotation.append("[](#spacer)")

			if i == 13:
				self.freeRotation.append("[](#bottom)")

		string = ''
		for item in self.freeRotation:
			string += item + '\n'
		return string





# if __name__ == '__main__':
# 	rotation = freeRotation()
# 	print rotation.buildRotation()
