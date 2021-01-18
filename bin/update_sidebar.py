import sys
from automation import GoogleCalendar, Rotation, Sidebar, Twitch

sub = "heroesofthestaging"
if len(sys.argv) > 1:
    sub = sys.argv[1]

events = GoogleCalendar().sidebar_text()
# rotation = Rotation().sidebar_text()
rotation = ""
streams = Twitch().sidebar_text()

sidebar = Sidebar(sub)
sidebar.update(events, rotation, streams)
