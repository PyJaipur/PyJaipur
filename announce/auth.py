import os
import pickle
from rauth import OAuth1Service


def refresh_twitter(sessions):
    session = sessions.get("twitter")
    try:
        params = {"include_rts": 1, "count": 10}
        r = session.get("statuses/home_timeline.json", params=params)
    except Exception:
        twitter = OAuth1Service(
            name="twitter",
            consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
            consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
            request_token_url="https://api.twitter.com/oauth/request_token",
            access_token_url="https://api.twitter.com/oauth/access_token",
            authorize_url="https://api.twitter.com/oauth/authorize",
            base_url="https://api.twitter.com/1.1/",
        )
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


def get_sessions(path=".secret/auth.pickle"):
    sessions = {}
    if os.path.exists(path):
        with open(path, "rb") as fl:
            sessions = pickle.load(fl)
    refresh_twitter(sessions)
    # ----------------------------
    with open(path, "wb") as fl:
        sessions = pickle.dump(fl)
    return sessions
