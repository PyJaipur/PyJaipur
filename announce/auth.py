import os
import pickle
import requests
import logging
from requests_oauthlib import OAuth1Session
from announce import const

log = logging.getLogger(__name__)


def refresh_twitter(sessions):
    request_token_url = "https://api.twitter.com/oauth/request_token"
    access_token_url = "https://api.twitter.com/oauth/access_token"
    authorize_url = "https://api.twitter.com/oauth/authorize"
    base_url = const.tw
    session = sessions.get("twitter")
    try:
        params = {"include_rts": 1, "count": 10}
        r = session.get(f"{base_url}/statuses/home_timeline.json", params=params)
        log.info("Found cached twitter credentials")
    except Exception:
        log.info("Refreshing twitter auth")
        client_key = os.environ.get("TWITTER_CONSUMER_KEY")
        client_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        oauth = OAuth1Session(client_key=client_key, client_secret=client_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        authorization_url = oauth.authorization_url(authorize_url)
        log.info("Please visit this url: ", authorization_url)
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
    refresh_twitter(sessions)
    # ----------------------------
    with open(path / "sessions.pickle", "wb") as fl:
        pickle.dump(sessions, fl)
    return sessions
