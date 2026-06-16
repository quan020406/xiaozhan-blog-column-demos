from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai_firm"))

from cheat_detector import scan

findings = scan(Path(__file__).resolve().parents[1])
if findings:
    print("\n".join(findings))
    raise SystemExit(1)
print("Integrity audit passed.")

