Slurpy
======

Slurpy is an RPC mechanism to call python methods from javascript and viceversa.

Installation
------------

Install the package using pip

    $ pip install slurpy

Usage
----

* Create a new Slurpy server instance

```python
from slurpy import Slurpy

def sum(a,b):
    return a + b

s = Slurpy()

#register the method 'sum'
s.register_method(sum)

#start the server
s.start()
```

* Then integrate on your HTML document 

```javascript
<html>
    <head>
       <script type="text/javascript" src="http://localhost:51711/slurpy/js"></script>
       <script type="text/javascript">
            python = new Slurpy();
            python.on('loaded', function(evt) {
                python.sum(100, 1000, function(response) {
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

