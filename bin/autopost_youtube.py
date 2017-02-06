import bs4
import praw
import requests
import sqlite3


RSS_FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCpVdq9gLew6E76BmfB2GJ0w'


def store_video(db, video):
    q = '''INSERT INTO youtube_videos VALUES (?, ?)'''

    # using video,published directly assumes iso 8601
    db.cursor().execute(q, (video.id.text, video.published.text))
    db.commit()


def already_seen(db, video):
    q = '''SELECT EXISTS(
             SELECT video_id FROM youtube_videos WHERE video_id = ? LIMIT 1
           )'''

    c = db.cursor()
    c.execute(q, (video.id.text,))
    return c.fetchone()[0] == 1


def get_recent_videos():
    xml = requests.get(RSS_FEED_URL).text
    soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    entries = soup.select('entry')
    return entries


def post_to_reddit(r, subreddit, title, link):
    sub = r.subreddit(subreddit)
    sub.submit(title,
               url=link,
               resubmit=False,
               send_replies=False)


def main():
    first_run = True

    db = sqlite3.connect('autopost.sqlite3')
    try:
        q = '''CREATE TABLE youtube_videos (video_id text, published text)'''
        db.cursor().execute(q)
        db.commit()
    except sqlite3.OperationalError:
        first_run = False

    agent = '/r/heroesofthestorm Autoposter v0.0.1'
    reddit = praw.Reddit('sidebar_updater', user_agent=agent)

    videos = get_recent_videos()
    for vid in reversed(videos):
        if not already_seen(db, vid):
            store_video(db, vid)

            if not (first_run):
                post_to_reddit(reddit,
                               'heroesofthestaging',
                               vid.title.text,
                               vid.link['href'])
                print("Posted new video: {0}".format(vid.title.text))

    db.close()

if __name__ == "__main__":
    main()
