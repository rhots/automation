import argparse

import praw

USER_AGENT = 'Flair Counter v0.0.1 by /r/heroesofthestorm'


def main():
    parser = argparse.ArgumentParser(description='Count subreddit flair usage')
    parser.add_argument('subreddit', help='subreddit name')
    parser.add_argument('--site', help='use custom praw.ini configuration site')
    args = vars(parser.parse_args())

    site = args['site']
    if site:
        reddit = praw.Reddit(site, user_agent=USER_AGENT)
    else:
        reddit = praw.Reddit(user_agent=USER_AGENT)
    subreddit = reddit.subreddit(args['subreddit'])

    flairs = {}
    total = 0
    for flair in subreddit.flair():
        css_class = flair['flair_css_class']
        user = flair['user'].name

        if css_class in flairs:
            flairs[css_class].append(user)
        else:
            flairs[css_class] = [user]

        total += 1
        if total % 1000 == 0:
            print('Processed {} flairs...'.format(total))

    flairs = sorted(flairs.items(), key=lambda x: len(x[1]), reverse=True)
    print('Total flairs: {}'.format(total))
    for flair in flairs:
        print('{0} {1}'.format(len(flair[1]), flair[0]))


main()
