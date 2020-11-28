#! Python3
# HTMLtoYouTubePlaylist.py
# 

"""

GET VIDEO URLS FROM HTML FILE

"""

import re
from bs4 import BeautifulSoup

FILE = "/Users/jasonflorentino/Desktop/Ad Campaign Boot Camp.html"
contents = open(FILE, 'r').read()
soup = BeautifulSoup(contents, 'html.parser')

fullURLS = []
for link in soup.find_all('a'):
    fullURLS.append(link.get('href'))

del fullURLS[0:2]

regFilter = r"(https:\/\/www\.youtube\.com\/watch\?v.{16})"
youtubeLinks = []
otherSources = []
for i, url in enumerate(fullURLS):
    match = re.search(regFilter, url)
    if match:
        youtubeLinks.append(match.group(0).replace("https://www.youtube.com/watch?v%253D", "", 1))
    else:
        otherSources.append(url.replace("https://www.google.com/url?q=https://www.google.com/url?q%3D", "", 1))

"""

ADD VIDEOS TO YOUTUBE PLAYLIST

"""

from Google import Create_Service

CLIENT_SECRET = 'client_secret_file.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

service = Create_Service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)

playlistId = "PL9XjG2AG6D2rLaS4pTBPYFZQX1Omfnvsc"

for url in youtubeLinks:
    try:
        request_body = {
            'snippet': {
                'playlistId': playlistId,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': url
                }
            }
        }

        response = service.playlistItems().insert(
                part='snippet',
                body=request_body
                ).execute()
    except:
        continue


