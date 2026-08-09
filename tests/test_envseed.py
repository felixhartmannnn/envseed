from __future__ import annotations

from pathlib import Path
from typing import List

import pytest

from envseed import render, scan
from envseed.cli import main as cli_main


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_scan_finds_env_var_names(tmp_path: Path) -> None:
    p = tmp_path / "main.py"
    _write(p, "import os\nDB_HOST = os.getenv(\"DB_HOST\")\nDB_PORT = os.getenv(\"DB_PORT\")\n")
    results = scan([p])
    assert len(results) == 1
    assert results[0][1] == ["DB_HOST", "DB_PORT"]


def test_scan_skips_hidden_directories(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    _write(src / "main.py", "import os\nX = os.getenv(\"X\")\n")
    hidden = tmp_path / ".git"
    hidden.mkdir()
    _write(hidden / "hidden.py", "import os\nSECRET = os.getenv(\"SECRET\")\n")
    results = scan([tmp_path])
    for _, vars_ in results:
        assert "SECRET" not in vars_
    assert any(path.name == "main.py" for path, _ in results)


def test_scan_missing_vars_reports_error(tmp_path: Path) -> None:
    p = tmp_path / "app.py"
    _write(p, "import os\nX = os.getenv(\"X\")\nY = os.getenv(\"Y\")\n")
    results = scan([p])
    assert all(isinstance(v, str) for _, vars_ in results for v in vars_)
    assert results[0][1] == ["X", "Y"]


def test_render_formats_output() -> None:
    env_vars = ["DB_HOST", "DB_PORT"]
    text = render(env_vars)
    assert "DB_HOST=<value>" in text
    assert "DB_PORT=<value>" in text
    assert text.endswith("\n")


def test_cli_scan_writes_output_file(tmp_path: Path) -> None:
    src = tmp_path / "app.py"
    _write(src, "import os\nAPI_KEY = os.getenv(\"API_KEY\")\n")
    out = tmp_path / ".env.example"
    rc = cli_main(["add", str(src), "-o", str(out)])
    assert rc == 0
    assert out.exists()
    assert "API_KEY=<value>" in out.read_text(encoding="utf-8")


def test_cli_scan_returns_zero_on_success() -> None:
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "main.py"
        p.write_text("import os\nX = os.getenv('X')\n", encoding="utf-8")
        rc = cli_main(["add", str(p)])
        assert rc == 0
