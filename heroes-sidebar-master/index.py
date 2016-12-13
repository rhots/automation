from match import match
from reddit import reddit
from freeRotation import freeRotation
from email_me import email_me
from twitch import twitch
from slack import slack
import time
class index:

	def __init__(self):
		self.match = match()
		self.reddit = reddit()
		self.email_me = email_me()
		self.twitch = twitch()
		self.freeRotation = freeRotation()
		self.slack = slack()



	def run(self):
		self.match.getMatches()
		matches = self.match.formatMatches()
		streams = self.twitch.getStreams()
		freeRotation = self.freeRotation.buildRotation()
		saleRotation = self.freeRotation.buildSales()
		# self.reddit.setup()
		self.reddit.connect()
		self.reddit.updateSidebar(matches, streams, freeRotation, saleRotation)
		self.slack.postToSlack(matches, streams, freeRotation, saleRotation)
		# self.email_me.populate_email('Heroes Bot Posted', matches)
		# self.email_me.send_email()
		#self.sidebar.run()



if __name__ == '__main__':
	bot = index()
	bot.run()
