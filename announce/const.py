from collections import namedtuple

email = "pyjaipur.india@gmail.com"
tw = "https://api.twitter.com/1.1"
tw_upload = "https://upload.twitter.com/1.1"
format = "D MMMM YYYY HH:mm:ss Z"
Event = namedtuple(
    "Event", "title start end short description poster add_to_cal call tweet_id"
)
