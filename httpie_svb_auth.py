"""
SVB API auth plugin for HTTPie.

http://docs.svbplatform.com/
Copyright (c) 2017 Silicon Valley Bank
"""
import hashlib
import hmac
import httpie.plugins
import time

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class SVBAuth:

    def __init__(self, api_key, hmac_secret):
        self.api_key = str(api_key)
        self.hmac_secret = str(hmac_secret)

    def __call__(self, r):
        timestamp = str(int(time.time()))
        url = urlparse(r.url)

        if r.headers.get('Content-Type', '').startswith('application/json'):
            body = r.body
        else:
            body = ''

        str_to_sign = '\n'.join([timestamp,
                                 r.method.upper(),
                                 url.path,
                                 url.query,
                                 body])
        signature = hmac.new(self.hmac_secret, str_to_sign, hashlib.sha256) \
                        .digest() \
                        .encode('hex')

        r.headers['Authorization'] = 'Bearer ' + self.api_key
        r.headers['X-Signature'] = signature
        r.headers['X-Timestamp'] = timestamp
        return r


class SVBAuthPlugin(httpie.plugins.AuthPlugin):

    name = 'SVB API auth'
    description = 'Sign requests as required by the SVB API'
    auth_type = 'svb'

    def get_auth(self, username=None, password=None):
        return SVBAuth(username, password)
