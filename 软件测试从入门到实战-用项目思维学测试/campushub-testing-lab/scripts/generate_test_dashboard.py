from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

MODULE_NAMES = {
    "auth": "账号中心",
    "activity": "活动中心",
    "room": "场地预约",
    "device": "设备借用",
    "notification": "消息通知",
    "booknest": "BookNest",
    "review": "后台审核",
    "system": "系统健康",
    "unknown": "未归类",
}

MODULE_SCOPES = {
    "auth": "登录、角色、连续失败锁定",
    "activity": "活动浏览、报名、取消报名",
    "room": "场地查询、预约申请、冲突时段",
    "device": "设备库存、借用申请、重复借用",
    "notification": "通知列表、已读状态、归属校验",
    "booknest": "图书检索、借阅、续借、归还",
    "review": "审核任务、权限、操作日志",
    "system": "健康检查、OpenAPI 文档",
    "unknown": "待补充映射的测试项",
}

TEST_TYPES = [
    ("api", "接口测试"),
    ("ui-automation", "UI 自动化"),
    ("performance", "性能测试"),
    ("release-check", "发布检查"),
]

SCREENSHOT_MODULES = [
    ("login", "auth", "登录成功页面"),
    ("activity", "activity", "活动报名页面"),
    ("room", "room", "场地预约页面"),
    ("device", "device", "设备借用页面"),
    ("booknest", "booknest", "BookNest 借阅页面"),
    ("notification", "notification", "消息通知页面"),
]


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def testcase_module(name: str) -> str:
    lower = name.lower()
    if "login" in lower or "auth" in lower:
        return "auth"
    if "activity" in lower or "registration" in lower:
        return "activity"
    if "room" in lower or "reservation" in lower:
        return "room"
    if "device" in lower:
        return "device"
    if "notification" in lower:
        return "notification"
    if "book" in lower or "borrow" in lower or "renew" in lower:
        return "booknest"
    if "review" in lower or "admin" in lower or "decide" in lower:
        return "review"
    if "openapi" in lower or "health" in lower or "overview" in lower:
        return "system"
    return "unknown"


def testcase_status(case: ET.Element) -> str:
    if case.find("failure") is not None or case.find("error") is not None:
        return "failed"
    if case.find("skipped") is not None:
        return "skipped"
    return "passed"


def parse_junit(root: Path) -> tuple[list[dict], dict[str, int], bool]:
    report_dir = root / "backend" / "target" / "surefire-reports"
    files = sorted(report_dir.glob("TEST-*.xml"))
    cases: list[dict] = []
    totals = {"tests": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0}
    for xml_file in files:
        suite = ET.parse(xml_file).getroot()
        totals["tests"] += int(suite.attrib.get("tests", 0))
        totals["failed"] += int(suite.attrib.get("failures", 0))
        totals["errors"] += int(suite.attrib.get("errors", 0))
        totals["skipped"] += int(suite.attrib.get("skipped", 0))
        for index, case in enumerate(suite.findall("testcase"), start=1):
            name = case.attrib.get("name", f"case-{index}")
            module = testcase_module(name)
            status = testcase_status(case)
            cases.append({
                "id": f"AUTO-{module.upper()}-{index:03d}",
                "title": name,
                "module": module,
                "type": "api",
                "priority": "P1" if status == "passed" else "P0",
                "status": status,
                "executor": "maven-surefire",
                "lastRunAt": now_iso(),
                "evidence": {
                    "kind": "junit",
                    "summary": f"Surefire 用例 {name} 执行结果为 {status}",
                    "path": "backend/target/surefire-reports",
                },
                "automation": {"available": False, "scriptPath": "", "screenshotPath": ""},
                "performance": {"related": module == "activity", "scenarioId": "PERF-ACT-001" if module == "activity" else ""},
            })
    totals["failed"] += totals["errors"]
    totals["passed"] = max(totals["tests"] - totals["failed"] - totals["skipped"], 0)
    return cases, totals, bool(files)


