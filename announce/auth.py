import os
import pickle
import requests
from requests_oauthlib import OAuth1Session
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs, urlencode
from announce import const


def refresh_linkedin(sessions, path):
    API_KEY = os.environ.get("LINKEDIN_CLIENT_ID")
    API_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
    RETURN_URL = "http://localhost:9126/code"
    session = sessions.get("linkedin")
    url = "https://www.linkedin.com/oauth/v2/authorization/?" + urlencode(
        {
            "response_type": "code",
            "client_id": API_KEY,
            "redirect_uri": RETURN_URL,
            "scope": "w_member_social",
        }
    )
    print("Visit this url:", url)
    q = input("Enter redirected url: ")
    code = parse_qs(urlparse(ru).query).get("code")[0]
    r = requests.get(
        "https://www.linkedin.com/oauth/v2/accessToken",
        params={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": RETURN_URL,
            "client_it": API_KEY,
            "client_secret": API_SECRET,
        },
    )
    access_token = r.json().get("access_token")
    sessions["linkedin"] = {"access_token": access_token, "code": code}


def refresh_google(sessions, path):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    if os.path.exists(path / "googletoken.pickle"):
        with open(path / "googletoken.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path / "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path / "googletoken.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("calendar", "v3", credentials=creds)
    sessions["google"] = service


def refresh_twitter(sessions, path):
    request_token_url = "https://api.twitter.com/oauth/request_token"
    access_token_url = "https://api.twitter.com/oauth/access_token"
    authorize_url = "https://api.twitter.com/oauth/authorize"
    base_url = const.tw
    session = sessions.get("twitter")
    try:
        params = {"include_rts": 1, "count": 10}
        r = session.get(f"{base_url}/statuses/home_timeline.json", params=params)
        print("Found cached twitter credentials")
    except Exception:
        print("Refreshing twitter auth")
        client_key = os.environ.get("TWITTER_CONSUMER_KEY")
        client_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        oauth = OAuth1Session(client_key=client_key, client_secret=client_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        authorization_url = oauth.authorization_url(authorize_url)
        print("Please visit this url: %s", authorization_url)
        verifier = input("Enter pin: ")
        oauth = OAuth1Session(
            client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        session = oauth
        params = {"include_rts": 1, "count": 10}
        r = session.get(f"{base_url}/statuses/home_timeline.json", params=params)

    sessions["twitter"] = session


def get_sessions(path):
    sessions = {}
    if os.path.exists(path / "sessions.pickle"):
        with open(path / "sessions.pickle", "rb") as fl:
            sessions = pickle.load(fl)
    # TODO(thesage21): linkedin app permissions need approval
    # refresh_linkedin(sessions, path)
    refresh_twitter(sessions, path)
    refresh_google(sessions, path)
    # ----------------------------
    with open(path / "sessions.pickle", "wb") as fl:
        pickle.dump(sessions, fl)
    return sessions
