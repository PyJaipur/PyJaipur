import pendulum


def in_future(date, force=None):
    now = pendulum.now("Asia/Kolkata")
    print(force, date, now)
    if force is not None:
        return force
    pre = date[:-9]
    start = pendulum.from_format(pre, "DD MMMM YYYY HH:mm:ss", tz="Asia/Kolkata")
    return start > now
