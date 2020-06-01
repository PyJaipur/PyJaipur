import string
import json
import random
import pendulum
import pickle
import os.path
from urllib.parse import urlparse, parse_qs, urlencode
from announce import const


def run(session, event):
    if event.add_to_cal is not None:
        return event
    service = session
    body = {
        "summary": event.title,
        "description": event.short,
        "visibility": "public",
        "start": {
            "dateTime": event.start.to_iso8601_string(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {"dateTime": event.end.to_iso8601_string(), "timeZone": "Asia/Kolkata",},
    }

    calevent = service.events().insert(calendarId="primary", body=body).execute()
    link = calevent.get("htmlLink")
    add_to_cal = "https://calendar.google.com/event?" + urlencode(
        {
            "action": "TEMPLATE",
            "tmeid": parse_qs(urlparse(link).query)["eid"][0],
            "tmsrc": const.email,
            "scp": "ALL",
        }
    )
    conf = (
        service.events()
        .patch(
            calendarId="primary",
            eventId=calevent.get("id"),
            body={
                "conferenceData": {
                    "createRequest": {
                        "requestId": f"pyj-{''.join(random.sample(string.ascii_lowercase, 10))}"
                    }
                }
            },
            sendNotifications=True,
            conferenceDataVersion=1,
        )
        .execute()
    )
    call_link = conf.get("hangoutLink")
    return const.Event(
        **{**event._asdict(), "add_to_cal": add_to_cal, "call": call_link}
    )
