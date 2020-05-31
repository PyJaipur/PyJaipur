import os
import logging
import json
from collections import namedtuple
from functools import lru_cache
from pathlib import Path
from announce.auth import get_sessions
from announce import const

log = logging.getLogger(__name__)


@lru_cache()
def get_event(event_path):
    Event = namedtuple("Event", "title start short description poster")
    with open(event_path / "meta.json", "r") as fl:
        meta = json.loads(fl.read())
    with open(event_path / "text.txt", "r") as fl:
        text = fl.read()
    if os.path.exists(event_path / "poster.png"):
        poster = open(event_path / "poster.png", "rb")
    elif os.path.exists(event_path / "poster.jpeg"):
        poster = open(event_path / "poster.jpeg", "rb")
    else:
        poster = None
    ev = Event(meta["title"], meta["start"], meta["short"], text, poster)
    return ev


def update_website(event_path):
    event = get_event(event_path)
    with open("website/src/.events.html", "r") as fl:
        html = fl.read()
    if event.start in html:
        return
    mark = "<!-- announce-new-event-after-this -->"
    idx = html.find(mark) + len(mark)
    ev_html = f"""

  <div class='alert'>
    <strong>{event.title}</strong><br>
    <time>{event.start}</time><br>
    <a class='badge' target="_blank" href="#">Add to calendar</a><br>
    <a class='badge' href='#'>Call</a>
    <hr>
    {event.short}
  </div>

    """
    with open("website/src/.events.html", "w") as fl:
        fl.write(html[:idx] + ev_html + html[idx:])
    log.info("Site updated")


def announce(event_path, session_cache_path):
    """
    Provide a path to the event folder. This is usually some path like `events/2020/5/21`.
    Session cache path is where the session cache is stored.
    """
    update_website(event_path)
    event = get_event(event_path)
    sessions = get_sessions(session_cache_path)
    # Twitter
    data = {"status": event.short, "enable_dmcommands": True}
    if event.poster is not None:
        r = sessions["twitter"].post(
            f"{const.tw_upload}/media/upload.json", files={"media": event.poster}
        )
        if r.status_code == 200:
            log.info(r.json())
            mid = r.json().get("media_id_string")
            data["media_ids"] = mid
    sessions["twitter"].post(f"{const.tw}/statuses/update.json", data=data)
    log.info("Tweet done")
