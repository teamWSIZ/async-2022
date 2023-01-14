import json
from datetime import datetime

d = dict()
print(d)
d['xx'] = 'just do it'

e = {}

e['abc'] = 11
e['gg'] = 123**123
e['dd'] = d
print(e)
print(type(e))  # chcemy "str"

sss = json.dumps(e)
print(sss)
print(type(sss))


dd = json.loads(sss)
print(dd)
print(type(dd))
