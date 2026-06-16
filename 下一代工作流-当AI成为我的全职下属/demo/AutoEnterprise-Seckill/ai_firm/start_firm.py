from __future__ import annotations

import argparse
import json
from pathlib import Path

from cheat_detector import scan
from context_pruner import JavaContextPruner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local AI-firm governance workflow")
    parser.add_argument("--issue", type=Path, default=Path("issue.txt"))
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("src/main/java/com/xiaoz/seckill/service/AtomicSeckillService.java"),
    )
    parser.add_argument("--report", type=Path, default=Path("reports/firm-report.json"))
    args = parser.parse_args()

    issue = args.issue.read_text(encoding="utf-8").strip()
    context = JavaContextPruner(Path("src/main/java"), max_depth=2).prune(args.target)
    findings = scan(Path("."))
    report = {
        "issue": issue,
        "target": str(args.target),
        "context_file_count": context["file_count"],
        "context_character_count": context["character_count"],
        "integrity_passed": not findings,
        "findings": findings,
        "next_action": "review implementation and run mvn test" if not findings else "reject change",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

