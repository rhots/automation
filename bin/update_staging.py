from automation import Gosugamers, Rotation, Sidebar, Twitch

events = Gosugamers().sidebar_text()
rotation = Rotation().sidebar_text()
streams = Twitch().sidebar_text()

sidebar = Sidebar("heroesofthestaging")
sidebar.update(events, rotation, streams)
