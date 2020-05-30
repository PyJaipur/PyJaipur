from pathlib import Path
from announce.auth import get_sessions


def announce(event_path, session_cache_path):
    text_path = Path(event_path) / "text.txt"
    with open(text_path, "r") as fl:
        text = fl.read()
    sessions = get_sessions(session_cache_path)
    sessions["twitter"].post("statuses/update.json", json={"status": text})
