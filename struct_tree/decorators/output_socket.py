from collections import namedtuple
from functools import wraps

from struct_tree.sockets.output_socket import OutputSocket

OutputSocketInfo = namedtuple('OutputSocketInfo', ['node', 'name', 'cpp_getter'])


def output_socket(name: str, cpp_getter: str = None):
    cpp_getter = cpp_getter or 'get_'+name

    def decorator(cls):
        cls.OUTPUTS[name] = OutputSocketInfo(cls, name, cpp_getter)

        orig_init = cls.__init__

        @wraps(cls.__init__)
        def __init__(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            if name in self._outputs:
                raise ValueError(f'output socket with name {name} already exists')
            if name in self._inputs:
                raise ValueError(f'cannot create output socket with the same name {name} as input socket')
            self._outputs[name] = OutputSocket(self, name)

        cls.__init__ = __init__
        return cls

    return decorator
