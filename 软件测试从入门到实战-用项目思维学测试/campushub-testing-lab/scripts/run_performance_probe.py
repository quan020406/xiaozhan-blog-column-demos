from __future__ import annotations

import argparse
import csv
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SCENARIOS = [
    ("GET /api/health", "/api/health"),
    ("GET /api/activities", "/api/activities?username=student01"),
    ("GET /api/rooms", "/api/rooms"),
    ("GET /api/devices", "/api/devices"),
    ("GET /api/notifications", "/api/notifications?username=student01"),
    ("GET /api/books keyword", "/api/books?" + urllib.parse.urlencode({"keyword": "测试"})),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a JMeter-compatible JTL by calling CampusHub APIs.")
    parser.add_argument("--base-url", default="http://localhost:8080", help="Backend base URL.")
    parser.add_argument("--loops", type=int, default=5, help="Loops per scenario.")
    parser.add_argument("--output", default="test-assets/reports/jmeter-latest.jtl", help="Output JTL path.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "timeStamp",
        "elapsed",
        "label",
        "responseCode",
        "responseMessage",
        "threadName",
        "dataType",
        "success",
        "bytes",
        "sentBytes",
        "grpThreads",
        "allThreads",
        "URL",
        "Latency",
        "IdleTime",
        "Connect",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for loop_index in range(args.loops):
            for label, path in SCENARIOS:
                url = args.base_url.rstrip("/") + path
                started = time.perf_counter()
                timestamp = int(time.time() * 1000)
                response_code = "200"
                response_message = "OK"
                success = True
                body_size = 0
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        body = response.read()
                        body_size = len(body)
                        response_code = str(response.status)
                        response_message = response.reason
                        success = 200 <= response.status < 400
                except urllib.error.HTTPError as exc:
                    body = exc.read()
                    body_size = len(body)
                    response_code = str(exc.code)
                    response_message = exc.reason
                    success = False
                except Exception as exc:
                    response_code = "0"
                    response_message = exc.__class__.__name__
                    success = False
                elapsed = max(1, int((time.perf_counter() - started) * 1000))
                writer.writerow({
                    "timeStamp": timestamp,
                    "elapsed": elapsed,
                    "label": label,
                    "responseCode": response_code,
                    "responseMessage": response_message,
                    "threadName": f"probe-{loop_index + 1}",
                    "dataType": "text",
                    "success": str(success).lower(),
                    "bytes": body_size,
                    "sentBytes": 0,
                    "grpThreads": 1,
                    "allThreads": 1,
                    "URL": url,
                    "Latency": elapsed,
                    "IdleTime": 0,
                    "Connect": 0,
                })
    print(f"jtl generated: {output.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
