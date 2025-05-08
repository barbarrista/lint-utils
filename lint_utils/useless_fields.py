import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping, TypeAlias

from lint_utils.rules import Rule, can_ignore_rule
from lint_utils.std import report_info
from lint_utils.text_styling import to_bold, to_cyan, to_red
from lint_utils.tree_info import TreeInfo

FuncDef: TypeAlias = ast.FunctionDef | ast.AsyncFunctionDef


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldInfo:
    name: str
    line: int
    col_offset: int
    assigned_to: str | None = None


class UselessFieldVisitor(ast.NodeVisitor):
    rule: Final[str] = Rule.useless_field

    def __init__(self, raw_code: str) -> None:
        super().__init__()

        self._code_lines = raw_code.split("\n")
        self._class_name: str
        self._field_definitions: dict[str, FieldInfo] = {}

    @property
    def useless_fields(self) -> Mapping[str, FieldInfo]:
        return self._field_definitions

    @property
    def class_name(self) -> str:
        return self._class_name

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self._class_name = node.name

        for item in node.body:
            if not isinstance(item, FuncDef):
                continue

            if item.name == "__init__":
                self._process_init_assignment(item)

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if isinstance(node.ctx, ast.Load):
            root_node = _find_root_node(node)
            self._field_definitions.pop(root_node.attr, None)

        return self.generic_visit(node)

    def _process_init_assignment(self, method: FuncDef):
        for item in method.body:
            match item:
                case ast.Assign():
                    target = item.targets[0]
                    if not isinstance(target, ast.Attribute):
                        continue

                    field_info = FieldInfo(
                        name=target.attr,
                        line=target.lineno,
                        col_offset=target.col_offset,
                        assigned_to=_get_assigned_to(item),
                    )

                case ast.AnnAssign():
                    target = item.target
                    if not isinstance(target, ast.Attribute):
                        continue

                    field_info = FieldInfo(
                        name=target.attr,
                        line=target.lineno,
                        col_offset=target.col_offset,
                        assigned_to=_get_assigned_to(item),
                    )

                case _:
                    continue

            if can_ignore_rule(
                self._code_lines,
                line=field_info.line - 1,
                rule=self.rule,
            ):
                continue

            self._field_definitions[field_info.name] = field_info


def _get_assigned_to(attr: ast.Assign | ast.AnnAssign) -> str | None:
    if not isinstance(attr.value, ast.Name):
        return

    return attr.value.id


def _find_root_node(node: ast.Attribute) -> ast.Attribute:
    if isinstance(node.value, ast.Attribute):
        return _find_root_node(node.value)

    return node


def check_useless_field(info: TreeInfo, *, file_path: Path) -> bool:
    visitor = UselessFieldVisitor(raw_code=info.raw)
    visitor.visit(info.tree)

    if visitor.useless_fields:
        msg = f"{to_bold(to_cyan(visitor.rule))} Unused object class fields found in class {to_bold(visitor.class_name)}"
        report_info(msg)
        for field_info in visitor.useless_fields.values():
            full_path = (
                f"{file_path.as_posix()}:{field_info.line}:{field_info.col_offset + 1}"
            )
            line_msg = f"{full_path} {to_bold(to_red(f'self.{field_info.name}'))}"
            report_info(line_msg)
        report_info("")

        return True

    return False
