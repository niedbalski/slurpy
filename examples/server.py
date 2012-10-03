import slurpy

def sum(a,b):
    slurpy.javascript.js_sum(1, 2, callback=on_js_sum_response)
    return a + b

def on_js_sum_response(value):
    print "The js_sum return =  %d" % value

s = slurpy.Slurpy()
s.register_method(sum)

s.start()
