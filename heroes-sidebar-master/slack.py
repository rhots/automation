from slacker import Slacker
from env import env
class slack():

	def __init__(self):
		self.env = env()
		self.slack = Slacker(self.env.slackAPIToken)


	def postToSlack(self, message, messageTwo):
		sendingMessage = message + messageTwo
		self.slack.chat.post_message('#kalebapitests', sendingMessage)