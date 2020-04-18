def stream_file(*args, chunksize=512, **kwargs):
    with open(*args, **kwargs) as fl:
        yield fl.read(chunksize)


def dbrunner(url):
    db = connect(url)

    def runner(sql, args):
        with db.connect() as conn:
            rows = conn.execute(sql, args)
            yield from rows

    return runner
