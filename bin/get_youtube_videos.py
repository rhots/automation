# This script fetches the latest YouTube videos from the official Heroes of the
# Storm channel: https://www.youtube.com/channel/UCpVdq9gLew6E76BmfB2GJ0w.

import bs4
import requests

RSS_FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCpVdq9gLew6E76BmfB2GJ0w'

xml = requests.get(RSS_FEED_URL).text
soup = bs4.BeautifulSoup(xml, 'lxml-xml')
entries = soup.select("entry")

for e in entries:
    print(e.link['href'], e.title.text)
