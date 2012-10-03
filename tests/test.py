from slurpy import Slurpy

def sum(a,b):
    print "caca"
    return a + b

s = Slurpy()
s.register_method(sum)

s.start()
