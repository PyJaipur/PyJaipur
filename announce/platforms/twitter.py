from announce import const
import logging

log = logging.getLogger()


def run(session, event):
    data = {"status": event.short, "enable_dmcommands": True}
    if event.poster is not None:
        r = session.post(
            f"{const.tw_upload}/media/upload.json", files={"media": event.poster}
        )
        if r.status_code == 200:
            log.info(r.json())
            mid = r.json().get("media_id_string")
            data["media_ids"] = mid
    session.post(f"{const.tw}/statuses/update.json", data=data)
    log.info("Tweet done")
