from __future__ import annotations

import argparse
import json
import re
from collections import deque
from pathlib import Path

IMPORT_PATTERN = re.compile(r"^import\s+([\w.]+);", re.MULTILINE)


class JavaContextPruner:
    def __init__(self, source_root: Path, max_depth: int = 2) -> None:
        self.source_root = source_root.resolve()
        self.max_depth = max_depth

    def prune(self, target: Path) -> dict[str, object]:
        target = target.resolve()
        if self.source_root not in target.parents:
            raise ValueError(f"target must be inside {self.source_root}")

        queue: deque[tuple[Path, int]] = deque([(target, 0)])
        visited: set[Path] = set()
        files: list[dict[str, object]] = []

        while queue:
            path, depth = queue.popleft()
            if path in visited or not path.exists():
                continue
            visited.add(path)
            content = path.read_text(encoding="utf-8")
            files.append({
                "path": str(path.relative_to(self.source_root)),
                "depth": depth,
                "characters": len(content),
                "content": content,
            })
            if depth >= self.max_depth:
                continue
            for imported in IMPORT_PATTERN.findall(content):
                candidate = self.source_root / (imported.replace(".", "/") + ".java")
                if candidate.exists():
                    queue.append((candidate, depth + 1))

        return {
            "target": str(target.relative_to(self.source_root)),
            "file_count": len(files),
            "character_count": sum(int(item["characters"]) for item in files),
            "files": files,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a bounded Java context bundle")
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--source-root", type=Path, default=Path("src/main/java"))
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = JavaContextPruner(args.source_root, args.max_depth).prune(args.target)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()

