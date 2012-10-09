var Slurpy = (function() {

    function Slurpy(hostname, port) {
        this.events = {};
        this.port = port || {{ port }};
        this.hostname = hostname || "{{ host }}";
        
        this.websocket = new WebSocket("ws://" + this.hostname + ":" + this.port + "/slurpy" );
        this.websocket.onopen = this.load;
        this.websocket.onmessage = this.receive;
    }

    Slurpy.prototype.messages = {
        LOAD : 'load',
        UNLOAD: 'unload'
    }

    Slurpy.prototype.on = function(event, callback) {
        if ( typeof this.events[event] === undefined || this.events[event] == null )
            this.events[event] = []
        this.events[event].push(callback);
    }

    Slurpy.prototype.emit = function(event, data) {
        for(var callback in this.events[event]) {
            return this.events[event][callback].apply(this, data);
        }
    }

    Slurpy.prototype.load = function() {
        return this.send(
            python.utils.hydrate({ 
                'action': python.messages.LOAD,
                'functions' : Object.keys(python.get_js_functions()) 
            })
        );
    }

    Slurpy.prototype.utils = {
        hydrate: function(message) {
            return JSON.stringify(message);
        },
        
        wrap: function(fn) {
            return function() {
                return this.call(fn, arguments);
            }
        },

        wrap_module: function(module, fn) {
            return function() {
                return python.call_module(module, fn, arguments);
            }
        }
    }
 
    Slurpy.prototype.call_module = function(module, fn, arguments) {
        this.websocket.send(
            this.utils.hydrate({ 
                'action': 'execute',
                'args': arguments,
                'module': module, 
                'method': fn,
                'functions' : Object.keys(python.get_js_functions()),
                'callback': arguments[arguments.length-1].toString()
            })
        );
    } 

    Slurpy.prototype.call = function(fn, arguments) {
        this.websocket.send(
            this.utils.hydrate({ 
                'action': 'execute',
                'args': arguments, 
                'method': fn,
                'functions' : Object.keys(python.get_js_functions()),
                'callback': arguments[arguments.length-1].toString()
            })
        );
    } 

   Slurpy.prototype.receive = function(event) {
        var message = eval('(' + event.data + ')');

        if ( message != undefined && message != '' ) {
            
            switch(message.action) {
                case 'load' : {

                    if ( message.functions ) {
                        for ( var func in message.functions ) {
                            python[message.functions[func]] = 
                                python.utils.wrap(message.functions[func]);
                        }
                    }

                    if ( message.modules ) {
                        var modules = Object.keys(message.modules);
                        for ( var index in modules ) {
                            var module = modules[index];
                            
                            if ( ! python[module] ) 
                                python[module] = {}
                            
                            for ( var func in message.modules[module] ) {
                                python[module][message.modules[module][func]] = 
                                        python.utils.wrap_module(module, message.modules[module][func]);
                            }
                        }
                    }

                    python.emit('loaded', event);
                    break;
                }
                
                case 'callback' : {
                    var method = eval('(' + message.fn + ')')(message.response);
                    break;
                }

                case 'execute': {
                    try {
                        method = python.lookup(message.method).apply(this, message.args);
                    } catch(error) {
                        method = python.lookup(message.method)(message.args);
                    } finally {
                        return python.py_return(method, message.callback);
                    }
                    break;
                }
            }                        
        }
    }

    Slurpy.prototype.py_return = function(value, callback) {
        this.websocket.send(
            this.utils.hydrate({   
                'action': 'return', 
                'result' : value ,
                'callback' : callback 
            })
        );
    }

    Slurpy.prototype.lookup = function(name) {
        var functions = this.get_js_functions();
        for(var func in functions) {
            if ( func == name ) {
                return functions[func];
            } 
        }
        return false;
    }

    Slurpy.prototype.get_js_functions = function() {
        var functions = {}
        for(var obj in window) {
            if ( typeof(window[obj]) == 'function' ) {
                functions[obj] = window[obj];
            }
        }
        return functions;
    }

    return Slurpy;

})();        

python = new Slurpy();
