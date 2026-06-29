from __future__ import annotations

import shutil
import subprocess
import sys


CHECKS = [
    ("Java", "java", ["-version"], 17),
    ("Maven", "mvn", ["-version"], None),
    ("Node.js", "node", ["--version"], 18),
    ("npm", "npm", ["--version"], 9),
    ("Python", "python", ["--version"], 3),
]


def first_line(executable_path: str, args: list[str]) -> str:
    try:
        result = subprocess.run([executable_path, *args], capture_output=True, text=True, timeout=10)
    except Exception as exc:
        return f"unable to run: {exc.__class__.__name__}"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else "available"


def major_version(text: str) -> int | None:
    for token in text.replace('"', " ").replace("v", " ").split():
        head = token.split(".", 1)[0]
        if head.isdigit():
            return int(head)
    return None


def main() -> int:
    print("CampusHub Testing Lab local environment check")
    print()
    missing: list[str] = []
    warnings: list[str] = []
    for name, executable, args, minimum_major in CHECKS:
        executable_path = shutil.which(executable)
        if not executable_path:
            print(f"[MISSING] {name}: command not found ({executable})")
            missing.append(name)
            continue

        version_text = first_line(executable_path, args)
        found_major = major_version(version_text)
        if minimum_major and found_major is not None and found_major < minimum_major:
            print(f"[WARN] {name}: {version_text} (recommended >= {minimum_major})")
            warnings.append(name)
        else:
            print(f"[OK] {name}: {version_text}")

    print()
    if missing:
        print("Missing tools:", ", ".join(missing))
        print("Install the missing tools first, then run this script again.")
        return 1
    if warnings:
        print("Warnings:", ", ".join(warnings))
        print("These tools are available, but the project recommends newer versions.")
        print()

    print("Next steps:")
    print("1. cd backend && mvn spring-boot:run")
    print("2. cd frontend && npm install && npm run dev")
    print("3. Open http://localhost:5173 and log in with student01 / campus123")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
