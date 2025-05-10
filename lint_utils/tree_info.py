import ast
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class TreeInfo:
    tree: ast.Module
    raw: str


def get_tree_info(file_path: Path) -> TreeInfo | None:
    with (
        suppress(SyntaxError, OSError, UnicodeDecodeError),
        file_path.open("r", encoding="UTF-8") as file,
    ):
        source = file.read()
        return TreeInfo(tree=ast.parse(source), raw=source)

    return None
