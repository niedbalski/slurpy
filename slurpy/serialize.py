#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshal
import json
import types


class CallbackSerialize:

    @classmethod
    def serialize(cls, function):
        if callable(function):
            serialized = json.dumps((
                            marshal.dumps(function.func_code),
                            function.func_name,
                            function.func_defaults)
                        )
            return serialized

    @classmethod
    def deserialize(cls, encoded):
        (code, name, defaults) = json.loads(encoded)
        code = marshal.loads(code)

        return types.FunctionType(code, globals=globals(), name=str(name), \
                                                            argdefs=defaults)
