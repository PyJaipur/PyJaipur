## Logging
def log(function):
    def new_function(*args, **kwargs):
        print("Beginning", function, args, kwargs)
        rval = function(*args, **kwargs)
        print("Ended", function, rval)
        return rval

    return new_function


@log
def median(array):
    array.sort()
    l = len(array)
    mid = l // 2 if l % 2 == 0 else (l + 1) // 2
    return array[mid]


# median([1, 2, 3, 4, 5, 6])

## Caching


def cache(function):
    notebook = {}

    def new_function(x):
        if x not in notebook:
            notebook[x] = function(x)
        return notebook[x]

    return new_function


@log
@cache
def fibo(n):
    if n < 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)


# fibo(50)

## Registry

lookup = {}


def use_for(ctype):
    lookup[ctype] = function
    return function


@use_for("html")
def html_fn():
    pass


@use_for("pdf")
def pdf_fn():
    pass


ctype = "pdf"
fn = lookup[ctype]
fn()

## Rate limits/locks

from threading import Lock, Thread


def using(lock):
    def decorator(function):
        def new_function(*a, **kwargs):
            with lock:
                return function(*a, **kwargs)

        return new_function

    return decorator


common_value = 0
addition_lock = Lock()


@using(addition_lock)
def counter(n):
    global common_value
    for _ in range(10):
        print(common_value, end=f"--+{n}-->")
        common_value += n
        print(common_value)


# t1, t2, t3 = [Thread(target=counter, args=(i,)) for i in range(1, 4)]
# t1.start(), t2.start(), t3.start()