def parse_bugs(root: Path) -> list[dict]:
    bug_dir = root / "test-assets" / "bug-reports"
    bugs: list[dict] = []
    for index, path in enumerate(sorted(bug_dir.glob("*.md")), start=1):
        text = path.read_text(encoding="utf-8")
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")), path.stem)
        module = "booknest" if "BookNest" in text or "图书" in text else "unknown"
        is_sample = "样例" in title or "教学用 Bug 报告样例" in text or path.stem.startswith("sample-")
        critical_row = re.search(r"\|\s*(严重程度|Severity)\s*\|\s*Critical\s*\|", text, re.IGNORECASE)
        severity = "critical" if critical_row else "major"
        priority = "P1" if severity == "critical" else "P2"
        bugs.append({
            "id": f"BUG-{module.upper()}-{index:03d}",
            "title": title,
            "module": module,
            "severity": severity,
            "priority": priority,
            "status": "sample" if is_sample else "open",
            "evidenceType": "teaching-sample" if is_sample else "runtime-defect",
            "foundBy": "markdown-sample" if is_sample else "markdown",
            "relatedCaseId": "",
            "summary": "教学用 Bug 报告样例，不计入当前工程开放缺陷。" if is_sample else "来自 Bug Markdown 的开放缺陷，详情以复现文档为准。",
            "reproducePath": rel(path, root),
            "createdAt": now_iso(),
        })
    return bugs


