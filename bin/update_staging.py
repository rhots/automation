from automation import Rotation, Sidebar, Twitch

events = "No upcoming matches"
rotation = Rotation().sidebar_text()
streams = Twitch().sidebar_text()

sidebar = Sidebar("heroesofthestaging")
sidebar.update(events, rotation, streams)
