from announce import const


def run(session, event):
    if event.tweet_id is not None:
        return event
    data = {"status": event.short, "enable_dmcommands": True}
    if event.poster is not None:
        r = session.post(
            f"{const.tw_upload}/media/upload.json", files={"media": event.poster}
        )
        if r.status_code == 200:
            mid = r.json().get("media_id_string")
            data["media_ids"] = mid
    tweet = session.post(f"{const.tw}/statuses/update.json", data=data)
    return const.Event(**{**event._asdict(), "tweet_id": tweet.json()["id"]})
