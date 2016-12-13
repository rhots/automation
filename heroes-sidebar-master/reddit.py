import praw
import requests

from env import env
from twitch import twitch

class reddit:

	def __init__(self):
		self.r = praw.Reddit(user_agent='Heroes of the Storm Sidebar by /u/Hermes13')
		self.env = env()
		self.access_information = None

	def setup(self):
		# self.r.set_oauth_app_info(	client_id=self.env.redditClientID,
		# 						  	client_secret=self.env.redditSecretID,
		# 						  	redirect_uri=self.env.redditRedirectURI)
		# url = self.r.get_authorize_url('uniqueKey', 'identity modconfig modcontributors wikiread', True)
		# import webbrowser
		# webbrowser.open(url)	
		pass	



	def connect(self):
		self.r.set_oauth_app_info(	client_id=self.env.redditClientID,
								  	client_secret=self.env.redditSecretID,
								  	redirect_uri=self.env.redditRedirectURI)

		# self.access_information = self.r.get_access_information(self.env.redditAuthCode)

		# print self.access_information
		# self.r.set_access_credentials(**self.access_information)

		self.r.refresh_access_information(self.env.redditRefreshToken)

		authenticated_user=self.r.get_me()

	def updateSidebar(self, matches, streams, freeRotation, saleRotation):
		sidebar = self.r.get_wiki_page('kalebhermes', 'sidebar')
		sidebarWiki = sidebar.content_md
		if matches:
			sidebarWiki = sidebarWiki.replace("%%EVENTS%%", matches)
		if streams:
			sidebarWiki = sidebarWiki.replace("%%STREAMS%%", streams)
		if freeRotation:
			sidebarWiki = sidebarWiki.replace("%%FREEROTATION%%", freeRotation)
		if saleRotation:
			sidebarWiki = sidebarWiki.replace("%%SALEROTATION%%", saleRotation)

		self.r.update_settings(self.r.get_subreddit('kalebhermes'), description=sidebarWiki)
		return sidebarWiki.encode('ascii','ignore')	