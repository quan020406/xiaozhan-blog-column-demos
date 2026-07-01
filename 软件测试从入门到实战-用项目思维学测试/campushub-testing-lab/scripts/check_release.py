from pathlib import Path
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
    "docs/requirements.md",
    "docs/api-contract.md",
    "test-assets/test-cases/core-cases.md",
    "test-assets/bug-reports/sample-activity-registration-full.md",
    "test-assets/postman/campushub.postman_collection.json",
    "test-assets/known-defects.md",
    "test-assets/article-evidence-map.md",
    "test-assets/article-deliverables/03-24-method-tables.md",
    "test-assets/selenium/README.md",
    "test-assets/selenium/requirements.txt",
    "test-assets/selenium/pages.py",
    "test-assets/selenium/test_login_activity_book.py",
    "test-assets/jmeter/README.md",
    "test-assets/jmeter/campushub-activity-booknest-smoke.jmx",
    "scripts/run_performance_probe.py",
    "scripts/check_completion.py",
    "scripts/check_ui_smoke.py",
]

POSTMAN_REQUIRED_ENDPOINTS = [
    "/api/auth/login",
    "/api/activities",
    "/api/books",
    "/api/book-borrows",
    "/api/rooms",
    "/api/devices",
    "/api/notifications",
    "/api/admin/review-tasks",
    "/api/overview",
]

DELIVERABLE_EPISODES = ["03", "04", "05", "07", "10", "12", "13", "15", "16", "19", "24"]

REQUIREMENTS_REQUIRED_TERMS = [
    "登录",
    "活动报名",
    "BookNest",
    "我的记录",
    "管理员简表",
    "场地预约",
    "设备借用",
    "消息通知",
    "后台审核",
    "Selenium",
    "JMeter",
]

TEXT_SUFFIXES = {".md", ".java", ".sql", ".yml", ".json", ".py", ".ts", ".vue", ".css", ".html", ".xml", ".txt"}
SKIP_DIRS = {"node_modules", "dist", "target", ".vite", ".git"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|cookie)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)(?<![\w:-])password\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"[A-Z]:\\"),
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
]
OBSOLETE_REFERENCES = [
    "campushub-testing-lab.postman_collection.json",
    "frontend/src/assets/test-assets/test-dashboard.json",
    "generate_test_dashboard.py",
    "activity-and-booknest-core-cases.md",
    "core-lite-cases.md",
    "campushub-lite.postman_collection.json",
]
ALLOWLIST_SNIPPETS = {
    'password": "campus123"',
    '"password":"campus123"',
    "password | `campus123`",
    "密码 | `campus123`",
    "`student01 / campus123`",
    "`admin01 / campus123`",
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
        if rel in {"scripts/check_release.py", "scripts/check_completion.py"}:
            continue
        for obsolete in OBSOLETE_REFERENCES:
            if obsolete in text:
                errors.append(f"obsolete removed asset reference found in {rel}: {obsolete}")
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"local absolute path found in {rel}")
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                if any(snippet in text for snippet in ALLOWLIST_SNIPPETS):
                    continue
                errors.append(f"possible secret pattern found in {rel}: {match.group(0).strip()}")

    requirements_text = (ROOT / "docs/requirements.md").read_text(encoding="utf-8")
    for term in REQUIREMENTS_REQUIRED_TERMS:
        if term not in requirements_text:
            errors.append(f"requirements missing required term: {term}")

    postman_path = ROOT / "test-assets/postman/campushub.postman_collection.json"
    try:
        postman_data = json.loads(postman_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"postman collection json parse failed: {exc}")
        postman_text = ""
    else:
        postman_text = json.dumps(postman_data, ensure_ascii=False)

    for endpoint in POSTMAN_REQUIRED_ENDPOINTS:
        if endpoint not in postman_text:
            errors.append(f"postman collection missing endpoint: {endpoint}")

    api_contract_text = (ROOT / "docs/api-contract.md").read_text(encoding="utf-8")
    if "campushub-testing-lab.postman_collection.json" in api_contract_text:
        errors.append("api contract still references removed postman collection name")

    try:
        ET.parse(ROOT / "test-assets/jmeter/campushub-activity-booknest-smoke.jmx")
    except ET.ParseError as exc:
        errors.append(f"jmeter xml parse failed: {exc}")

    evidence_text = (ROOT / "test-assets/article-evidence-map.md").read_text(encoding="utf-8")
    for episode in range(1, 27):
        marker = f"| {episode:02d} |"
        if marker not in evidence_text:
            errors.append(f"article evidence map missing episode: {episode:02d}")
    if "待补专表" in evidence_text:
        errors.append("article evidence map still contains pending method table marker: 待补专表")

    deliverables_text = (ROOT / "test-assets/article-deliverables/03-24-method-tables.md").read_text(encoding="utf-8")
    for episode in DELIVERABLE_EPISODES:
        if f"## {episode} " not in deliverables_text:
            errors.append(f"method tables missing episode section: {episode}")

    selenium_text = (ROOT / "test-assets/selenium/test_login_activity_book.py").read_text(encoding="utf-8")
    pages_text = (ROOT / "test-assets/selenium/pages.py").read_text(encoding="utf-8")
    if "CampusHubPage" not in selenium_text or "class CampusHubPage" not in pages_text:
        errors.append("selenium smoke test must use CampusHubPage page object")

    jmeter_text = (ROOT / "test-assets/jmeter/campushub-activity-booknest-smoke.jmx").read_text(encoding="utf-8")
    for required in ["/api/auth/login", "JSONPostProcessor", "authToken", "/api/activities/${ACTIVITY_ID}/registrations"]:
        if required not in jmeter_text:
            errors.append(f"jmeter plan missing login/session chain marker: {required}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("release check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
