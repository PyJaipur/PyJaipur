#!/usr/bin/python

import os
import pickle
import json
from urllib.request import urlopen
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# scrape youtube video ids from the channel id specified in the url
url = 'https://www.googleapis.com/youtube/v3/search?key={your_api_key}&channelId=UCLgQwtSa4EsuJge-N8Bjs3g&part=snippet,id&order=date&maxResults=20'
data = urlopen(url).read()
info = json.loads(data)
vidId=[]
for i in range(len(info['items'])):
    vidId.append(info['items'][i]['id'].get('videoId'))

CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

RATINGS = ('like', 'dislike', 'none')

# Authorize the request and store authorization credentials.
def get_authenticated_service():
  credentials = None
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          credentials = pickle.load(token)
  #  Check if the credentials are invalid or do not exist
  if not credentials or not credentials.valid:
      # Check if the credentials have expired
      if credentials and credentials.expired and credentials.refresh_token:
          credentials.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              CLIENT_SECRETS_FILE, SCOPES)
          credentials = flow.run_console()

      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(credentials, token)
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# Add the video rating. This code sets the rating to 'like,' but you could
# change the value of rating to 'like' and 'dislike.'
def like_video(youtube, vId):
  youtube.videos().rate(
    id=vId,
    rating='like'
  ).execute()

if __name__ == '__main__':
  for i in range(len(vidId)):
    youtube = get_authenticated_service()
    try:
      like_video(youtube, vidId[i])
    except HttpError:
      print ('An HTTP error %d occurred:\n%s' % (HttpError.resp.status, HttpError.content))
    else:
      print ('The like rating has been added for video ID %s.' % (vidId[i]))
