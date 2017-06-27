import logging
import os

import requests

logger = logging.getLogger('slackapi')


class SlackAPI(object):
    """
    Yet Another Slack Client
    """
    url = 'https://slack.com/api/{method}'

    def __init__(self, token=None, auth_test=False, verify=True, lazy=False):
        """
        Instantiation an instance of the Slack API

        Args:
            token: {str} (required) API token, read from SLACK_TOKEN env var
            auth_test: {bool} verify this token
            verify: {bool} verify all API calls return with a True 'ok'
            lazy: {bool} Don't populate properties until called
        """

        try:
            self.token = token if token else os.environ['SLACK_TOKEN']
        except KeyError:
            raise ValueError('If not providing a token, must set SLACK_TOKEN envvar')
        if auth_test:
            response = self.auth_test()
            if not response['ok']:
                raise ValueError('Authentication Failed with response: {}'.format(response))
        self.verify = verify

        # Attributes backing properties

    def _call_api(self, method, params=None):
        """
        Low-level method to call the Slack API.

        Args:
            method: {str} method name to call
            params: {dict} GET parameters
                The token will always be added
        """
        url = self.url.format(method=method)
        if not params:
            params = {'token': self.token}
        else:
            params['token'] = self.token
        logger.debug('Send request to %s', url)
        response = requests.get(url, params=params).json()
        if self.verify:
            if not response['ok']:
                msg = 'For {url} API returned this bad response {response}'
                raise Exception(msg.format(url=url, response=response))
        return response

    # API Methods
    def auth_test(self):
        """
        Call auth.test
        """
        return self._call_api('auth.test')

    def rtm_start(self):
        """
        Call rtm.start
        """
        return self._call_api('rtm.start')
