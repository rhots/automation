import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests
import json
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import string


class freeRotation:

	def __init__(self):
		self.freeRotation = None;

	def scrapeRotation(self):
	    # We prefer the PhantomJS driver to avoid opening any GUI windows.
	    browser = webdriver.PhantomJS()
	    browser.get("http://us.battle.net/heroes/en/heroes/#/")
	    heroes = browser.execute_script("return window.heroes;")
	    browser.quit()

	    heroes = [(h['name'], h['slug']) for h in heroes if h['inFreeHeroRotation'] == True]

	    return heroes

	def buildRotation(self):
		heroList = self.scrapeRotation()

		self.freeRotation = []
		twoHeros = {
			'samuro':'',
			'ragnaros':'',
			'varian':'',
			'zuljin':'',
		}

		self.freeRotation.append("")

		count = 0
		self.freeRotation.append("[](#spacer)")

		for i in range(14):
			if i in range(0, 3) or i in range (4, 8) or i in range(9, 12):
				forURL = heroList[count][1]

				isTwoHero = ''
				if forURL in twoHeros:
					isTwoHero = '2'

				heroName = heroList[count][0].replace(' ','').replace('.','').replace("'",'')
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





if __name__ == '__main__':
	rotation = freeRotation()
	print rotation.buildRotation()
