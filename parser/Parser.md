# Python AST Parser

## Data Flow

Code -> `ast.parse(...)` -> Python AST -> visitor walk -> extracted data

## What It Extracts

- module docstring
- imports and import-from statements
- top-level assignments
- functions and async functions
- classes, methods, and class attributes

## Usage

```bash
python -m python_parser path/to/file.py
```

Read from stdin:

```bash
cat path/to/file.py | python -m python_parser --stdin
```

Pretty-print JSON output:

```bash
python -m python_parser path/to/file.py --indent 2
```
