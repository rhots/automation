import os
import random

from twitch import TwitchClient

class Twitch:
    """Twitch enables interaction with the twitch.tv API to get info on
    Heroes of the Storm streams."""

    def __init__(self):
        self._client = TwitchClient(client_id=os.environ["TWITCH_CLIENT_ID"])

    # TODO: doesn't use pagination, limited to 100 streams by twitch
    def _get_streams(self):
        return self._client.streams.get_live_streams(
            game="Heroes of the Storm", limit=100)

    def _format_stream(self, stream):
        """Takes a stream dict as found in API responses and formats it
        for the sidebar."""

        display_name = stream["channel"]["display_name"].strip()
        status = stream["channel"]["status"].strip()
        viewers = str(stream["viewers"])
        url = stream["channel"]["url"]

        return "* [{0} ~~{1}~~ ^{2}]({3})\n\n".format(
                display_name,
                status,
                viewers,
                url)

    # TODO: omg get this outta here
    def sidebar_text(self):
        streams = self._get_streams()

        # Choose top five streams
        top_streams_formatted = [self._format_stream(s) for s in streams[:5]]
        top_streams_text = "".join(top_streams_formatted)

        # Choose five randomly chosen streams
        random_streams = random.sample(streams[5:], 5)
        random_streams_formatted = [self._format_stream(s) for s in random_streams]
        random_streams_text = "".join(random_streams_formatted)

        return "Top\n\n{0}\nDiscover\n\n{1}".format(
                top_streams_text,
                random_streams_text)
