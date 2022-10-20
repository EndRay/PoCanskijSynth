import os
import re

from code_generator.utils import space_all_lines
from settings import TEMPLATES_FOLDER, GENERATED_CPP, EMPTY_BLOCK_COMMENTS


def replace(code: str, block_name: str, replacement: str) -> str:
    block = re.search(rf' *// *\[ *{block_name} *] *', code) or \
            re.search(rf'/\* *\[ *{block_name} *] \**/', code)
    if block is None:
        raise ValueError(f'block {block_name} not found')
    block = block.group()
    if replacement is None:
        return code.replace(block, '')
    # count spaces on the start of the block
    spaces = len(block) - len(block.lstrip(' '))
    if not replacement.strip() and EMPTY_BLOCK_COMMENTS:
        return code.replace(block, space_all_lines(f"/* block {block_name} is empty */", spaces))
    return code.replace(block, space_all_lines(replacement, spaces))


def fill_template(code: str, replacements: dict[str, str]) -> str:
    for block_name, replacement in replacements.items():
        code = replace(code, block_name, replacement)
    return code


def get_filled_template(template_name: str, replacements: dict[str, str]) -> str:
    with open(os.path.join(TEMPLATES_FOLDER, template_name), 'r') as f:
        code = f.read()
    return fill_template(code, replacements)


def write_filled_template(file_name: str, template_name: str, replacements: dict[str, str]) -> None:
    os.makedirs(GENERATED_CPP, exist_ok=True)
    with open(os.path.join(GENERATED_CPP, file_name), "w") as fhpp:
        fhpp.write(get_filled_template(template_name, replacements))
