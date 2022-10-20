from struct_tree import output_socket, input_socket, StructNode


@input_socket('frequency')
@output_socket('output')
class SineOscillator(StructNode):
    pass
