# Lint Utils

The humble linter package

## Installation

```bash
pip install lint-utils
```

## Usage

```bash
lu check src
```

or

```bash
lu check path/to/file_1.py path/to/file_2/ path/to/dir
```

## Aliases

short alias: `lu check ...`

full alias `lint-utils check ...`

## Rules

**USL001** - Unused object class fields found

## Configuration

You can create `lint_utils.toml` in root project directory

```toml
[lint-utils]
exclude = []
lint.ignore = []

[lint-utils.exclude-base-classes]
USL001 = []

[lint-utils.exclude-classes]
USL001 = []
```

`pyproject.toml` is also supported

```toml
...

[tool.lint-utils]
exclude = []
lint.ignore = []

[tool.lint-utils.exclude-base-classes]
USL001 = []

[tool.lint-utils.exclude-classes]
USL001 = []
```

### exclude

If you put a file path in the exclude list, it will be ignored during checking.

```toml
...

[tool.lint-utils]
exclude = ["path/to/file.py"]
```

### tool.lint-utils.exclude-base-classes

If you add a base class, it and its child classes will be ignored during validation.

```toml
...

[tool.lint-utils.exclude-base-classes]
USL001 = ["Exception"]
```

Example:

```py
# src/exceptions.py
class FieldNameError(Exception):
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name
```

This file will be ignored if `USL001` rules are followed, because `Exception` class putted in `tool.lint-utils.exclude-base-classes`

### tool.lint-utils.exclude-classes

If you add a class, it will be ignored during validation.

```toml
...

[tool.lint-utils.exclude-classes]
USL001 = ["FieldNameError"]
```

Example:

```py
# src/exceptions.py
class FieldNameError(Exception):
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name
```

This file will be ignored, because `FieldNameError` class putted in lint.exclude_classes for `USL001` rule

### lint.ignore

If you add a rule code, it will be ignored during validation.

```toml
...

[tool.lint-utils]
lint.ignore = ["USL001"]
```

### Line ignoring

In order not to conflict with Ruff and `noqa`, it was decided to specify the following design:

```python
class CommandCommand:
    def __init__(self, variable: str) -> None:
        self._variable = variable  # lu: USL001
```
