def run_sync():
    with crawler_db.connect() as cdb, postgres.connect() as pgdb:
        for row in crawler_db.execute("select * from some table"):
            for row in pgdb.execute(
                "select * from some table where c_id < %s", (row.id,)
            ):
                with client_db.begin() as client:
                    client.execute("insert into some table")


def run_sync():
    for row in crawler_db("select * from some table"):
        for row in pgdb("select * from some table where c_id < %s", (row.id,)):
            list(client("insert into some table"))


def submissions(qcode):
    # api calls
    yield requests.text


for submission in submissions(qcode):
    pass
