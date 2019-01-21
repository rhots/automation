from datetime import datetime, timedelta
import re

from dateutil.tz import UTC
import ics
import requests


class GoogleCalendar:
    CALENDAR_URL = 'https://calendar.google.com/calendar/ical/cnn3isjfigrc1etop91np7f22c@group.calendar.google.com/public/basic.ics'
    NUM_EVENTS = 5
    MATCH_FORMAT_STRING = '>>> [~~{tournament}~~\n~~{starts_in}~~\n~~{team1}~~\n~~{team2}~~]\n({url})\n\n[](#matchSpacer)\n'

    def __init__(self):
        self.url_regex = re.compile(r'\[(.+?)\]\((.+?)\)')

    def sidebar_text(self):
        'Return the next NUM_EVENTS from CALENDAR_URL formatted for the old reddit sidebar.'
        matches = self._get_next_matches()
        if not matches:
            return 'No upcoming matches.'
        return self._format_matches(matches)

    def _get_next_matches(self):
        now = datetime.now(UTC)
        events = ics.Calendar(requests.get(self.CALENDAR_URL).text).events
        events = sorted(
            [event for event in events if event.end.astimezone(UTC) >= now],
            key=lambda event: event.begin)[:self.NUM_EVENTS]
        matches = []
        for event in events:
            # Example event title: "Dignitas vs. Tempo Storm"
            title_words = event.name.split(' ')
            team1, team2 = '', ''
            for i, word in enumerate(title_words):
                if word.lower() in ['vs', 'vs.', '-']:
                    team1 = ' '.join(title_words[:i])
                    team2 = ' '.join(title_words[i + 1:])
                    break
            if not team1 and not team2:
                split_i = len(title_words) // 2
                team1 = ' '.join(title_words[:split_i])
                team2 = ' '.join(title_words[split_i:])
            # Location should have a list of reddit-formatted URLs, like:
            # "[Stream](...) | [Bracket](...) | [Liquipedia](...)"
            re_matches = self.url_regex.finditer(event.location)
            stream_url = ''
            bracket_url = ''
            for re_match in re_matches:
                name, url = re_match.group(1), re_match.group(2)
                if not stream_url and 'stream' in name.lower():
                    stream_url = url
                if not bracket_url and not 'stream' in name.lower():
                    bracket_url = url
            if bracket_url:
                url = bracket_url
            elif stream_url:
                url = stream_url
            else:
                url = 'https://liquipedia.net/heroes/Main_Page'
            # The regex breaks on things like:
            # [Liquipedia](https://liquipedia.net/heroes/Nexus_Cup_\(French_Tournament\))
            # This is a "fix" so it at least doesn't break reddit formatting.
            if url.endswith('\\'):
                url += ')'
            # Event description can be for example "Nexus Cup - semifinal".
            # The " - " would often be at line end on old reddit, so delete it.
            match = {
                'starts_in': event.begin.astimezone(UTC) - now,
                'team1': team1,
                'team2': team2,
                'tournament': event.description.replace(' - ', ' '),
                'url': url
            }
            # Empty ~~~~ could break some reddit formatting.
            for key, value in match.items():
                if not value:
                    match[key] = '-'
            matches.append(match)
        return matches

    def _format_matches(self, matches):
        ret = ''
        for match in matches:
            match['starts_in'] = self._format_timedelta(match['starts_in'])
            ret += self.MATCH_FORMAT_STRING.format(**match)
        return ret

    def _format_timedelta(self, timediff):
        total_five_minutes = round(timediff.total_seconds() / (5 * 60))
        total_minutes = total_five_minutes * 5
        if total_minutes <= 0:
            return 'LIVE'
        days = total_minutes // (24 * 60)
        hours = (total_minutes % (24 * 60)) // 60
        minutes = total_minutes % 60
        ret = []
        if days > 0:
            ret.append('{}d'.format(days))
        if days > 0 or hours > 0:
            ret.append('{}h'.format(hours))
        ret.append('{}m'.format(minutes))
        return ' '.join(ret)


def main():
    print(GoogleCalendar().sidebar_text())


if __name__ == '__main__':
    main()
