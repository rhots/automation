from automation import GoogleCalendar, Rotation, Sidebar, Twitch

events = GoogleCalendar().sidebar_text()
rotation = Rotation().sidebar_text()
streams = Twitch().sidebar_text()

sidebar = Sidebar("heroesofthestaging")
sidebar.update(events, rotation, streams)
