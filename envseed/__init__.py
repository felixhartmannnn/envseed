from __future__ import annotations

import re
from pathlib import Path
from typing import List, Sequence, Set, Tuple

ENV_RE = re.compile(r"os\.getenv\(\s*['\"]([^'\"]+)['\"]\)")


def _collect_env_vars(text: str) -> Set[str]:
    return set(ENV_RE.findall(text))


def scan(
    paths: Sequence[Path],
    include: Sequence[str] = ("*.py",),
    skip: Sequence[str] = (".git", "__pycache__", ".venv", "node_modules"),
) -> List[Tuple[Path, List[str]]]:
    results: List[Tuple[Path, List[str]]] = []
    seen: Set[str] = set()
    patterns = tuple(include)

    def _scan(path: Path) -> None:
        path = path.resolve()
        if any(part in skip for part in path.parts):
            return
        if path.is_file():
            for pattern in patterns:
                if path.match(pattern):
                    text = path.read_text(encoding="utf-8", errors="replace")
                    vars_ = sorted(_collect_env_vars(text))
                    if vars_:
                        results.append((path, vars_))
                        seen.update(vars_)
                    break
        elif path.is_dir():
            for child in path.iterdir():
                _scan(child)

    for p in paths:
        _scan(p)
    return results


def render(env_vars: List[str], header: str = "") -> str:
    lines: List[str] = []
    if header:
        lines.append(header)
    lines.extend(f"{var}=<value>" for var in env_vars)
    text = "\n".join(lines)
    if text and not text.endswith("\n"):
        text += "\n"
    return text


__all__ = ["scan", "render"]
