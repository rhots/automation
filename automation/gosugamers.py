from datetime import datetime, timedelta
import os

import requests


class Gosugamers:
    """Gosugamers allows us to access their match ticker API."""

    ENDPOINT_URL = "http://gosugamers.net/api/matches"
    GAME = "heroesofthestorm"

    def __init__(self):
        self.API_KEY = os.environ["GOSUGAMERS_API_KEY"]

    def _get_matches(self):
        params = {"game": "heroesofthestorm", "apiKey": self.API_KEY}
        resp = requests.get(self.ENDPOINT_URL, params=params)
        return resp.json()["matches"]

    def sidebar_text(self):
        matches = self._get_matches()

        if len(matches) == 0:
            return "No Upcoming Matches"

        final_line_items = []
        for match in matches[:5]:
            final_line_items.append(self._format_match(match))
            final_line_items.append("\n[](#matchSpacer)")

        return "\n".join(final_line_items)

    def _format_match(self, match):
        """_format_match formats a match object into a line item in the
        sidebar's match ticker."""

        """
        >>> [~~North America Heroes Global Championship~~
        ~~23h 45m~~
        ~~Tempo Storm HotS~~
        ~~Team Naventic~~]
        (https://goo.gl/zeTeMF)
        """

        name = match["tournament"]["name"]
        url = match["pageUrl"]
        time = match["datetime"]
        is_live = match["isLive"]
        plaintiff = match["firstOpponent"]["name"]
        defendant = match["secondOpponent"]["name"]

        time_left = self._parse_gosu_time(time) - datetime.utcnow()
        if is_live or (time_left < timedelta(minutes=1)):
            time_left = "LIVE"
        else:
            time_left = self._format_time(time_left)

        lines = []
        lines.append(">>> [~~{0}~~".format(name))
        lines.append("~~{0}~~".format(time_left))
        lines.append("~~{0}~~".format(plaintiff))
        lines.append("~~{0}~~]".format(defendant))
        lines.append("({0})".format(url))

        return "\n".join(lines)

    def _parse_gosu_time(self, tstring):
        # Example: 2017-01-20T17:00:00+00:00
        return datetime.strptime(tstring, "%Y-%m-%dT%H:%M:%S+00:00")

    def _format_time(self, delta):
        days = delta.days
        hours = int(delta.seconds // 60) // 60
        minutes = int((delta.seconds - (hours * 60 * 60)) // 60)

        formatted = ''

        if days != 0:
            formatted = formatted + str(days) + 'd '
        if hours != 0:
            formatted = formatted + str(hours) + 'h '
        minutes = self._round_to_five(minutes)

        formatted = formatted + str(minutes) + 'm'

        return formatted

    def _round_to_five(self, x, base=5):
        return int(base * round(float(x)/base))
