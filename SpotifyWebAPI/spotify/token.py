# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import requests
import time
import base64
import six

TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTH_URL = 'https://accounts.spotify.com/authorize'


class TokenError(Exception):
    pass


class Token(object):
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._token_info = None

        auth_header = base64.b64encode(
            six.text_type(client_id + ':' + client_secret).encode('ascii')
        )
        self._headers = {
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

    @property
    def token(self):
        now = int(time.time())
        if self._token_info:
            if self._token_info['expires_at'] - now < 60:
                token_info = self._refresh_access_token(
                    self._token_info['refresh_token']
                )
            else:
                return self._token_info['access_token']
        else:
            token_info = self._request_access_token()

        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        self._token_info = token_info
        return self._token_info['access_token']

    def _refresh_access_token(self, refresh_token):
        payload = {
            'refresh_token': refresh_token,
            'grant_type':    'refresh_token'
        }

        response = requests.post(
            TOKEN_URL,
            data=payload,
            headers=self._headers
        )
        if response.status_code != 200:
            return None
        token_info = response.json()
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        if 'refresh_token' not in token_info:
            token_info['refresh_token'] = refresh_token

        return token_info

    def __str__(self):
        return self.token

    def _request_access_token(self, code=None):

        params = {
            'redirect_uri':  self._redirect_uri,
            'response_type': 'code' if code is None else code,
            'grant_type':    'authorization_code'
        }

        response = requests.post(
            AUTH_URL,
            params=params,
            headers=self._headers,
            verify=True
        )
        if response.status_code != 200:
            raise TokenError(response.reason)

        token_info = response.json()
        return token_info
