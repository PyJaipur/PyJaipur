import os
from pathlib import Path
import argparse
from announce.core import announce

parser = argparse.ArgumentParser()
parser.add_argument("event_path")
parser.add_argument("--secret", default=".secret")

args = parser.parse_args()
if not os.path.exists(args.secret):
    os.mkdir(args.secret)
announce(Path(args.event_path), Path(args.secret))
