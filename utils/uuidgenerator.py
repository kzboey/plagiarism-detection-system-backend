import uuid
import random


#uuid generator
def gen_uuid4(size=20):
    _uuid4 = str(uuid.uuid4()).replace('-', '')
    return _uuid4[:size]


def gen_randomid(size=10):
    rnd = random.randint(0, 10**size)
    return rnd