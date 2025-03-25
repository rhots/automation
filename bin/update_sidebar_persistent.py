import datetime, sys, time
from automation import GoogleCalendar, Rotation, Sidebar, Twitch

sub = "heroesofthestaging"
if len(sys.argv) > 1:
    sub = sys.argv[1]

def do():
    print("Getting calendar text...")
    events = GoogleCalendar().sidebar_text()
    # rotation = Rotation().sidebar_text()
    rotation = ""
    print("Getting Twitch text...")
    streams = Twitch().sidebar_text()

    print("Updating sidebar...")
    sidebar = Sidebar(sub)
    sidebar.update(events, rotation, streams)

while True:
    print(datetime.datetime.now())
    do()
    print("Sleeping...")
    time.sleep(60)
