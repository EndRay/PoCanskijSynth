from struct_tree import StructNode, output_socket, input_socket


@input_socket('input')
@output_socket('output')
class OneSampleDelay(StructNode):
    DELAY = 1
