def space_all_lines(code: str, count=1) -> str:
    is_endl = code.endswith("\n")
    for _ in range(count):
        code = " " + code.replace("\n", "\n ")
        if is_endl:
            code = code[:-1]
    return code


def tab_all_lines(code: str, count=1) -> str:
    return space_all_lines(code, count * 4)
