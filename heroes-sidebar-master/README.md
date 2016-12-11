# heroes-sidebar-master

## Getting Started

Make a copy of env.py.example named env.py. Add all of the different info required.

## match.py

match.py uses an API key provided by GosuGamers to request the list of upcoming Heroes matches. If this call fails, Hermes recieves an email from email_me.py with the server's IP address. The bot then takes the first 5 from that list and uses that info to format a string using our Stylesheet guidelines. This is called in index.py.

## twitch.py

twitch.py uses Hermes' Twitch API key to request all the current Heroes streams. It grabs the top 5 streams, and then 5 random streams from the remaining list. The bot then takes those stream's info and formats into a string using our Stylesheet guidelines. This is called in index.py.

## slack.py

Once both match.py and twitch.py have constructed their strings, they're posted into a Slack channel. This is called by index.py

## email_me.py

email_me.py is used to email Hermes if the GosuGamers API call fails. This used to happen frequently, and was much more necessary than it is now. GosuGamers API call now only fails when Gosu is doing maintance. This is called in match.py

## reddit.py

reddit.py has classes that will initialize the bot with your reddit account. These are commented out because they only need to be sucvessfully called once. There are two functions **updateSidebar** and **updateSidebarNoStream** that can post to the subreddit's settings. They both function the same, one just accepts a Twitch string. The class pulls the string in /wiki/sidebar and replaces specific strings with strings that are passed in. This is called in index.py.

## index.py

index.py sets up all of the other classes. It calles match.py and twitch.py to get the correct information. It then calls reddit.py to post the information back to the subreddit. Finally, it calles slack.py to confer the information to a Slack channel. This is called by a Cron Job every 10 minutes. 
