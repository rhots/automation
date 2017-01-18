import argparse
import praw


def main():
    parser = argparse.ArgumentParser(description='Get or set link flair')
    parser.add_argument('action', choices=['get', 'set'], help='get or set')
    parser.add_argument('id', help='id of the submission')
    parser.add_argument('--text', help='link flair text to set')
    parser.add_argument('--class', help='link flair CSS class to set')
    args = vars(parser.parse_args())

    reddit = praw.Reddit('moderation')
    submission = reddit.submission(args['id'])

    if args['action'] == 'get':
        print('Flair text: {0}'.format(submission.link_flair_text))
        print('Flair class: {0}'.format(submission.link_flair_css_class))
    elif args['action'] == 'set':
        submission.mod.flair(args['text'], args['class'])
        print('Link flair set')

main()
