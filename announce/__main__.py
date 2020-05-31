import os
import json
import sys
from textwrap import dedent
from shutil import copyfile
import datetime
import calendar
from pathlib import Path
import argparse
from announce.core import announce

parser = argparse.ArgumentParser()
parser.add_argument("--event", default=None, help="What event are we talking about?")
parser.add_argument(
    "--announce", default=False, action="store_true", help="Should we announce?"
)
parser.add_argument("--secret", default=".secret", help="Where to cache credentials?")
parser.add_argument(
    "--new", default=False, action="store_true", help="Create a new event"
)

args = parser.parse_args()
if not os.path.exists(args.secret):
    os.mkdir(args.secret)
if args.announce:
    if args.event is None:
        print("Please specify --event")
        sys.exit(0)
    announce(Path(args.event), Path(args.secret))
elif args.new:
    this_year = str(datetime.datetime.now().year)
    this_month = str(datetime.datetime.now().month)
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
    start = f"{date} {calendar.month_name[int(month)]} {year} {start} GMT+5:30"
    default_short = "TBD"
    short = input(f"Short description ({default_short}):")
    short = short if short else default_short
    root = Path(".") / "events" / year / month / date
    with open(root / "meta.json", "w") as fl:
        fl.write(json.dumps({"title": title, "start": start, "short": short}))
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
