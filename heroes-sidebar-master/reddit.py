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

	def constructPost(self, match):
		#constructs post, takes a match's info and formats it into reddit style
		pass

	def updateSidebar(self, matches, streams):
		sidebar = self.r.get_wiki_page('heroesofthestorm', 'sidebar')
		sidebarWiki = sidebar.content_md
		sidebarWiki = sidebarWiki.replace("%%EVENTS%%", matches);
		sidebarWiki = sidebarWiki.replace("%%STREAMS%%", streams)
		self.r.update_settings(self.r.get_subreddit('heroesofthestorm'), description=sidebarWiki)
		return sidebarWiki.encode('ascii','ignore')	

	def updateSidebarNoStream(self, matches):
		sidebar = self.r.get_wiki_page('heroesofthestorm', 'sidebar')
		sidebarWiki = sidebar.content_md
		sidebarWiki = sidebarWiki.replace("%%EVENTS%%", matches);
		# sidebarWiki = sidebarWiki.replace("%%STREAMS%%", streams)
		self.r.update_settings(self.r.get_subreddit('heroesofthestorm'), description=sidebarWiki)
		return sidebarWiki.encode('ascii','ignore')


	def upsateSidebarWeeklyRotation(self):
		pass

	def getSidebar(self):
		pass

	def makePost(self, post):
		#takes a constructed post and posts it
		pass