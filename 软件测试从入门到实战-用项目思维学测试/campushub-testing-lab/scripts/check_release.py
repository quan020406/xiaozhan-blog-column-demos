from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    ".gitignore",
    "backend/pom.xml",
    "frontend/package.json",
    "test-assets/test-cases/activity-and-booknest-core-cases.md",
    "test-assets/bug-reports/sample-book-inventory-inconsistency.md",
    "test-assets/selenium/test_login_activity_book.py",
    "test-assets/selenium/requirements.txt",
    "test-assets/jmeter/campushub-activity-booknest-smoke.jmx",
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
    "password\": \"campus123\"",
    "\"password\":\"campus123\"",
    "password | `campus123`",
    "密码 | `campus123`",
}


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

    if errors:
        for error in errors:
            print(error)
        return 1

    print("release check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
