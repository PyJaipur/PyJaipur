def count(start=1):
    while True:
        yield start
        start += 1


def stream(*a, seek=0, chunksize=512, **kwargs):
    with open(*a, **kwargs) as fl:
        fl.seek(seek)
        while True:
            chunk = fl.read(chunksize)
            if not chunk:
                break
            yield chunk


def take(n, seq):
    for i, x in enumerate(seq):
        if i >= n:
            break
        yield x


def lines(seq):
    accumulator = ""
    for chunk in seq:
        accumulator += chunk
        while "\n" in accumulator:
            line, accumulator = accumulator.split("\n", 1)
            yield line


for i in take(10, lines(stream("pyj1.py", "r", chunksize=5))):
    print(i)


def lines():
    def fn(seq):
        accumulator = ""
        for chunk in seq:
            accumulator += chunk
            while "\n" in accumulator:
                line, accumulator = accumulator.split("\n", 1)
                yield line

    return fn


def take(n):
    def fn(seq):
        for i, x in enumerate(seq):
            if i >= n:
                break
            yield x

    return fn


def stream(*a, seek=0, chunksize=512, **kwargs):
    def fn():
        with open(*a, **kwargs) as fl:
            fl.seek(seek)
            while True:
                chunk = fl.read(chunksize)
                if not chunk:
                    break
                yield chunk

    return fn


for i in take(10)(lines()(stream("pyj1.py", "r", chunksize=5)())):
    print(i)


def nest(*a):
    first, *leftover = a
    if not leftover:
        yield from first()
    else:
        for i in first(nest(*leftover)):
            yield i


log_html = "".join(
    i
    for i in nest(
        take(10),
        turn_to_html_tables(),
        read_like_nginx_logs(),
        lines(),
        stream("nginx5.5gfile", "r", chunksize=512),
    )
)
