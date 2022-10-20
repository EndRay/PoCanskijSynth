from __future__ import annotations

from typing import TYPE_CHECKING, Collection

if TYPE_CHECKING:
    from struct_tree.sockets.input_socket import InputSocket
    from struct_tree import StructNode


class OutputSocket:
    def __init__(self, node: StructNode, name: str):
        self.__name = name
        self.__connected_to: set[InputSocket] = set()
        self.__node = node

    def add_to_connected(self, input_socket: InputSocket):
        self.__connected_to.add(input_socket)

    def remove_from_connected(self, input_socket: InputSocket):
        self.__connected_to.remove(input_socket)

    @property
    def connected_to(self) -> Collection[InputSocket]:
        return frozenset(self.__connected_to)

    @property
    def cpp_getter(self):
        return self.__node.OUTPUTS[self.__name].cpp_getter

    @property
    def name(self):
        return self.__name

    @property
    def node(self) -> StructNode:
        return self.__node

    def __repr__(self):
        return repr(self.__node) + '.' + self.__name
