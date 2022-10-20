from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING
from struct_tree.sockets.output_socket import OutputSocket

if TYPE_CHECKING:
    from struct_tree import StructNode
    PossibleInput = OutputSocket | Number | None


class InputSocket:
    def __init__(self, node: StructNode, name: str):
        self.__name: str = name
        self.__connected_to: PossibleInput = None
        self.__node = node

    @property
    def connected_to(self) -> PossibleInput:
        return self.__connected_to

    @connected_to.setter
    def connected_to(self, output_socket: PossibleInput):
        if self.__connected_to == output_socket:
            return
        if isinstance(self.__connected_to, OutputSocket):
            self.__connected_to.remove_from_connected(self)
        self.__connected_to = output_socket
        if isinstance(output_socket, OutputSocket):
            output_socket.add_to_connected(self)

    @property
    def cpp_setter(self) -> str:
        return self.__node.INPUTS[self.__name].cpp_setter

    @property
    def name(self) -> str:
        return self.__name

    @property
    def node(self) -> StructNode:
        return self.__node

    def __repr__(self):
        return repr(self.__node) + '.' + self.__name

