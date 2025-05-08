from collections.abc import Sequence
from pathlib import Path
import time
import click

from lint_utils.std import report_info
from lint_utils.text_styling import to_bold, to_green, to_red
from lint_utils.tree_info import get_tree_info
from lint_utils.useless_fields import check_useless_field


@click.group()
def cli() -> None:
    pass


@cli.command("check")
@click.argument("args", nargs=-1)
def check(args: Sequence[str]) -> None:
    start_time = time.perf_counter()
    not_processed_files: list[str] = []
    errors_files_count = 0
    files_count = 0

    if not args:
        report_info(to_red("Please provide the file or directory name"))
        return

    for arg in args:
        root_path = Path(arg)
        if root_path.is_dir():
            for path in root_path.rglob("*.py"):
                info = get_tree_info(path)
                if info is None:
                    not_processed_files.append(path.as_posix())
                    continue

                has_errors = check_useless_field(info, file_path=path)

                if has_errors:
                    errors_files_count += 1

                files_count += 1

        if root_path.is_file():
            info = get_tree_info(root_path)
            if info is None:
                not_processed_files.append(root_path.as_posix())
                continue

            has_errors = check_useless_field(info, file_path=root_path)
            if has_errors:
                errors_files_count += 1

            files_count += 1

    elapsed = time.perf_counter() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    milliseconds = int((elapsed - int(elapsed)) * 10000)
    total_seconds = f"{minutes}:{seconds:02}:{milliseconds:04}"

    if errors_files_count > 0:
        files_part = "files" if errors_files_count > 1 else "file"
        msg = to_bold(to_red(f"Errors found in {errors_files_count} {files_part} 😱"))
        report_info(msg)
    else:
        report_info(to_bold(to_green("No errors found. All is well 🤗")))

    report_info(to_bold((f"Processed {files_count} files at {total_seconds}")))





if __name__ == "__main__":
    cli()
