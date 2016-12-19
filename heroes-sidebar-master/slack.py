from slacker import Slacker
from env import env
class slack():

	def __init__(self):
		self.env = env()
		self.slack = Slacker(self.env.slackAPIToken)


	def postToSlack(self, message, messageTwo, messageThree):
		sendingMessage = message + messageTwo + messageThree 
		self.slack.chat.post_message('#kalebapitests', sendingMessage)