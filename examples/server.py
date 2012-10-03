from slurpy import Slurpy

def sum(a,b):
    return a + b

s = Slurpy()
s.register_method(sum)

s.start()
