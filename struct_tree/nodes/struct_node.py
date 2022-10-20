from __future__ import annotations
from typing import Collection, TYPE_CHECKING

from struct_tree.sockets.input_socket import InputSocket
from struct_tree.sockets.output_socket import OutputSocket

if TYPE_CHECKING:
    from struct_tree.sockets.input_socket import PossibleInput


class StructNode:

    INPUTS = {}
    OUTPUTS = {}
    DELAY = False
    TEMPLATE = 'class.hpp'
    _last_id = -1

    def __init__(self):
        self._inputs: dict[str, InputSocket] = {}
        self._outputs: dict[str, OutputSocket] = {}
        StructNode._last_id += 1
        self.__id = StructNode._last_id

    @property
    def inputs(self) -> Collection[InputSocket]:
        return frozenset(self._inputs.values())

    @property
    def outputs(self) -> Collection[OutputSocket]:
        return frozenset(self._outputs.values())

    @property
    def id(self):
        return self.__id

    def __getitem__(self, item):
        if item in self._inputs:
            return self._inputs[item]
        if item in self._outputs:
            return self._outputs[item]

    def __setitem__(self, key: str, value: PossibleInput | StructNode):
        if key in self._outputs:
            raise ValueError('cannot write to the output')
        if key in self._inputs:
            if isinstance(value, StructNode):
                try:
                    self._inputs[key].connected_to = value['output']
                except KeyError:
                    raise ValueError('specify output socket')
            else:
                self[key].connected_to = value

    def __repr__(self):
        return f'{self.__class__.__name__}_{self.id}'
