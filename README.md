# envseed

Scan source files for `os.getenv()` calls and generate `.env.example` files.

## About

`envseed` reads Python source files, extracts environment variable names from `os.getenv("NAME")` calls, and emits a `.env.example` listing. It is intentionally small and stdlib-only.

## Features

- Scan files or directories for env var names
- Render a `.env.example` listing with stable ordering
- Supports glob-based file inclusion
- Optional direct write to an output file
- Works as both a CLI and a library

## Installation

```bash
python -m pip install -e .
```

Requires Python 3.8 or newer. No external dependencies.

## Usage

```bash
# Scan src/ and write .env.example
envseed src/ -o .env.example

# Scan specific files
envseed app/main.py config.py

# Include only certain patterns
envseed . --include "*.py" --include "*.sh"
```

## Project structure

```text
envseed/
  envseed/
    __init__.py
    cli.py
  tests/
    test_envseed.py
  pyproject.toml
  README.md
```

## Tags

env, dotenv, scanner, cli, stdlib
