from pathlib import Path
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "CONTRIBUTING.md",
    "FAQ.md",
    "LEARNING_PATH.md",
    "RELEASE_CHECKLIST.md",
    ".gitignore",
    "backend/pom.xml",
    "frontend/package.json",
    "scripts/generate_test_dashboard.py",
    "scripts/run_performance_probe.py",
    "scripts/verify_local.py",
    "scripts/verify_local.ps1",
    "frontend/src/assets/test-assets/test-dashboard.json",
    "frontend/src/assets/test-assets/screenshots/selenium-login.png",
    "frontend/src/assets/test-assets/screenshots/selenium-activity.png",
    "frontend/src/assets/test-assets/screenshots/selenium-room.png",
    "frontend/src/assets/test-assets/screenshots/selenium-device.png",
    "frontend/src/assets/test-assets/screenshots/selenium-booknest.png",
    "frontend/src/assets/test-assets/screenshots/selenium-notification.png",
    "docs/api-contract.md",
    "docs/test-strategy.md",
    "test-assets/test-cases/activity-and-booknest-core-cases.md",
    "test-assets/bug-reports/sample-book-inventory-inconsistency.md",
    "test-assets/selenium/test_login_activity_book.py",
    "test-assets/selenium/requirements.txt",
    "test-assets/jmeter/campushub-activity-booknest-smoke.jmx",
    "test-assets/reports/selenium-latest.json",
    "test-assets/reports/jmeter-latest.jtl",
    "test-assets/postman/campushub-testing-lab.postman_collection.json",
]

TEXT_SUFFIXES = {".md", ".java", ".sql", ".yml", ".json", ".py", ".jmx", ".ts", ".vue", ".css", ".html", ".xml", ".txt"}
SKIP_DIRS = {"node_modules", "dist", "target", ".vite", ".git"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|cookie)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"[A-Z]:\\"),
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
]
ALLOWLIST_SNIPPETS = {
    'password": "campus123"',
    '"password":"campus123"',
    "password | `campus123`",
    "密码 | `campus123`",
}


def parse_jtl(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    with path.open(newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        if sample.lstrip().startswith("<"):
            tree = ET.parse(handle)
            total = 0
            failures = 0
            for item in tree.getroot().iter():
                if "t" in item.attrib:
                    total += 1
                    if item.attrib.get("s", "true").lower() == "false":
                        failures += 1
            return total, failures

        reader = csv.DictReader(handle)
        total = 0
        failures = 0
        for row in reader:
            total += 1
            if str(row.get("success", "true")).lower() == "false":
                failures += 1
        return total, failures


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            errors.append(f"missing required path: {rel}")

    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if rel == "scripts/check_release.py":
            continue
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"local absolute path found in {rel}")
        for pattern in SECRET_PATTERNS:
            for match in pattern.findall(text):
                if any(snippet in text for snippet in ALLOWLIST_SNIPPETS):
                    continue
                errors.append(f"possible secret pattern found in {rel}: {match}")

    try:
        ET.parse(ROOT / "test-assets/jmeter/campushub-activity-booknest-smoke.jmx")
    except ET.ParseError as exc:
        errors.append(f"jmeter xml parse failed: {exc}")

    postman_text = (ROOT / "test-assets/postman/campushub-testing-lab.postman_collection.json").read_text(encoding="utf-8")
    for endpoint in ["/v3/api-docs", "/api/auth/login", "/api/activities", "/api/rooms", "/api/devices", "/api/notifications", "/api/books", "/api/admin/review-tasks"]:
        if endpoint not in postman_text:
            errors.append(f"postman collection missing endpoint: {endpoint}")

    contract_text = (ROOT / "docs/api-contract.md").read_text(encoding="utf-8")
    for endpoint in ["/v3/api-docs", "/swagger-ui.html", "/api/auth/login", "/api/rooms", "/api/room-reservations", "/api/devices", "/api/device-borrows", "/api/notifications", "/api/book-borrows", "/api/admin/review-tasks"]:
        if endpoint not in contract_text:
            errors.append(f"api contract missing endpoint: {endpoint}")

    jtl_path = ROOT / "test-assets/reports/jmeter-latest.jtl"
    sample_count, failure_count = parse_jtl(jtl_path)
    if sample_count == 0:
        errors.append("jmeter report has no samples: test-assets/reports/jmeter-latest.jtl")
    if failure_count:
        errors.append(f"jmeter report contains failed samples: {failure_count}/{sample_count}")

    dashboard_path = ROOT / "frontend/src/assets/test-assets/test-dashboard.json"
    dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))
    dashboard_summary = dashboard.get("summary", {})
    dashboard_perf_status = dashboard.get("summary", {}).get("performanceStatus")
    expected_perf_status = "failed" if failure_count else "passed"
    if dashboard_perf_status != expected_perf_status:
        errors.append(f"dashboard performanceStatus mismatch: expected {expected_perf_status}, got {dashboard_perf_status}")
    if dashboard_summary.get("qualityGate") != "passed":
        errors.append(f"dashboard qualityGate is not passed: {dashboard_summary.get('qualityGate')}")
    for item in dashboard.get("automation", {}).get("screenshots", []):
        image_path = item.get("imagePath", "")
        if item.get("status") == "placeholder":
            errors.append(f"dashboard still uses placeholder screenshot: {item.get('id')}")
        if "placeholder" in image_path.lower():
            errors.append(f"dashboard screenshot path points to placeholder: {image_path}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("release check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
