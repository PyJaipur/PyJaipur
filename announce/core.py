import os
import calendar
from textwrap import dedent
import pendulum
import json
from functools import lru_cache
from pathlib import Path
from announce.auth import get_sessions
from announce.platforms import twitter, google, website, mailinglist, linkedin
from announce import const


@lru_cache()
def get_event(event_path):
    with open(event_path / "meta.json", "r") as fl:
        meta = json.loads(fl.read())
    with open(event_path / "text.txt", "r") as fl:
        text = fl.read()
    poster = None
    if os.path.exists(event_path / "poster.png"):
        poster = open(event_path / "poster.png", "rb")
    elif os.path.exists(event_path / "poster.jpeg"):
        poster = open(event_path / "poster.jpeg", "rb")
    ev = const.Event(
        meta["title"],
        pendulum.parse(meta["start"]),
        pendulum.parse(meta["end"]),
        meta["short"],
        text,
        poster,
        meta.get("add_to_cal"),
        meta.get("call"),
        meta.get("tweet_id"),
        meta.get("email_sent"),
        meta.get("linkedin_id"),
    )
    return ev


def update_event(event_path, event):
    with open(event_path / "meta.json", "w") as fl:
        ev = dict(event._asdict())
        ev["start"] = ev["start"].to_iso8601_string()
        ev["end"] = ev["end"].to_iso8601_string()
        ev.pop("poster")
        fl.write(json.dumps(ev, indent=2))
    with open(event_path / "text.txt", "w") as fl:
        fl.write(event.description)


def new_event():
    this_year = str(pendulum.now().year)
    this_month = str(pendulum.now().month)
    year = input(f"Year ({this_year}):")
    year = year.strip() if year.strip() else this_year
    month = input(f"Month ({this_month}):")
    month = month.strip() if month.strip() else this_month
    date = input("Date: ").strip()
    os.makedirs(Path(".") / "events" / year / month / date, exist_ok=True)
    # ------------------
    default_title = f"{calendar.month_name[int(month)]} meetup"
    title = input(f"Event title ({default_title}):")
    title = title if title else default_title
    default_start = "11:00:00"
    start = input(f"Start time ({default_start}):")
    start = start if start else default_start
    start = pendulum.datetime(
        int(year),
        int(month),
        int(date),
        int(start.split(":")[0]),
        int(start.split(":")[1]),
        int(start.split(":")[2]),
        tz="Asia/Kolkata",
    )
    default_end = "12:00:00"
    end = input(f"End time ({default_end}):")
    end = end if end else default_end
    end = pendulum.datetime(
        int(year),
        int(month),
        int(date),
        int(end.split(":")[0]),
        int(end.split(":")[1]),
        int(end.split(":")[2]),
        tz="Asia/Kolkata",
    )
    default_short = "TBD"
    short = input(f"Short description ({default_short}):")
    short = short if short else default_short
    root = Path(".") / "events" / year / month / date
    with open(root / "meta.json", "w") as fl:
        fl.write(
            json.dumps(
                {
                    "title": title,
                    "start": start.to_iso8601_string(),
                    "short": short,
                    "end": end.to_iso8601_string(),
                }
            )
        )
    with open(root / "text.txt", "w") as fl:
        fl.write(
            dedent(
                """\
        Please use pyjaipur.org/#call to join the call.
        #pyjaipur #event
        """
            )
        )
    print(f"Created {root/'text.txt'} for description. Please fill it up")
    poster = input(f"Copy monthly meetup poster as poster for this event? (Y/n)")
    if poster.strip().lower() in ("", "y"):
        os.symlink(
            Path(".")
            / "website"
            / "src"
            / "images"
            / "assets"
            / "monthly_meetup_thumbnail.jpeg",
            root / "poster.jpeg",
        )
        print("Created symlink to monthly meetup poster for this event")
    print("To announce this event please use:")
    print(f"     python -m announce --event events/{year}/{month}/{date} --announce")


def announce(event_path, session_cache_path):
    """
    Provide a path to the event folder. This is usually some path like `events/2020/5/21`.
    Session cache path is where the session cache is stored.
    """
    event = get_event(event_path)
    sessions = get_sessions(session_cache_path)
    # TODO(thesage21): linkedin app permissions need approval
    # event = linkedin.run(sessions.get("linkedin"), event)
    event = google.run(sessions["google"], event)
    event = twitter.run(sessions["twitter"], event)
    event = mailinglist.run(sessions.get("mailinglist"), event)
    event = website.run(sessions.get("website"), event)
    update_event(event_path, event)
