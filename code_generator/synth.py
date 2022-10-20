from numbers import Number
from warnings import warn

from code_generator.classes import generate_class
from code_generator.templates import write_filled_template
from settings import SAMPLERATE
from struct_tree import StructNode
from struct_tree.order import topsort
from struct_tree.sockets import OutputSocket


def expand_tree(tree: list[StructNode]) -> None:
    for node in tree:
        for input_socket in node.inputs:
            if isinstance(conn := input_socket.connected_to, OutputSocket) and conn.node not in tree:
                tree.append(conn.node)
    for node in tree:
        for output_socket in node.outputs:
            for neighbour in output_socket.connected_to:
                if neighbour.node not in tree:
                    warn(f'node {neighbour.node} not used in result')


def generate_synth(tree: list[StructNode]):
    expand_tree(tree)
    if any(any(input_socket.connected_to is None for input_socket in node.inputs) for node in tree):
        raise ValueError('not all inputs are connected')
    generated_classes = set()
    for node in tree:
        cls = node.__class__
        if cls not in generated_classes:
            generate_class(cls)
            generated_classes.add(cls)
    includes = '\n'.join(f'#include "{cls.__name__}.hpp"' for cls in generated_classes)

    order = topsort(tree)
    inits = ''
    for node in order:
        init = ''
        init += f'{str(node.__class__.__name__)} {str(node)} = {node.__class__.__name__}();\n'
        init += ''.join(f'{str(node)}.{in_socket.cpp_setter}({in_socket.connected_to});\n'
                        for in_socket in node.inputs if isinstance(in_socket.connected_to, Number))
        inits += init
    inits = inits[:-1]

    default_nodes_updates = ''
    for node in order:
        if node.DELAY:
            continue
        update = ''
        update += ''.join(f'{str(node)}.{in_socket.cpp_setter}('
                          f'{str(in_socket.connected_to.node)}.{in_socket.connected_to.cpp_getter}());\n'
                          for in_socket in node.inputs if isinstance(in_socket.connected_to, OutputSocket))
        update += f'{str(node)}.calculate();\n'
        default_nodes_updates += update
    default_nodes_updates = default_nodes_updates[:-1]

    delay_nodes_setters = ''
    for node in order:
        if not node.DELAY:
            continue
        setters = ''
        setters += ''.join(f'{str(node)}.{in_socket.cpp_setter}('
                           f'{str(in_socket.connected_to.node)}.{in_socket.connected_to.cpp_getter}());\n'
                           for in_socket in node.inputs if isinstance(in_socket.connected_to, OutputSocket))
        delay_nodes_setters += setters
    delay_nodes_setters = delay_nodes_setters[:-1]

    delay_nodes_recalculation = ''
    for node in order:
        if not node.DELAY:
            continue
        delay_nodes_recalculation += f'{str(node)}.calculate();\n'
    delay_nodes_recalculation = delay_nodes_recalculation[:-1]

    output_nodes = [node for node in order if all(not out_socket.connected_to for out_socket in node.outputs)]
    if not output_nodes:
        raise ValueError('no output nodes')
    if len(output_nodes) > 1:
        raise ValueError('more than one output node')
    output_node = output_nodes[0]
    try:
        output_node['output']
    except KeyError:
        raise ValueError('output node has no output socket')

    replacements: dict[str, str] = {
        "includes": includes,
        "samplerate": str(SAMPLERATE),
        "nodes_inits": inits,
        "default_nodes_update": default_nodes_updates,
        "delay_nodes_setters": delay_nodes_setters,
        "delay_nodes_recalculation": delay_nodes_recalculation,
        "output_node": f'{str(output_node)}.{output_node["output"].cpp_getter}()',
    }
    write_filled_template('synth.cpp', 'synth.cpp', replacements)
