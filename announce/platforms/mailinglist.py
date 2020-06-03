import os
import smtplib
from textwrap import dedent
import json
from announce import const


def send(*, to, subject, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(const.email, os.environ.get("GMAIL_PWD"))

    body = "\r\n".join(
        [
            "To: %s" % to,
            "From: PyJaipur <%s>" % const.email,
            "Subject: %s" % subject,
            "",
            message,
        ]
    )
    try:
        server.sendmail(const.email, [to], body)
    except Exception as e:
        log.exception(e)
    server.quit()


def run(session, event):
    message = f"Hello,\n\n{event.description}\n\nThanks,\nPyJaipur"
    send(to=const.mailing_list_email, subject=event.title, message=message)
    return const.Event(**{**(event._asdict()), "email_sent": True})
