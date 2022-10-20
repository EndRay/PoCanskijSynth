import os
import re
from typing import Type

from code_generator.templates import get_filled_template, write_filled_template
from code_generator.utils import tab_all_lines
from settings import GENERATED_CPP, SRC_FOLDER
from struct_tree import StructNode


def extract_function(code: str, return_type: str, function_name: str) -> (str, str):
    try:
        calculate_start = re.search(rf"{return_type} +{function_name}\(\) *{{", code).start()
        calculate_end = code.find("}", calculate_start)
    except AttributeError:
        raise ValueError("calculate function not found")
    calculate_function = \
        code[calculate_start:calculate_end+1]
    code = code.replace(calculate_function, "")
    calculate_function = calculate_function
    return code, calculate_function


# todo: inheritance
# todo: init
# todo: includes
def generate_class(node_cls: Type[StructNode]) -> str:
    # open file with node's name for read
    file_name = node_cls.__name__ + ".hpp"
    with open(os.path.join(SRC_FOLDER, node_cls.__name__ + ".cpp"), "r") as f:
        code = f.read()
        code, calculate_function = extract_function(code, "void", "calculate")
        code = code.strip()
        replacements = {
            "class_name": node_cls.__name__,
            "inputs": "\n".join(f"double {socket.name};" for socket in node_cls.INPUTS.values()),
            "outputs": "\n".join(f"double {socket.name};" for socket in node_cls.OUTPUTS.values()),
            "private": code,
            "setters": "\n".join(
                f"void {socket.cpp_setter}(double value) {{\n"
                f"    {socket.name} = value;\n"
                f"}}" for socket in node_cls.INPUTS.values()),
            "getters": "\n".join(
                f"double {socket.cpp_getter}() {{\n"
                f"    return {socket.name};\n"
                f"}}" for socket in node_cls.OUTPUTS.values()),
            "calculate": calculate_function
        }
        write_filled_template(file_name, node_cls.TEMPLATE, replacements)

    return file_name
