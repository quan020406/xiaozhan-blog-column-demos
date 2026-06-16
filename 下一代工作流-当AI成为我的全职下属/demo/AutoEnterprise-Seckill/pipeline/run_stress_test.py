from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)


def request_json(url: str, method: str = "GET") -> dict:
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    load_env_file(Path(__file__).resolve().parents[1] / ".env")

    parser = argparse.ArgumentParser(description="Concurrent HTTP stress test for the seckill demo")
    parser.add_argument("--base-url", default=os.environ.get("SECKILL_BASE_URL"))
    parser.add_argument("--mode", choices=("unsafe", "atomic", "redisson"), default="atomic")
    parser.add_argument("--concurrency", type=int, default=100)
    parser.add_argument("--requests", type=int, default=500)
    parser.add_argument("--stock", type=int, default=100)
    args = parser.parse_args()
    if not args.base_url:
        parser.error("set SECKILL_BASE_URL or pass --base-url")

    reset_url = f"{args.base_url}/api/admin/reset?{urllib.parse.urlencode({'stock': args.stock})}"
    request_json(reset_url, method="POST")

    started = time.perf_counter()
    success = 0
    errors: list[str] = []

    def call(user_id: int) -> bool:
        query = urllib.parse.urlencode({"userId": user_id, "productId": 1})
        payload = request_json(f"{args.base_url}/api/seckill/{args.mode}?{query}", method="POST")
        return bool(payload.get("success"))

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(call, user_id) for user_id in range(1, args.requests + 1)]
        for future in as_completed(futures):
            try:
                success += int(future.result())
            except (urllib.error.URLError, TimeoutError, ValueError) as exception:
                errors.append(str(exception))

    elapsed = time.perf_counter() - started
    status = request_json(f"{args.base_url}/api/products/1")
    product = status["product"]
    report = {
        "mode": args.mode,
        "requests": args.requests,
        "concurrency": args.concurrency,
        "initial_stock": args.stock,
        "success_responses": success,
        "database_orders": status["orderCount"],
        "remaining_stock": product["stock"],
        "elapsed_seconds": round(elapsed, 3),
        "requests_per_second": round(args.requests / elapsed, 2),
        "errors": len(errors),
        "oversold": status["orderCount"] > args.stock,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
