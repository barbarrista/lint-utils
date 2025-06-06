from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from lint_utils.config import LintUtilsConfig
from lint_utils.tree_info import get_tree_info
from lint_utils.visitors.useless_fields import check_useless_field


@dataclass(frozen=True, slots=True, kw_only=True)
class CheckResult:
    files_count: int
    errors_files_count: int
    not_processed_files: list[str]


class CheckCommand:
    def __init__(
        self,
        paths: Iterable[Path],
        config: LintUtilsConfig | None,
    ) -> None:
        self._paths = paths
        self._config = config

    def execute(self) -> CheckResult:
        files_count = 0
        errors_files_count = 0
        not_processed_files: list[str] = []

        for path in self._paths:
            info = get_tree_info(path)
            if info is None:
                not_processed_files.append(path.as_posix())
                continue

            has_errors = check_useless_field(
                info,
                file_path=path,
                config=self._config,
            )

            if has_errors:
                errors_files_count += 1

            files_count += 1

        return CheckResult(
            files_count=files_count,
            errors_files_count=errors_files_count,
            not_processed_files=not_processed_files,
        )
