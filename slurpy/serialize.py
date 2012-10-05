#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5

import marshal
import json
import types


class CallbackSerialize:

    @classmethod
    def md5sum(cls, serialized):
        hasher = md5()
        hasher.update(serialized)
        return hasher.hexdigest()

    @classmethod
    def serialize(cls, function):
        if callable(function):
            serialized = json.dumps((
                            marshal.dumps(function.func_code),
                            function.func_name,
                            function.func_defaults)
                        )
            return (cls.md5sum(serialized), serialized)

    @classmethod
    def deserialize(cls, encoded):
        (code, name, defaults) = json.loads(encoded)
        code = marshal.loads(code)

        return (cls.md5sum(encoded), \
                types.FunctionType(code, globals=globals(), name=str(name), \
                                                            argdefs=defaults))
