import requests
import requests
import json
from lxml import html
from lxml.cssselect import CSSSelector
import requests
from datetime import datetime
import string
import praw
import time

class freeHeroRotationUpdate:

	def __init__(self):
		self.preUpdateSideBarText = None;
		self.postUpdatedSideBarText = "";
		self.freeRotation = None;
		self.saleRotation = None;

	def getPreUpdateSideBar(self):
		wikiSideBarData = requests.get("http://www.reddit.com/r/heroesofthestorm/wiki/sidebar.json")
		while(wikiSideBarData.text == '{"message": "Too Many Requests", "error": 429}'):
			print "waittime"
			time.sleep(1)
			wikiSideBarData = requests.get("http://www.reddit.com/r/heroesofthestorm/wiki/sidebar.json")

		self.preUpdateSideBarText = wikiSideBarData.json()['data']['content_md']

	def getFreeRotation(self):
		forum_page = requests.get('http://us.battle.net/heroes/en/forum/topic/17936383460')
		tree = html.fromstring(forum_page.text)

		results = CSSSelector('div.TopicPost-bodyContent li')
		preParsedFreeRotation = results(tree)

		self.freeRotation = [Hero.text for Hero in preParsedFreeRotation]

		numberTwoHeroes = {
			'#Samuro':'',
			'#Ragnaros':'',
			'#Varian':'',
		}

		for i in range(10):
			self.freeRotation[i] = self.freeRotation[i].split("(", 1)[0].replace(' ','').replace('.','') + '#'

			if self.freeRotation[i] in numberTwoHeroes:
				self.freeRotation[i] = self.freeRotation[i] + '2'



	def buildNewFreeRotation(self):
		text_to_replace = []

		text_to_replace.append("")

		count = 0
		text_to_replace.append("[](#spacer)")

		for i in range(14):
			if i in range(0, 3) or i in range (4, 8) or i in range(9, 12):
				forURL = self.freeRotation[count].lower()
				heroName = self.freeRotation[count]
				text_to_replace.append("[](http://us.battle.net/heroes/en/heroes/{0}/#free_rotation{1})".format(forURL, heroName))
				count = count + 1

			if i == 3 or i == 8 or i == 12:
				text_to_replace.append("[](#spacer)")

			if i == 13:
				text_to_replace.append("[](#bottom)")

		self.freeRotation = text_to_replace

	def assembleNewFreeRotation(self):
		self.preUpdateSideBarText = string.split(self.preUpdateSideBarText, '\n')

		for i in range(len(self.preUpdateSideBarText)):
			if "#Free Hero Rotation" in self.preUpdateSideBarText[i]:
				for j in range(16):
					self.preUpdateSideBarText[i+j+1] = self.freeRotation[j]

	def getSaleRotation(self):
		forum_page = requests.get('http://us.battle.net/heroes/en/forum/topic/18183929301')
		tree = html.fromstring(forum_page.text)

		results = CSSSelector('div.TopicPost-bodyContent li:contains("Sale")')
		preParsedSaleRotation = results(tree)

		self.saleRotation = [SaleItem.xpath("string()") for SaleItem in preParsedSaleRotation]

	def buildNewSaleRotation(self):
		saleDate = '#Weekly Sale'

		text_to_replace = []
		text_to_replace.append(saleDate)
		count = 0
		# 7 if only 3, 13 if 6 for sale
		for i in range(7):
		# for i in range(13):
			if i % 2 == 0:
				text_to_replace.append("")
			else:
				text_to_replace.append(self.saleRotation[count])
				count = count + 1

		self.saleRotation = text_to_replace

	def assembleNewSaleRoation(self):
		print self.saleRotation
		for i in range(len(self.preUpdateSideBarText)):
			if "#Free Hero Rotation" in self.preUpdateSideBarText[i]:
				# 7 if there's only three for sale, 13 if there are 6 for sale
				for j in range(7):
				# for j in range(13):
					self.preUpdateSideBarText[i+j+18] = self.saleRotation[j]


		for line in self.preUpdateSideBarText:
			self.postUpdatedSideBarText = self.postUpdatedSideBarText + "\n" + line

	def postToSubredditWiki(self):
		r = praw.Reddit(user_agent="Heroes of the Storm Free/Sale Rotation Sidebar Update")
		r.login('USERNAME', 'PASSWORD')

		r.edit_wiki_page('heroesofthestorm', 'sidebar', self.postUpdatedSideBarText)
		print "posted"





if __name__ == '__main__':
	sidebar = freeHeroRotationUpdate()
	sidebar.getPreUpdateSideBar()
	sidebar.getFreeRotation()
	sidebar.buildNewFreeRotation()
	sidebar.assembleNewFreeRotation()
	sidebar.getSaleRotation()
	sidebar.buildNewSaleRotation()
	sidebar.assembleNewSaleRoation()
	sidebar.postToSubredditWiki()
