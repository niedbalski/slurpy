Slurpy
======

Slurpy is an RPC mechanism to call python methods from javascript and viceversa.

Installation
------------

Install the package using pip

    $ pip install slurpy

Usage
----

* Create a new Slurpy server instance, in this case, we are gonna
call the "js_sum" method from python

```python
import slurpy

def sum(a,b):
    slurpy.javascript.js_sum(1, 2, callback=on_js_sum_response)
    return a + b

def on_js_sum_response(value):
    print "The js_sum return =  %d" % value

s = slurpy.Slurpy()
s.register_method(sum)

s.start()

```

* Then integrate on your HTML document , defining the function to be called
by the server.

```javascript
<html>
    <head>
       <script type="text/javascript" src="http://localhost:51711/slurpy/js"></script>
       <script type="text/javascript">

            //invoked by the python code
            var js_sum = function(a, b) {
                return a + b;
            }

            python.on('loaded', function(evt) {
                python.sum(10, 1000, function(response) {
                    alert(response);    
                });
            });

        </script>
    </head>
    <body>
    </body>
</html>
```

* Start the server

$ python your_slurpy_server.py

