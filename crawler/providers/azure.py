import datetime
import json
import logging
import requests
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from crawler.providers.base_provider import BaseProvider
from secret import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID

logger = logging.getLogger('contrail.crawler.azure')

URL_TOKEN_REQUEST = 'https://login.microsoftonline.com/{tenant}/oauth2/token'
"""
URL queried to obtain an Azure management access token. Replaces {tenant} with a tenant (directory) ID.
"""

URL_RATECARD_REQUEST = "https://management.azure.com:443/subscriptions/{subscriptionId}/providers/" \
                       "Microsoft.Commerce/RateCard?api-version=2016-08-31-preview&$filter=" \
                       "OfferDurableId eq 'MS-AZR-0003P' and Currency eq 'USD' " \
                       "and Locale eq 'en-US' and RegionInfo eq 'US'"
"""
URL queried to list prices. Replaces {subscriptionId}.
"""


class Azure(BaseProvider):
    def __init__(self):
        super().__init__()
        self._access_token = ''
        self._access_token_expire = 0

    def crawl(self) -> datetime.timedelta:
        ratecard = self.request_ratecard()

        self.upload_provider_data(region='US', data=ratecard)

        return datetime.timedelta(minutes=60)

    def request_ratecard(self):
        # post_data = {
        #     'Authorization': 'Bearer {}'.format(self.access_token())
        # }
        url = URL_RATECARD_REQUEST.format(subscriptionId=AZURE_SUBSCRIPTION_ID)
        response = requests.get(url, allow_redirects=False,
                                headers={'Authorization': 'Bearer {}'.format(self.access_token())})

        # Initial request forces a redirect. Look at response headers to get the redirect URL
        redirect_url = response.headers['Location']

        # Get the ratecard content by making another call to go the redirect URL
        rate_card = requests.get(redirect_url)

        # Print the ratecard content
        return json.loads(rate_card.content)

    def _renew_access_token(self):
        """
        Retrieve an access token needed to pull pricing data.
        :return: The access token.
        """
        logger.info("Renewing access token.")

        post_data = {
            'client_id': AZURE_CLIENT_ID,
            'grant_type': 'client_credentials',
            'client_secret': AZURE_CLIENT_SECRET,
            'resource': 'https://management.azure.com/'
        }

        request = Request(URL_TOKEN_REQUEST.format(tenant=AZURE_TENANT_ID), urlencode(post_data).encode())
        response = urlopen(request).read().decode()
        resp_json = json.loads(response)

        self._access_token = resp_json['access_token']
        self._access_token_expire = int(resp_json['expires_on'])

    def access_token(self):
        # Renew access token 1 minute before the current one expires
        if self._access_token_expire < time.time() + 60:
            self._renew_access_token()

        return self._access_token