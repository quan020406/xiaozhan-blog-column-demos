import argparse
import csv
import time
from pathlib import Path
from urllib import request


SCENARIOS = [
    ("activities", "/api/activities?username=student01"),
    ("books_search", "/api/books?keyword=%E6%B5%8B%E8%AF%95"),
    ("overview", "/api/overview"),
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run a tiny CampusHub API performance probe.")
    parser.add_argument("--base-url", default="http://localhost:8080", help="Backend base URL.")
    parser.add_argument("--loops", type=int, default=3, help="Loop count per scenario.")
    parser.add_argument("--output", default="test-assets/reports/jmeter-latest.jtl", help="CSV output path.")
    return parser.parse_args()


def main():
    args = parse_args()
    rows = []
    for _ in range(args.loops):
        for label, path in SCENARIOS:
            url = args.base_url.rstrip("/") + path
            started = time.perf_counter()
            success = True
            code = 0
            try:
                with request.urlopen(url, timeout=10) as response:
                    code = response.status
                    response.read()
            except Exception:
                success = False
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            rows.append(
                {
                    "timeStamp": int(time.time() * 1000),
                    "elapsed": elapsed_ms,
                    "label": label,
                    "responseCode": code,
                    "success": str(success).lower(),
                }
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timeStamp", "elapsed", "label", "responseCode", "success"])
        writer.writeheader()
        writer.writerows(rows)

    failures = sum(1 for row in rows if row["success"] != "true")
    print(f"probe samples={len(rows)} failures={failures} output={output}")


if __name__ == "__main__":
    main()
