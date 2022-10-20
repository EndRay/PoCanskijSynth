from collections import namedtuple
from functools import wraps

from struct_tree.sockets.input_socket import InputSocket

InputSocketInfo = namedtuple('InputSocketInfo', ['node', 'name', 'cpp_setter'])


def input_socket(name: str, cpp_setter: str = None):
    cpp_setter = cpp_setter or 'set_'+name

    def decorator(cls):
        cls.INPUTS[name] = InputSocketInfo(cls, name, cpp_setter)

        orig_init = cls.__init__

        @wraps(cls.__init__)
        def __init__(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            if name in self._inputs:
                raise ValueError(f'input socket with name {name} already exists')
            if name in self._outputs:
                raise ValueError(f'cannot create input socket with the same name {name} as output socket')
            self._inputs[name] = InputSocket(self, name)

        cls.__init__ = __init__
        return cls

    return decorator
