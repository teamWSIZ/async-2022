add = lambda x, y: x + y
mul = lambda x, y: x * y
div = lambda x, y: x / y
sub = lambda x, y: x - y
pow = lambda x, y: x ** y

ops = {'add': add, 'subtract': sub, 'divide': div}

op = "subtract"
a = 10.
b = 12.

print(ops[op](a, b))
