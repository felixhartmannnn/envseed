from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Sequence

from envseed import render, scan


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="envseed", description="Scan source files for os.getenv() and render an .env.example.")
    parser.add_argument("paths", nargs="+", type=Path, help="Source files or directories to scan")
    parser.add_argument("--include", nargs="*", default=["*.py"], help="Glob patterns to include")
    parser.add_argument("--skip", nargs="*", default=[".git", "__pycache__", ".venv", "node_modules"], help="Path segments to skip")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output file path")

    args = parser.parse_args(argv)
    results = scan(args.paths, include=args.include, skip=tuple(args.skip))
    ordered_vars: List[str] = []
    seen: set = set()
    for _, vars_ in results:
        for var in vars_:
            if var not in seen:
                ordered_vars.append(var)
                seen.add(var)
    text = render(ordered_vars)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
