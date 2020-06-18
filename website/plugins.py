import pendulum


def in_future(date):
    pre = date[:-9]
    start = pendulum.from_format(pre, "DD MMMM YYYY HH:mm:ss", tz="Asia/Kolkata")
    now = pendulum.now()
    return start > now
