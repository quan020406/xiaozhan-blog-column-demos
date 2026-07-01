from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
COLUMN_ROOT = ROOT.parent

PRD_REQUIREMENT_IDS = [
    "L-001", "L-002", "L-003", "L-004", "L-005", "L-006",
    "A-001", "A-002", "A-003", "A-004", "A-005", "A-006",
    "B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007",
    "R-001", "R-002", "R-003", "R-004",
    "D-001", "D-002", "D-003", "D-004",
    "N-001", "N-002", "N-003",
    "AD-001", "AD-002", "AD-003", "AD-004",
]

NAV_LABELS = ["活动列表", "图书列表", "场地预约", "设备借用", "消息通知", "我的记录", "管理员入口", "测试素材"]

FRONTEND_TEST_IDS = [
    "service-status",
    "login-username",
    "login-password",
    "login-submit",
    "register-activity",
    "book-keyword",
    "book-search",
    "borrow-book",
    "room-date",
    "reserve-room",
    "device-borrow-date",
    "device-due-date",
    "borrow-device",
    "read-notification",
    "renew-book",
    "return-book",
    "approve-task",
]

API_FRAGMENTS = [
    "/api/overview",
    "/api/auth/login",
    "/api/activities",
    "/registrations",
    "/api/books",
    "/api/book-borrows",
    "/api/rooms",
    "/api/room-reservations",
    "/api/devices",
    "/api/device-borrows",
    "/api/notifications",
    "/api/admin/review-tasks",
]

POSTMAN_ENDPOINTS = [
    "/api/auth/login",
    "/api/activities",
    "/api/books",
    "/api/book-borrows",
    "/api/rooms",
    "/api/room-reservations",
    "/api/devices",
    "/api/device-borrows",
    "/api/notifications",
    "/api/admin/review-tasks",
    "/api/overview",
]

TEST_CASE_IDS = [f"CHL-TC-{index:03d}" for index in range(1, 30)]

METHOD_TABLE_EPISODES = ["03", "04", "05", "07", "10", "12", "13", "15", "16", "19", "24"]

REMOVED_REFERENCES = [
    "frontend/src/assets/test-assets/test-dashboard.json",
    "generate_test_dashboard.py",
    "activity-and-booknest-core-cases.md",
    "core-lite-cases.md",
    "campushub-lite.postman_collection.json",
]


def main() -> int:
    errors: list[str] = []

    prd_text = read(COLUMN_ROOT / "docs/07-CampusHub-Lite-PRD.md")
    requirements_text = read(ROOT / "docs/requirements.md")
    for requirement_id in PRD_REQUIREMENT_IDS:
        if requirement_id not in prd_text:
            errors.append(f"PRD missing requirement id: {requirement_id}")
        if requirement_id not in requirements_text:
            errors.append(f"requirements missing requirement id: {requirement_id}")

    app_text = read(ROOT / "frontend/src/App.vue")
    api_text = read(ROOT / "frontend/src/composables/useCampusHubApi.ts")
    for label in NAV_LABELS:
        if label not in app_text:
            errors.append(f"frontend missing nav label: {label}")
    for test_id in FRONTEND_TEST_IDS:
        if f'data-testid="{test_id}"' not in app_text and f"data-testid='{test_id}'" not in app_text:
            errors.append(f"frontend missing data-testid: {test_id}")
    for fragment in API_FRAGMENTS:
        if fragment not in api_text:
            errors.append(f"frontend API layer missing endpoint fragment: {fragment}")

    cases_text = read(ROOT / "test-assets/test-cases/core-cases.md")
    for test_case_id in TEST_CASE_IDS:
        if test_case_id not in cases_text:
            errors.append(f"manual test cases missing id: {test_case_id}")

    postman_text = json.dumps(json.loads(read(ROOT / "test-assets/postman/campushub.postman_collection.json")), ensure_ascii=False)
    for endpoint in POSTMAN_ENDPOINTS:
        if endpoint not in postman_text:
            errors.append(f"postman missing endpoint: {endpoint}")

    evidence_text = read(ROOT / "test-assets/article-evidence-map.md")
    for episode in range(1, 27):
        if f"| {episode:02d} |" not in evidence_text:
            errors.append(f"article evidence map missing episode: {episode:02d}")
    if "当前缺口" in evidence_text or "待补" in evidence_text:
        errors.append("article evidence map still contains gap marker")

    method_tables_text = read(ROOT / "test-assets/article-deliverables/03-24-method-tables.md")
    for episode in METHOD_TABLE_EPISODES:
        if f"## {episode} " not in method_tables_text:
            errors.append(f"method tables missing episode: {episode}")

    ET.parse(ROOT / "test-assets/jmeter/campushub-activity-booknest-smoke.jmx")
    selenium_text = read(ROOT / "test-assets/selenium/test_login_activity_book.py")
    if "CampusHubPage" not in selenium_text:
        errors.append("selenium smoke test does not use page object")
    ui_smoke_text = read(ROOT / "scripts/check_ui_smoke.py")
    for label in NAV_LABELS:
        if label not in ui_smoke_text:
            errors.append(f"ui smoke script missing nav label: {label}")
    if "sync_playwright" not in ui_smoke_text:
        errors.append("ui smoke script must use Playwright")

    searchable_paths = [
        COLUMN_ROOT / "README.md",
        COLUMN_ROOT / "docs",
        ROOT / "README.md",
        ROOT / "docs",
        ROOT / "scripts",
        ROOT / "test-assets",
    ]
    for path in iter_text_files(searchable_paths):
        text = read(path)
        if path.name in {"check_completion.py", "check_release.py"}:
            continue
        for removed in REMOVED_REFERENCES:
            if removed in text:
                rel = path.relative_to(COLUMN_ROOT).as_posix()
                errors.append(f"removed asset reference found in {rel}: {removed}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("completion check passed")
    return 0


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_text_files(paths: list[Path]):
    suffixes = {".md", ".py", ".json", ".ts", ".vue", ".xml", ".txt"}
    skip_parts = {"node_modules", "dist", "target", ".git", ".vite"}
    for path in paths:
        if path.is_file() and path.suffix.lower() in suffixes:
            yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if any(part in skip_parts for part in child.parts):
                    continue
                if child.is_file() and child.suffix.lower() in suffixes:
                    yield child


if __name__ == "__main__":
    sys.exit(main())
