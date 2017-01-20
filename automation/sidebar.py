import praw

from . import __version__

class Sidebar:
    """Sidebar provides a simple API to update the subreddit's sidebar
    using the template found in the wiki. It expects a praw.ini
    configuration with `sidebar_updater` site for client info."""

    def __init__(self, sub_name):
        """:param sub_name: the name of the subreddit to update the sidebar of"""

        user_agent = "script:sidebarupdater:v{0} (by /u/HotSBot)".format(__version__)

        reddit = praw.Reddit('sidebar_updater', user_agent=user_agent)
        self._subreddit = reddit.subreddit(sub_name)

    def update(self, events, freeRotation, streams):
        template = self._subreddit.wiki['sidebar'].content_md

        new_sidebar = template.replace("%%EVENTS%%", events)
        new_sidebar = new_sidebar.replace("%%FREEROTATION%%", freeRotation)
        new_sidebar = new_sidebar.replace("%%STREAMS%%", streams)

        self._subreddit.mod.update(description=new_sidebar)
