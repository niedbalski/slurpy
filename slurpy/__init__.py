import logging
import sys
import json
import os
import types

from slurpy.serialize import CallbackSerialize
from tornado import websocket, ioloop, httpserver, web, template


_HERE = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger('slurpy')

callbacks = []
javascript = None


class Javascript:

    def __init__(self, functions, websocket):
        self.functions = functions
        self.websocket = websocket

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name in self.functions:
                self.run(name, *args, **kwargs)
        return method

    def run(self, name, *args, **kwargs):
        callback = None
        if 'callback' in kwargs:
            (md5sum, callback) = \
                    CallbackSerialize.serialize(kwargs['callback'])

            if md5sum not in callbacks:
                callbacks.extend({md5sum: callback})

        self.websocket.write_message(json.dumps({'method': name,
                                                 'action': 'execute',
                                                 'callback': callback,
                                                 'args': args }))


class SlurpyJSHandler(web.RequestHandler):

    def initialize(self, host, port):
        self.host = host
        self.port = port

    def get(self):
        return self.render("js/slurpy.js", host=self.host, port=self.port)


class SlurpyHandler(websocket.WebSocketHandler):

    def initialize(self, methods):
        self.methods = methods

    def on_open(self):
        pass

    def response(self, message):
        self.write_message(json.dumps(message))

    def load_javascript(self, functions):
        global javascript
        javascript = Javascript(functions, self)

    def _hydrate_functions(self):
        modules = {}
        for module, methods in self.methods['modules'].items():
                modules[module] = self.methods['modules'][module].keys()
        return ( modules, self.methods['functions'].keys() )

    def load_handler(self, message):
        (modules, functions) = self._hydrate_functions()
        self.response({'action': 'load', 'functions': functions, \
                                         'modules': modules})

    def return_handler(self, message):
        if 'callback' in message:
            (md5sum, callback) = \
                    CallbackSerialize.deserialize(message['callback'])

            if not md5sum in callbacks:
                raise Exception("Invalid callback function call")

            if 'result' in message:
                return callback(message['result'])

            return callback()

    def call_method(self, message):
        if 'module' in message:
            method = self.methods['modules'][message['module']][message['method']]
        else:
            method = self.methods['functions'][message['method']]

        if 'args' in message:
            response = method(*message['args'].values())
        else:
            response = method()

        return response

    def execute_handler(self, message):
        self.load_javascript(message['functions'])
        self.response({'action': 'callback', 'fn': message['callback'],
                       'response': self.call_method(message)})

    def hydrate_message(self, action, message):
        try:
            handler = getattr(self, action + "_handler")
        except AttributeError:
            raise Exception("Not found method %s " % action)
        return handler(message)

    def on_message(self, message):
        try:
            message = json.loads(message)
        except Exception as ex:
            logger.error(ex)
            raise

        if not 'action' in message:
            raise Exception("Please specify a valid action to be executed")

        message = self.hydrate_message(message['action'], message)

    def on_close(self):
        return


class Slurpy:

    methods = { 'functions': {}, 'modules': {} }

    def __init__(self, host="localhost", port=51711):
        self.host = host
        self.port = port

    def register(self, obj):
        if callable(obj):
            if  obj in self.methods['functions']:
                raise Exception("Function %s already exists" % obj.__name__)
            self.methods['functions'][obj.__name__] = obj
        elif isinstance(obj, types.ModuleType):
            for attr in obj.__dict__:
                if isinstance(obj.__dict__[attr], types.FunctionType) or \
                    isinstance(obj.__dict__[attr], types.BuiltinFunctionType) or \
                        isinstance(obj.__dict__[attr], types.BuiltinMethodType):
                    if not 'modules' in self.methods:
                        self.methods['modules'] = {}
                    if not obj.__name__ in self.methods['modules']:
                        self.methods['modules'][obj.__name__] = {}
                    self.methods['modules'][obj.__name__][attr] = \
                                                    obj.__dict__[attr]

    def start(self):
        """
            Start the server using a tornado Application
        """
        self.application = \
            web.Application([
                (r'/slurpy', SlurpyHandler, dict(methods=self.methods)),
                (r'/slurpy/js', SlurpyJSHandler,
                    dict(host=self.host, port=self.port))])

        http_server = httpserver.HTTPServer(self.application)
        http_server.listen(self.port)

        ioloop.IOLoop.instance().start()
        logger.debug("Started slurpy server -methods: %s" % self.methods)
