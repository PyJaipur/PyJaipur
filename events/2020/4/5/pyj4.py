import math


class IsPrime:
    known_primes = {2, 3}

    @staticmethod
    def check(n):
        if n < 2:
            return False
        if n in IsPrime.known_primes:
            return True
        for d in range(2, math.ceil(math.sqrt(n)) + 1):
            if n % d == 0:
                return False
        IsPrime.known_primes.add(n)
        return True


for n in range(20):
    if IsPrime.check(n):
        print(n)


known_primes = {2, 3}


def is_prime(n):
    global known_primes
    if n < 2:
        return False
    if n in known_primes:
        return True
    for d in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % d == 0:
            return False
    known_primes.add(n)
    return True


for n in range(20):
    if is_prime(n):
        print(n)


def primes(seq):
    known_primes = {2, 3}
    for n in seq:
        if n < 2:
            continue
        if n in known_primes:
            yield n
        for d in range(2, math.ceil(math.sqrt(n)) + 1):
            if n % d == 0:
                break
        else:
            known_primes.add(n)
            yield n


for i in primes(range(20)):
    print(i)
