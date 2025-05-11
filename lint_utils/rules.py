import re
from types import SimpleNamespace


class Rule(SimpleNamespace):
    useless_field = "USL001"


def can_ignore_rule(code_lines: list[str], line_number: int, rule: str) -> bool:
    pattern = r"lu:\s*([A-Z]+\d+(?:,\s*[A-Z]+\d+)*)"
    code_line = code_lines[line_number]

    match = re.search(pattern, code_line)
    codes: tuple[str, ...] = ()
    if match:
        codes = tuple(str(code).strip() for code in match.group(1).split(","))

    return rule in codes
