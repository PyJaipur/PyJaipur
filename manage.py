import yaml
import pendulum
import requests

TZ = "Asia/Kolkata"


def move_old_event_to_logs():
    with open("website/staticsite.yaml", "r") as fl:
        data = yaml.load(fl, Loader=yaml.FullLoader)
    latest = [e for e in data["events"] if e["title"] == "Community call"][0]
    d, m, y, *_ = latest["start"].split()
    if pendulum.from_format(f"{d} {m} {y}", "DD MMMM YYYY") >= pendulum.now():
        print("Latest event is in the future. Skipping")
        return
    m = m[:3]
    github_issue = [b["href"] for b in latest["badges"] if b["text"] == "Github"][0]
    mom = "website/src/.mom_list.html"
    with open(mom, "r") as fl:
        final = []
        done = False
        for line in fl.readlines():
            if "|" in line and not done:
                final.append(
                    f"""      ('{d} {m} {y} | Community call', '{github_issue}'),\n"""
                )
                done = True
            if final and final[-1] == line:
                continue
            final.append(line)
    with open(mom, "w") as fl:
        fl.write("".join(final))
    return github_issue.split("/")[-1]


def close_issue(issue_number, token):
    print("Closing", issue_number)
    r = requests.patch(
        f"https://api.github.com/repos/PyJaipur/PyJaipur/issues/{issue_number}",
        json={"state": "closed",},
        headers={"Authorization": f"token {token}"},
    )
    print("Response: ", r.status_code)


def create_issue(old_issue, token):
    print("Creating new issue")
    date = pendulum.now(TZ)
    date = pendulum.duration(days=7) + date
    with open("website/staticsite.yaml", "r") as fl:
        if date.format("DD MMMM YYYY") in fl.read():
            print("Event already exists")
            return
    date = date.format("DD MMM YYYY")
    title = f"Community call: {date}"
    r = requests.post(
        f"https://api.github.com/repos/PyJaipur/PyJaipur/issues",
        json={
            "title": title,
            "body": f"""## Agenda

- Follow up on #{old_issue}""",
            "labels": ["Event"],
        },
        headers={"Authorization": f"token {token}"},
    )
    print("Created issue: ", r.json()["number"])
    ino = r.json()["number"]
    return ino


def create_new_website_event(issue_num, calendar_link, call_link):
    date = pendulum.duration(days=7) + pendulum.now(TZ)
    date = date.format("DD MMMM YYYY")
    events = "website/staticsite.yaml"
    with open(events, "r") as fl:
        if date in fl.read():
            print("Event date already exists")
            return
    data = {
        "title": "Community call",
        "start": f"{date} 21:00:00 GMT+5:30",
        "desc": "We're having a community call this sunday at 9 pm! Come join the community!",
        "badges": [
            {
                "href": f"https://github.com/PyJaipur/PyJaipur/issues/{issue_num}",
                "text": "Github",
            },
        ],
    }
    if call_link:
        data["badges"].insert(0, {"href": call_link, "text": "Call"})
    if calendar_link:
        data["badges"].insert(
            0, {"href": calendar_link, "text": "Add to calendar"},
        )
    with open(events, "r") as fl:
        d = yaml.load(fl, Loader=yaml.FullLoader)
    d["events"] = [data] + d["events"]
    with open(events, "w") as fl:
        yaml.dump(d, fl)


def new_community_call(token, *_):
    old_gh = move_old_event_to_logs()
    if old_gh is not None:
        close_issue(old_gh, token)
    new_gh = create_issue(old_gh, token)
    # Google requires Oauth2 which means we cannot create these events via
    # github actions
    # create_calendar_event()
    if new_gh is not None:
        create_new_website_event(new_gh, "#", "#")


if __name__ == "__main__":
    import sys

    args = list(sys.argv)
    fn, args = args[1], args[2:]
    exec(f"{fn}(*{args})")
