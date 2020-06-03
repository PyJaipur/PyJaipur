import os
import json
import sys
from textwrap import dedent
from shutil import copyfile
import datetime
import calendar
from pathlib import Path
import argparse
from announce.core import announce, new_event

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
    new_event()
