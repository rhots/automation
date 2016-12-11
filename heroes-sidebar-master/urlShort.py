from env import env
import requests
import json

class urlShort:

	def __init__(self):
		self.env = env()
		self.apiKey = self.env.googleShortAPIKey
		self.shortURL = ''

	def shortenURL(self, url):
		post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + self.env.googleShortAPIKey
		payload = {'longUrl' : url}
		headers = {'content-type': 'application/json'}
		r = requests.post(post_url, data=json.dumps(payload), headers=headers)
		return r.json()['id']