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
    # print(auth_string)


# cred_path = os.path.join(os.path.dirname(
#     os.path.realpath(__file__)), "credential.json")
# cred_file = open(cred_path)
# credentials = json.load(cred_file)
# cred_file.close()

# """First, get a new token"""
# refreshToken = RefreshToken(
#     client_id=credentials["GOOGLE_CREDENTIAL"]["installed"]["client_id"],
#     client_secret=credentials["GOOGLE_CREDENTIAL"]["installed"]["client_secret"],
#     refresh_token=credentials["GOOGLE_CREDENTIAL"]["installed"]["refresh_token"])

# someString = GenerateOAuth2String(
#     username=credentials["GOOGLE_CREDENTIAL"]["EMAIL_USERNAME"], access_token=refreshToken['access_token'], base64_encode=False)
