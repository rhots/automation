import os

from slackclient import SlackClient

class Slack:
    """Slack allows you to send messages to a specified Slack channel."""

    def __init__(self):
        slack_api_token = os.environ["SLACK_API_TOKEN"]
        self._client = SlackClient(slack_api_token)

    def send_message(self, channel, message):
        self._client.api_call(
                "chat.postMessage",
                channel=channel,
                text=message)
