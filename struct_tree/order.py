from warnings import warn

from struct_tree import StructNode
from struct_tree.exceptions import CyclicStructureError
from struct_tree.sockets import OutputSocket


def topsort(tree: list[StructNode]) -> list[StructNode]:
    visited = set()
    inside = set()
    order = []

    def dfs(node: StructNode):
        if node in inside:
            raise CyclicStructureError(f'cycle detected in tree')
        if node in visited:
            return
        visited.add(node)
        inside.add(node)
        for input_socket in node.inputs:
            if isinstance(conn := input_socket.connected_to, OutputSocket):
                neighbour = conn.node
                if not neighbour.DELAY:
                    dfs(neighbour)
        inside.remove(node)
        order.append(node)
    for v in tree:
        if v.DELAY or all(not out.connected_to for out in v.outputs):
            dfs(v)
    for v in tree:
        if v not in order:
            warn(f'node {v} not used in result')
    return order
