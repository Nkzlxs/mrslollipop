# import urllib.request
# import urllib.parse
import json
import os
import requests
import base64


def RefreshToken(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    # print(params)
    request_url = "https://accounts.google.com/o/oauth2/token"

    response = requests.post(url=request_url, data=params)
    return response.json()


def GenerateOAuth2String(username, access_token, base64_encode=True):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if base64_encode:
        auth_string = base64.b64encode(auth_string)
    return auth_string