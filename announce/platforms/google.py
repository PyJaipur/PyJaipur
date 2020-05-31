from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

log = logging.getLogger()


def main(secret):
    creds = None
    if os.path.exists(secret / "googletoken.pickle"):
        with open(secret / "googletoken.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secrets / "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(secrets / "token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": event.title,
        "description": event.short,
        "start": {"dateTime": event.start, "timeZone": "Asia/Kolkata",},
        "end": {"dateTime": event.end, "timeZone": "Asia/Kolkata",},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    log.info("Calendar created: %s", event.get("htmlLink"))


if __name__ == "__main__":
    main()
