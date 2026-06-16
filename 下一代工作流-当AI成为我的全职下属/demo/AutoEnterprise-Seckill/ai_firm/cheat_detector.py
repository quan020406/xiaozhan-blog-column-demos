from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    code: str
    pattern: re.Pattern[str]
    message: str


RULES = (
    Rule("DISABLED_TEST", re.compile(r"@Disabled\b"), "禁止跳过核心测试"),
    Rule("ALWAYS_TRUE", re.compile(r"assertTrue\s*\(\s*true\s*\)"), "禁止万能真断言"),
    Rule("EMPTY_CATCH", re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}"), "禁止空 catch 块"),
    Rule("SWALLOW_THROWABLE", re.compile(r"catch\s*\(\s*Throwable\b"), "禁止捕获 Throwable 掩盖失败"),
    Rule("LOW_CONCURRENCY", re.compile(r"concurrent(?:Count|cy)\s*=\s*1\b"), "禁止把并发度降为 1"),
)


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".java", ".py", ".sh", ".ps1"}:
            continue
        if path.name == "cheat_detector.py":
            continue
        if any(part in {"target", ".git", "__pycache__"} for part in path.parts):
            continue
        if "ai_firm" in path.parts and "tests" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for number, line in enumerate(text.splitlines(), 1):
            for rule in RULES:
                if rule.pattern.search(line):
                    findings.append(f"{path}:{number} [{rule.code}] {rule.message}")
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect test weakening and fake-success patterns")
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    findings = scan(args.root)
    if findings:
        print("\n".join(findings))
        raise SystemExit(1)
    print("Integrity audit passed: no forbidden patterns found.")


if __name__ == "__main__":
    main()
