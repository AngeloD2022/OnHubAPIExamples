import requests
import json

def getRefreshToken():
    file = open("config.json", "r")
    rt = json.loads(file.read())
    rt = rt["refreshToken"]
    return rt


def getAPIToken(refresh):
    # Authentication step 1 as described in documentation...
    url = "https://www.googleapis.com/oauth2/v4/token"

    payload = f'client_id=936475272427.apps.googleusercontent.com&grant_type=refresh_token&refresh_token={refresh}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Take access token from step 1 and use in step 2...
    accessToken = response.json()["access_token"]

    url = "https://oauthaccountmanager.googleapis.com/v1/issuetoken"
    payload = 'app_id=com.google.OnHub&client_id=586698244315-vc96jg3mn4nap78iir799fc2ll3rk18s.apps.googleusercontent.com&hl=en-US&lib_ver=3.3&response_type=token&scope=https%3A//www.googleapis.com/auth/accesspoints%20https%3A//www.googleapis.com/auth/clouddevices'
    headers = {
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Get token for use in API requests...
    apiToken = response.json()["token"]

    return apiToken
