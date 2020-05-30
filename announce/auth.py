import os
import pickle
import requests
from requests_oauthlib import OAuth1Session, OAuth1


def refresh_twitter(sessions):
    session = sessions.get("twitter")
    request_token_url="https://api.twitter.com/oauth/request_token"
    access_token_url="https://api.twitter.com/oauth/access_token"
    authorize_url="https://api.twitter.com/oauth/authorize"
    base_url="https://api.twitter.com/1.1/"
    try:
        params = {"include_rts": 1, "count": 10}
        r = session.get("statuses/home_timeline.json", params=params)
    except Exception:
        twitter = OAuth1Session(
            client_key=os.environ.get("TWITTER_CONSUMER_KEY"),
            client_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
        )
        fetch_response = twitter.fetch_request_token(request_token_url)
        {
        oauth = OAuth1(client_key, client_secret=client_secret)

        request_token, request_token_secret = twitter.get_request_token()
        authorize_url = twitter.get_authorize_url(request_token)
        print(authorize_url)
        pin = input("Enter pin: ")
        session = twitter.get_auth_session(
            request_token,
            request_token_secret,
            method="POST",
            data={"oauth_verifier": pin},
        )
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
