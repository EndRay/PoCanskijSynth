from collections import namedtuple

from struct_script.lexer import Lexeme
from struct_script.utils import enum

PRECEDENCE = {
    "=": 1,
    "->": 1,
    "<-": 1,

    "+": 10,
    "-": 10,

    "*": 20,
    "/": 20,
}

ASTNodeType = enum("OBJECT", "SOCKET", "FUNCTION", "CONSTRUCTOR", "ACTION", "ARITHMETIC_OPERATION")
ASTNode = namedtuple("ASTNode", ["type", "value", "children"])


# lexemes array will be modified
def parse(lexemes: list[Lexeme]):
    def get_precedence(lexeme: Lexeme):
        return PRECEDENCE.get(lexeme.value, 0)

    def parse_atom() -> ASTNode:
        lexeme = lexemes[0]
        match lexeme.type:
            case "OPEN_BRACKET":
                lexemes.pop(0)
                res = parse_expression()
                if lexemes[0].type != "CLOSE_BRACKET":
                    raise Exception("expected ')'")
                lexemes.pop(0)
            case "NUMBER":
                res = ASTNode("NUMBER", lexeme.value, [])
                lexemes.pop(0)

            case "NUMBER":
                return ASTNode("SOCKET", lexeme.value, [])


    def maybe_binary(left: ASTNode, precedence: int) -> ASTNode:
        pass

    def parse_expression() -> ASTNode:
        return maybe_binary(parse_atom(), 0)

    ans: list[ASTNode] = []
    while lexemes[0].type != "EOL":
        cur_lexeme = lexemes[0]
