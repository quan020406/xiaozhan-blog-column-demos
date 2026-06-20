from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", "target", "dist"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".toml"}
RULES = {
    "windows_absolute_path": re.compile(r"(?i)\b[a-z]:[\\/]"),
    "loopback_address": re.compile(r"(?i)(?:127\.0\.0\.1|localhost)"),
    "known_local_user": re.compile(r"31899"),
}


def main() -> None:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(content.splitlines(), 1):
            for name, pattern in RULES.items():
                if pattern.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{line_number} [{name}]")
    if findings:
        print("\n".join(findings))
        raise SystemExit(1)
    print("Portability check passed: no machine-specific paths or loopback hosts found.")


if __name__ == "__main__":
    main()