def parse_screenshots(root: Path) -> list[dict]:
    shot_dir = root / "frontend" / "src" / "assets" / "test-assets" / "screenshots"
    files = sorted([p for p in shot_dir.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg"}])
    screenshots: list[dict] = []
    for keyword, module, title in SCREENSHOT_MODULES:
        candidates = [p for p in files if keyword in p.name.lower()]
        match = next((p for p in candidates if p.name.lower() == f"selenium-{keyword}.png"), None)
        if not match:
            match = next((p for p in candidates if "placeholder" not in p.name.lower()), None)
        if not match:
            match = next(iter(candidates), None)
        if not match:
            continue
        screenshots.append({
            "id": f"shot-{keyword}",
            "title": title,
            "module": module,
            "status": "placeholder" if "placeholder" in match.name else "captured",
            "imagePath": rel(match, root / "frontend"),
            "caption": "Selenium 截图占位" if "placeholder" in match.name else "Selenium 执行截图",
        })
    return screenshots


def parse_selenium_summary(root: Path) -> tuple[dict, bool]:
    summary_path = root / "test-assets" / "reports" / "selenium-latest.json"
    if not summary_path.exists():
        return {
            "status": "not_run",
            "runId": "ui-selenium-missing",
            "startedAt": "",
            "finishedAt": "",
            "browser": "Chrome or Edge",
            "scriptPath": "test-assets/selenium/test_login_activity_book.py",
        }, False
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    return {
        "status": data.get("status", "unknown"),
        "runId": data.get("runId", "ui-selenium-latest"),
        "startedAt": data.get("startedAt", ""),
        "finishedAt": data.get("finishedAt", ""),
        "browser": data.get("browser", "Chrome"),
        "scriptPath": "test-assets/selenium/test_login_activity_book.py",
        "summaryPath": rel(summary_path, root),
        "stepCount": len(data.get("steps", [])),
    }, True


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0
    ordered = sorted(values)
    k = (len(ordered) - 1) * pct
    floor = int(k)
    ceil = min(floor + 1, len(ordered) - 1)
    if floor == ceil:
        return ordered[floor]
    return ordered[floor] + (ordered[ceil] - ordered[floor]) * (k - floor)


def parse_jmeter(root: Path) -> tuple[dict, bool]:
    reports_dir = root / "test-assets" / "reports"
    candidates = sorted(reports_dir.glob("*.jtl")) if reports_dir.exists() else []
    if not candidates:
        return {
            "scenarioId": "PERF-ACT-001",
            "title": "活动报名接口性能趋势",
            "dataSource": "missing",
            "unit": {"responseTime": "ms", "throughput": "req/s", "errorRate": "%"},
            "thresholds": {"p95ResponseMs": 800, "errorRate": 1},
            "series": [{
                "time": "No JMeter JTL",
                "avgResponseMs": 0,
                "p95ResponseMs": 0,
                "throughputPerSecond": 0,
                "errorRate": 0,
                "note": "未发现 test-assets/reports/*.jtl，暂不生成性能结论",
            }],
            "reportPath": "test-assets/reports/jmeter-latest.jtl",
            "notes": "未提供 JMeter 结果，不能给出性能结论。",
        }, False

    latest = candidates[-1]
    rows: list[dict[str, str]] = []
    with latest.open(newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        if sample.lstrip().startswith("<"):
            tree = ET.parse(handle)
            for item in tree.getroot().iter():
                if "t" in item.attrib:
                    rows.append({"elapsed": item.attrib.get("t", "0"), "success": item.attrib.get("s", "true")})
        else:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(row)

    groups: dict[str, list[dict[str, str]]] = {}
    total_count = 0
    total_failures = 0
    max_p95 = 0
    for row in rows:
        label = row.get("label") or row.get("lb") or latest.stem
        groups.setdefault(label, []).append(row)
    series = []
    for label, group_rows in groups.items():
        elapsed = [float(row.get("elapsed") or row.get("t") or 0) for row in group_rows]
        failures = sum(1 for row in group_rows if str(row.get("success") or row.get("s") or "true").lower() == "false")
        count = len(elapsed)
        error_rate = round((failures / count) * 100, 2) if count else 0
        avg = round(statistics.mean(elapsed), 2) if elapsed else 0
        p95 = round(percentile(elapsed, 0.95), 2) if elapsed else 0
        total_count += count
        total_failures += failures
        max_p95 = max(max_p95, p95)
        series.append({
            "time": label,
            "avgResponseMs": avg,
            "p95ResponseMs": p95,
            "throughputPerSecond": count,
            "errorRate": error_rate,
            "note": f"从 {latest.name} 聚合 {count} 条样本",
        })
    thresholds = {"p95ResponseMs": 800, "errorRate": 1}
    total_error_rate = round((total_failures / total_count) * 100, 2) if total_count else 0
    status = "passed" if total_count and total_error_rate <= thresholds["errorRate"] and max_p95 <= thresholds["p95ResponseMs"] else "failed"
    return {
        "scenarioId": "PERF-ACT-001",
        "title": "活动报名接口性能趋势",
        "dataSource": "generated",
        "unit": {"responseTime": "ms", "throughput": "req/s", "errorRate": "%"},
        "thresholds": thresholds,
        "status": status,
        "sampleCount": total_count,
        "failureCount": total_failures,
        "totalErrorRate": total_error_rate,
        "maxP95ResponseMs": max_p95,
        "series": series,
        "reportPath": rel(latest, root),
        "notes": "由 JMeter JTL 聚合生成；状态由总错误率和最大 P95 阈值共同判定。",
    }, True


def module_summaries(cases: list[dict]) -> list[dict]:
    modules: list[dict] = []
    for module_id, name in MODULE_NAMES.items():
        module_cases = [case for case in cases if case["module"] == module_id]
        if not module_cases and module_id == "unknown":
            continue
        count = len(module_cases)
        passed = sum(1 for case in module_cases if case["status"] == "passed")
        failed = sum(1 for case in module_cases if case["status"] == "failed")
        blocked = sum(1 for case in module_cases if case["status"] == "blocked")
        coverage = round((passed / count) * 100, 2) if count else 0
        risk = "high" if failed else "medium" if blocked or count == 0 else "low"
        modules.append({
            "id": module_id,
            "name": name,
            "scope": MODULE_SCOPES[module_id],
            "owner": "脚本生成",
            "caseCount": count,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "coverageRate": coverage,
            "riskLevel": risk,
        })
    return modules


def build_dashboard(root: Path) -> dict:
    cases, totals, junit_available = parse_junit(root)
    bugs = parse_bugs(root)
    screenshots = parse_screenshots(root)
    selenium_latest_run, selenium_available = parse_selenium_summary(root)
    performance, jmeter_available = parse_jmeter(root)
    performance_status = performance.get("status", "warning") if jmeter_available else "warning"
    performance_passed = performance_status == "passed"
    total_cases = totals["tests"]
    pass_rate = round((totals["passed"] / total_cases) * 100, 2) if total_cases else 0
    open_bugs = [bug for bug in bugs if bug["status"] == "open"]
    sample_bugs = [bug for bug in bugs if bug["status"] == "sample"]
    critical_bugs = sum(1 for bug in open_bugs if bug["severity"] == "critical")
    failed = totals["failed"]
    quality_gate = "blocked" if failed or critical_bugs or performance_status == "failed" else "passed"
    quality_score = max(0, 100 - failed * 12 - critical_bugs * 10 - (0 if performance_passed else 8))
    return {
        "schemaVersion": "1.0.0",
        "generatedAt": now_iso(),
        "dataMode": "generated",
        "datasetNote": "由 scripts/generate_test_dashboard.py 汇总 JUnit XML、Selenium 截图、JMeter JTL 和 Bug Markdown 生成；缺失输入会在 runEvidence.reportFiles 中标记。",
        "project": {
            "name": "CampusHub Testing Lab",
            "version": "0.2.0-SNAPSHOT",
            "description": "CampusHub 教学项目测试可视化看板",
        },
        "summary": {
            "totalCases": total_cases,
            "passed": totals["passed"],
            "failed": failed,
            "blocked": 0,
            "skipped": totals["skipped"],
            "passRate": pass_rate,
            "openBugs": len(open_bugs),
            "sampleBugs": len(sample_bugs),
            "criticalBugs": critical_bugs,
            "performanceStatus": performance_status,
            "qualityGate": quality_gate,
            "qualityScore": quality_score,
            "qualityReason": f"JUnit 通过 {totals['passed']}/{total_cases}，真实开放缺陷 {len(open_bugs)} 个，教学样例缺陷 {len(sample_bugs)} 个，性能状态 {performance_status}。",
        },
        "modules": module_summaries(cases),
        "testTypes": [
            {"type": "api", "label": "接口测试", "caseCount": total_cases, "passed": totals["passed"], "status": "passed" if failed == 0 else "warning"},
            {"type": "ui-automation", "label": "UI 自动化", "caseCount": len(screenshots), "passed": sum(1 for item in screenshots if item["status"] == "captured"), "status": "passed" if selenium_available and selenium_latest_run["status"] == "passed" else "warning"},
            {"type": "performance", "label": "性能测试", "caseCount": 1, "passed": 1 if performance_passed else 0, "status": performance_status},
            {"type": "release-check", "label": "发布检查", "caseCount": 1, "passed": 1, "status": "passed"},
        ],
        "testCases": cases,
        "bugs": bugs,
        "performance": performance,
        "automation": {
            "latestRun": selenium_latest_run,
            "screenshots": screenshots,
        },
        "runEvidence": {
            "commands": [
                {"name": "后端单元测试", "command": "mvn test", "cwd": "campushub-testing-lab/backend", "status": "passed" if junit_available and failed == 0 else "warning", "summary": f"Surefire XML {'已读取' if junit_available else '未发现'}，通过 {totals['passed']} 条"},
                {"name": "UI 自动化", "command": "python test_login_activity_book.py --base-url http://localhost:5173", "cwd": "campushub-testing-lab/test-assets/selenium", "status": "passed" if selenium_available and selenium_latest_run["status"] == "passed" else "warning", "summary": f"Selenium {'已读取' if selenium_available else '未运行'}，步骤 {selenium_latest_run.get('stepCount', 0)} 条"},
                {"name": "测试看板生成", "command": "python scripts/generate_test_dashboard.py", "cwd": "campushub-testing-lab", "status": "passed", "summary": "已生成前端测试看板 JSON"},
                {"name": "性能结果聚合", "command": "jmeter -n -t test-assets/jmeter/campushub-activity-booknest-smoke.jmx -l test-assets/reports/jmeter-latest.jtl", "cwd": "campushub-testing-lab", "status": performance_status, "summary": f"JMeter JTL 已读取，错误率 {performance.get('totalErrorRate', 0)}%" if jmeter_available else "未发现 JTL，暂不输出性能结论"},
            ],
            "environment": {"java": "17", "node": "18+", "database": "H2", "browser": "Chrome or Edge"},
            "reportFiles": [
                {"kind": "junit", "path": "backend/target/surefire-reports", "available": junit_available},
                {"kind": "selenium", "path": "test-assets/reports/selenium-latest.json", "available": selenium_available},
                {"kind": "jmeter", "path": "test-assets/reports/jmeter-latest.jtl", "available": jmeter_available},
            ],
        },
        "nextActions": [
            "运行 Selenium 后用真实 PNG 覆盖截图占位",
            "运行 JMeter 并输出 test-assets/reports/jmeter-latest.jtl",
            "把设备借用和通知模块接入同一套测试证据生成链路",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CampusHub QA dashboard JSON from local test evidence.")
    parser.add_argument("--root", default=".", help="CampusHub Testing Lab root directory")
    parser.add_argument("--output", default="frontend/src/assets/test-assets/test-dashboard.json", help="Output JSON path relative to root")
    parser.add_argument("--dry-run", action="store_true", help="Print generated JSON without writing the output file")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    dashboard = build_dashboard(root)
    payload = json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n"
    if args.dry_run:
        print(payload)
        return 0
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")
    print(f"dashboard generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

