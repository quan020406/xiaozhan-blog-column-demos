from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "images"
W, H = 1600, 900

FONT_CANDIDATES = (
    ("Noto Sans SC (TrueType).otf", "Noto Sans SC Bold (TrueType).otf"),
    ("NotoSansSC-VF.ttf", "NotoSansSC-VF.ttf"),
    ("msyh.ttc", "msyhbd.ttc"),
    ("simhei.ttf", "simhei.ttf"),
)


def font_dirs() -> list[Path]:
    roots = [
        Path.home() / ".fonts",
        Path("/usr/share/fonts"),
        Path("/Library/Fonts"),
    ]
    system_root = os.environ.get("SystemRoot")
    if system_root:
        roots.append(Path(system_root) / "Fonts")
    return roots


def find_font(name: str) -> Path | None:
    for root in font_dirs():
        path = root / name
        if path.exists():
            return path
    return None


def select_fonts() -> tuple[Path | None, Path | None]:
    for regular, bold in FONT_CANDIDATES:
        regular_path = find_font(regular)
        bold_path = find_font(bold)
        if regular_path and bold_path:
            return regular_path, bold_path
    return None, None


FONT_REGULAR, FONT_BOLD = select_fonts()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    selected = FONT_BOLD if bold else FONT_REGULAR
    if selected:
        return ImageFont.truetype(str(selected), size)
    return ImageFont.load_default(size=size)


def label(draw: ImageDraw.ImageDraw, xy, text: str, size=30, fill="#111827", bold=False, anchor="mm"):
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(draw: ImageDraw.ImageDraw, box, radius=22, fill="#ffffff", outline="#cbd5e1", width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill="#475569", width=5):
    draw.line([start, end], fill=fill, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        sign = 1 if ex > sx else -1
        pts = [(ex, ey), (ex - sign * 24, ey - 14), (ex - sign * 24, ey + 14)]
    else:
        sign = 1 if ey > sy else -1
        pts = [(ex, ey), (ex - 14, ey - sign * 24), (ex + 14, ey - sign * 24)]
    draw.polygon(pts, fill=fill)


def base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#f6f8fb")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 132), fill="#111827")
    draw.rectangle((0, 132, W, 138), fill="#0ea5e9")
    label(draw, (80, 54), title, 42, "#ffffff", True, "la")
    label(draw, (80, 100), subtitle, 24, "#cbd5e1", False, "la")
    return img, draw


def task_unit_image() -> None:
    img, draw = base("Agent 可安全执行的任务单元", "把“帮我改一下”改成边界、上下文和验收都明确的工作包")

    rounded(draw, (95, 220, 455, 680), 28, "#dbeafe", "#2563eb", 3)
    label(draw, (275, 280), "任务输入", 36, "#2563eb", True)
    for i, item in enumerate(["issue.md", "context.json", "allowed-files.txt", "constraints.md", "verify.ps1"]):
        y = 350 + i * 55
        rounded(draw, (145, y, 405, y + 38), 10, "#ffffff", "#bfdbfe", 2)
        label(draw, (275, y + 21), item, 24, "#1e3a8a", False)

    rounded(draw, (620, 235, 980, 665), 28, "#fef3c7", "#d97706", 3)
    label(draw, (800, 298), "Agent 执行", 36, "#d97706", True)
    label(draw, (800, 380), "只读必要上下文", 27, "#374151")
    label(draw, (800, 442), "只改允许文件", 27, "#374151")
    label(draw, (800, 504), "不改验收标准", 27, "#374151")
    label(draw, (800, 566), "输出可审计 diff", 27, "#374151")

    rounded(draw, (1145, 220, 1505, 680), 28, "#dcfce7", "#16a34a", 3)
    label(draw, (1325, 280), "验收输出", 36, "#16a34a", True)
    for i, item in enumerate(["mvn test", "integrity audit", "stress test", "business invariants", "human review"]):
        y = 350 + i * 55
        rounded(draw, (1195, y, 1455, y + 38), 10, "#ffffff", "#bbf7d0", 2)
        label(draw, (1325, y + 21), item, 24, "#14532d", False)

    arrow(draw, (480, 450), (590, 450), "#475569", 7)
    arrow(draw, (1010, 450), (1120, 450), "#475569", 7)

    rounded(draw, (240, 735, 1360, 815), 18, "#ffffff", "#cbd5e1", 2)
    label(draw, (800, 776), "核心：Agent 可以高吞吐执行，但边界和验收不能由 Agent 临时解释", 31, "#111827", True)

    img.save(OUT_DIR / "article-04-architecture.png", quality=95)


def components_image() -> None:
    img, draw = base("从大 Service 到 Agent 友好组件", "拆分不是为了抽象漂亮，而是为了缩小阅读范围、修改范围和 Review 范围")

    rounded(draw, (95, 260, 435, 625), 28, "#fee2e2", "#dc2626", 3)
    label(draw, (265, 326), "万能 Service", 36, "#dc2626", True)
    for i, item in enumerate(["库存", "订单", "Redis 锁", "响应", "日志"]):
        label(draw, (265, 395 + i * 42), item, 28, "#374151")
    label(draw, (265, 585), "误改面大", 30, "#991b1b", True)

    arrow(draw, (470, 445), (590, 445), "#475569", 7)

    boxes = [
        (640, 210, 980, 330, "AtomicSeckillService", "编排任务入口", "#dbeafe", "#2563eb"),
        (1090, 210, 1430, 330, "SeckillProductMapper", "stock > 0 不变量", "#dcfce7", "#16a34a"),
        (640, 520, 980, 640, "OrderCreator", "订单副作用", "#fef3c7", "#d97706"),
        (1090, 520, 1430, 640, "SeckillResult", "响应契约", "#ede9fe", "#7c3aed"),
    ]
    for x1, y1, x2, y2, title, desc, bg, accent in boxes:
        rounded(draw, (x1, y1, x2, y2), 22, bg, accent, 3)
        label(draw, ((x1 + x2) // 2, y1 + 45), title, 27 if len(title) < 18 else 24, accent, True)
        label(draw, ((x1 + x2) // 2, y1 + 88), desc, 24, "#374151")

    arrow(draw, (810, 330), (810, 510), "#2563eb", 5)
    arrow(draw, (980, 270), (1085, 270), "#475569", 5)
    arrow(draw, (980, 580), (1085, 580), "#475569", 5)
    arrow(draw, (1260, 330), (1260, 510), "#16a34a", 5)

    rounded(draw, (610, 715, 1460, 815), 18, "#ffffff", "#cbd5e1", 2)
    label(draw, (1035, 755), "Agent 任务包只需携带相关组件，不必暴露整个 Web 层和 CI 规则", 29, "#111827", True)
    label(draw, (1035, 792), "允许修改范围越小，验收和 Review 越清楚", 24, "#475569")

    img.save(OUT_DIR / "article-04-solid-components.png", quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    task_unit_image()
    components_image()
    print(OUT_DIR / "article-04-architecture.png")
    print(OUT_DIR / "article-04-solid-components.png")


if __name__ == "__main__":
    main()
