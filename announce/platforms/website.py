def run(session, event):
    with open("website/src/.events.html", "r") as fl:
        html = fl.read()
    start = event.start.format("DD MMMM YYYY HH:mm:ss") + " GMT+5:30"
    if start in html:
        return event
    mark = "<!-- announce-new-event-after-this -->"
    idx = html.find(mark) + len(mark)
    ev_html = f"""

  <div class='alert'>
    <strong>{event.title}</strong><br>
    <time>{start}</time><br>
    <a class='badge' target="_blank" href="{event.add_to_cal}">Add to calendar</a><br>
    <a class='badge' href='{event.call}'>Call</a>
    <hr>
    {event.short}
  </div>

    """
    with open("website/src/.events.html", "w") as fl:
        fl.write(html[:idx] + ev_html + html[idx:])
    log.info("Site updated")
    return event
