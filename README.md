Slurpy
======

Slurpy is an RPC mechanism to call python methods from javascript and viceversa.

Installation
------------

Install the package using pip

    $ pip install slurpy

Usage
----

* Create a new Slurpy server instance. 
 With slurpy you can call javascript methods from the python function
 using the slurpy.javascript object and using the python object from the
javascript side.

```python

import slurpy
import os

def sum(a,b):
    // is possible to call a javascript method and pass a python 
    // callback on result
    slurpy.javascript.js_sum(1, 2, callback=on_js_sum_response)
    return a + b

def on_js_sum_response(value):
    print "The js_sum return =  %d" % value

s = slurpy.Slurpy()

s.register(os)
s.register(sum)

s.run()
```

* Then integrate on your HTML document , defining the function to be called
by the server.
```javascript
<html>
    <head>
       <script type="text/javascript" src="http://localhost:51711/slurpy/js"></script>
       <script type="text/javascript">

            //method invoked by the python code
            var js_sum = function(a, b) {
                return a + b;
            }

            //wait for loaded event
            python.on('loaded', function(evt) {
                    
                python.dirname('/etc/passwd', function(response) {
                    console.log("Directory name" + response);
                });

                //module invoke
                python.os.getenv("HOME", function(response) {
                    console.log("Home variable " + response);
                });

                //module invoke
                python.os.getuid(function(uid) {
                    console.log("Current UID " + uid);
                });
        
                //direct method invoke
                python.sum(10, 1000, function(response) {
                    console.log("Sum result " + response);
                });

            });

        </script>
    </head>
    <body>
    </body>
</html>
```

* Start the server

     $python your_slurpy_server.py


