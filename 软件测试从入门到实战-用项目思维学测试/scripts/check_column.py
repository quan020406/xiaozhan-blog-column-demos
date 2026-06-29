from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "case-project",
    "templates/article-template.md",
]

BANNED_EXAMPLES = [
    "买衣服",
    "女朋友",
    "邮箱注册",
    "百度",
    "五菱",
    "法拉利",
    "双十一",
]

ALLOWLIST_FILES = {
    "README.md",
    "docs/00-贯穿项目设定.md",
    "docs/csdn-publishing-checklist.md",
}
SKIP_DIRS = {
    "node_modules",
    "dist",
    "target",
    ".vite",
    ".git",
}


def main() -> int:
    errors = []

    for item in REQUIRED_PATHS:
        if not (ROOT / item).exists():
            errors.append(f"missing required path: {item}")

    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if rel.startswith(("articles/", "docs/")) or rel in ALLOWLIST_FILES:
            continue
        for word in BANNED_EXAMPLES:
            if word in text:
                errors.append(f"banned example '{word}' found in {rel}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("column check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
