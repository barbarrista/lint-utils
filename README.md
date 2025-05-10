# Lint Utils

The humble linter package

## Installation

```bash
pip install lint_utils
```

## Usage

```bash
lint utils check src
```

or

```bash
lint utils check path/to/file_1.py path/to/file_2/ path/to/dir
```

## Configuration

You can create `lint_utils.toml` in root project directory

```toml
[lint_utils]
exclude = []
lint.exclude_base_classes = []
lint.exclude_classes = []
lint.ignore = []

```

`pyproject.toml` is also supported

```toml
...

[tool.lint_utils]
exclude = []
lint.exclude_base_classes = []
lint.exclude_classes = []
lint.ignore = []

```

### exclude

If you put a file path in the exclude list, it will be ignored during checking.

```toml
...

[tool.lint_utils]
exclude = ["path/to/file.py"]
```

### lint.exclude_base_classes

If you add a base class, it and its child classes will be ignored during validation.

```toml
...

[tool.lint_utils]
lint.exclude_base_classes = ["Exception"]
```

Example:

```py
# src/exceptions.py
class FieldNameError(Exception):
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name
```

This file will be ignored, because `Exception` class putted in lint.exclude_base_classes

### lint.exclude_classes

If you add a class, it will be ignored during validation.

```toml
...

[tool.lint_utils]
lint.exclude_classes = ["FieldNameError"]
```

Example:

```py
# src/exceptions.py
class FieldNameError(Exception):
    def __init__(self, field_name: str) -> None:
        self._field_name = field_name
```

This file will be ignored, because `FieldNameError` class putted in lint.exclude_classes

### lint.ignore

If you add a rule code, it will be ignored during validation.

```toml
...

[tool.lint_utils]
lint.ignore = ["USL001"]
```

## Rules

**USL001** - Unused object class fields found
