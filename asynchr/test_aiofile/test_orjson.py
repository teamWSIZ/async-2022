f = lambda x: x.decode('UTF-8')

print(f(b'abc'))

import orjson

w = {'a': 12, 'b': 10}
s = f(orjson.dumps(w))
print(s)
w_ = orjson.loads(s)
print(w_)
