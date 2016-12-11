import requests, random

from email_me import email_me
from env import env


class twitch:

	def __init__(self):
		self.env = env()
		self.streamURL = 'https://api.twitch.tv/kraken/streams/?game=Heroes+of+the+Storm&limit=100&client_id=' + self.env.twitch_client_id
		self.streams = None
		self.textStreams = ''

	def getStreams(self):
		# headers = {'client_id':self.env.twitch_client_id}
		try:
			# self.streams = requests.get(self.streamURL, headers=headers)
			self.streams = requests.get(self.streamURL)
		except requests.exceptions.ConnectionError:
			email_me = email_me()
			email_me.populate_data('Couldn\'t get Twitch Stream Info')
			email_me.send_email()

		self.streams = self.streams.json()['streams']
		
		self.textStreams += 'Top\n\n'
		for stream in range(5):
			display_name = None
			status = None

			if len(self.streams[stream]['channel']['display_name']) > 11:
				trimNum = len(self.streams[stream]['channel']['display_name']) - 11
				display_name = self.streams[stream]['channel']['display_name'][:trimNum * -1] + '...'
			if len(self.streams[stream]['channel']['status']) > 16:
				trimNum = len(self.streams[stream]['channel']['status']) - 16
				status = self.streams[stream]['channel']['status'][:trimNum * -1] + '...'
			# for key, value in stream.iteritems():
				# print key, '\n', value
			self.textStreams += '* ['

			# if display_name != None:
			# 	self.textStreams += display_name + ' ~~'
			# else:	
			# 	self.textStreams += self.streams[stream]['channel']['display_name'] + ' ~~'
			# if status != None:
			# 	self.textStreams += status + '~~ '
			# else:
			# 	self.textStreams += self.streams[stream]['channel']['status'] + '~~ '

			self.textStreams += self.streams[stream]['channel']['display_name'].strip() + ' ~~'
			self.textStreams += self.streams[stream]['channel']['status'].strip() + '~~ '
			self.textStreams += '^' + str(self.streams[stream]['viewers'])
			self.textStreams += '](' + self.streams[stream]['channel']['url'] + ')' + '\n\n'

		self.textStreams += '\nDiscover\n\n'
		numbers = []
		for stream in range(5):
			number = random.randint(0, len(self.streams))
			# print number
			while number in range(5) or number in numbers or number == 100:
				number = random.randint(0, len(self.streams))
			numbers.append(number)
				# print key, '\n', value

			display_name = None
			status = None

			if len(self.streams[number]['channel']['display_name']) > 11:
				trimNum = len(self.streams[number]['channel']['display_name']) - 11
				display_name = self.streams[number]['channel']['display_name'][:trimNum * -1] + '...'
			if len(self.streams[number]['channel']['status']) > 16:
				trimNum = len(self.streams[number]['channel']['status']) - 16
				status = self.streams[number]['channel']['status'][:trimNum * -1] + '...'


			self.textStreams += '* ['


			# if display_name != None:
			# 	self.textStreams += display_name + ' ~~'
			# else:	
			# 	self.textStreams += self.streams[number]['channel']['display_name'] + ' ~~'
			# if status != None:
			# 	self.textStreams += status + '~~ '
			# else:
			# 	self.textStreams += self.streams[number]['channel']['status'] + '~~ '

			self.textStreams += self.streams[number]['channel']['display_name'].strip() + ' ~~'
			self.textStreams += self.streams[number]['channel']['status'].strip() + '~~ '
			self.textStreams += '^' + str(self.streams[number]['viewers'])
			self.textStreams += '](' + self.streams[number]['channel']['url'] + ')' + '\n\n'

		return self.textStreams



# if __name__ == '__main__':
# 	twitch = twitch()
# 	twitch.getStreams()