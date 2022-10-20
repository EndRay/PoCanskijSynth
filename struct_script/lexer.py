from collections import namedtuple

from struct_script.utils import enum

LexemeType = enum("NAME", "NUMBER", "OPERATOR", "EOL", "COMMA", "DOT",
                  "OPEN_BRACKET", "CLOSE_BRACKET", "EOF")
Lexeme = namedtuple("Lexeme", ["type", "value"])

OPERATORS = ['+', '-', '*', '/', '->', '<-', '=']

NUMBER_SUFFIXES: dict[str, int] = {
    "": 1,
    "k": 1000,
    "m": 1000000,
}

NUMBER_UNITS: dict[str, callable] = {
    "": lambda x: x,
}

# order dicts by keys from longer to shorter
NUMBER_SUFFIXES = {k: v for k, v in sorted(NUMBER_SUFFIXES.items(), key=lambda item: len(item[0]), reverse=True)}
NUMBER_UNITS = {k: v for k, v in sorted(NUMBER_UNITS.items(), key=lambda item: len(item[0]), reverse=True)}


def parse_number(number_str: str) -> float:
    initial_number = number_str
    number_conversion = None
    number_coefficient = None
    for unit, conversion in NUMBER_UNITS.items():
        if number_str.endswith(unit):
            number_conversion = conversion
            number_str = number_str[:-len(unit)]
    for suffix, coefficient in NUMBER_SUFFIXES.items():
        if number_str.endswith(suffix):
            number_coefficient = coefficient
            number_str = number_str[:-len(suffix)]
    try:
        number = float(number_str)
    except ValueError:
        raise ValueError(f"invalid number: {initial_number}")
    number *= number_coefficient
    number = number_conversion(number)
    return number


def lex(code: str) -> list[Lexeme]:
    res = []
    while code:
        # name
        if code[0].isalpha() or code[0] == '_':
            acc = ""
            while code and (code[0].isalpha() or code[0].isdigit() or code[0] == '_'):
                acc += code[0]
                code = code[1:]
            res.append(Lexeme("name", acc))
        # number
        elif code[0].isdigit():
            acc = ""
            while code and (code[0].isalpha() or code[0].isdigit() or code[0] == '.'):
                acc += code[0]
                code = code[1:]
            res.append(Lexeme("NUMBER", parse_number(acc)))
        elif code.startswith(","):
            res.append(Lexeme("COMMA", ","))
            code = code[1:]
        elif code.startswith("."):
            res.append(Lexeme("DOT", "."))
            code = code[1:]
        elif code.startswith("("):
            res.append(Lexeme("OPEN_BRACKET", "("))
            code = code[1:]
        elif code.startswith(")"):
            res.append(Lexeme("CLOSE_BRACKET", ")"))
            code = code[1:]
        elif code.startswith("\n"):
            res.append(Lexeme("EOL", "\n"))
            code = code[1:]
        elif code.startswith("->") or code.startswith("<-"):
            res.append(Lexeme("CONNECTION", code[:2]))
            code = code[2:]
        # operator
        else:
            for operator in OPERATORS:
                if code.startswith(operator):
                    res.append(Lexeme("OPERATOR", operator))
                    code = code[len(operator):]
                    break
    res.append(Lexeme("EOF", ""))
    return res
