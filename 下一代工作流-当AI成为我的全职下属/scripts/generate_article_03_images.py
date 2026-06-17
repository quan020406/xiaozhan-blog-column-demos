from __future__ import annotations

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
    roots = [Path.home() / ".fonts", Path("/usr/share/fonts"), Path("/Library/Fonts")]
    system_root = Path(__import__("os").environ.get("SystemRoot", r"C:\Windows"))
    roots.append(system_root / "Fonts")
    return roots


def find_font(name: str) -> Path | None:
    for root in font_dirs():
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def select_fonts() -> tuple[Path | None, Path | None]:
    for regular, bold in FONT_CANDIDATES:
        regular_path = find_font(regular)
        bold_path = find_font(bold)
        if regular_path and bold_path:
            return regular_path, bold_path
    return None, None


FONT_REGULAR, FONT_BOLD = select_fonts()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    selected = FONT_BOLD if bold else FONT_REGULAR
    if selected:
        return ImageFont.truetype(str(selected), size)
    return ImageFont.load_default(size=size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill, width=5):
    draw.line([start, end], fill=fill, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        sign = 1 if ex > sx else -1
        pts = [(ex, ey), (ex - sign * 22, ey - 13), (ex - sign * 22, ey + 13)]
    else:
        sign = 1 if ey > sy else -1
        pts = [(ex, ey), (ex - 13, ey - sign * 22), (ex + 13, ey - sign * 22)]
    draw.polygon(pts, fill=fill)


def draw_label(draw, xy, text, size=32, fill="#111827", bold=False, anchor="mm"):
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#f6f8fb")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 130), fill="#111827")
    draw_label(draw, (80, 50), title, 44, "#ffffff", True, "la")
    draw_label(draw, (80, 98), subtitle, 24, "#cbd5e1", False, "la")
    draw.rectangle((0, 130, W, 136), fill="#0ea5e9")
    return img, draw


def audit_cover() -> None:
    img, draw = base(
        "AI Agent 防作弊 CI",
        "把“让 CI 通过”改写为不可绕过的验收边界",
    )

    card_y = 210
    cards = [
        ("@Disabled", "跳过核心测试", "#fee2e2", "#dc2626"),
        ("assertTrue(true)", "万能真断言", "#fef3c7", "#d97706"),
        ("catch { }", "吞掉失败信号", "#e0e7ff", "#4f46e5"),
        ("concurrent=1", "降低并发度", "#dcfce7", "#16a34a"),
    ]
    for i, (code, desc, bg, accent) in enumerate(cards):
        x = 95 + i * 365
        rounded(draw, (x, card_y, x + 300, card_y + 170), 22, bg, "#d1d5db", 2)
        draw_label(draw, (x + 150, card_y + 58), code, 34, accent, True)
        draw_label(draw, (x + 150, card_y + 112), desc, 28, "#374151")

    rounded(draw, (140, 500, 1460, 740), 26, "#ffffff", "#cbd5e1", 2)
    draw_label(draw, (215, 560), "规则扫描", 34, "#0369a1", True, "la")
    draw_label(draw, (215, 615), "DISABLED_TEST / ALWAYS_TRUE / EMPTY_CATCH", 28, "#111827", False, "la")
    draw_label(draw, (215, 660), "SWALLOW_THROWABLE / LOW_CONCURRENCY", 28, "#111827", False, "la")
    draw_label(draw, (215, 706), "命中禁止项：输出文件、行号、规则码，并以非零状态阻断流水线", 26, "#4b5563", False, "la")

    rounded(draw, (1095, 575, 1370, 675), 20, "#111827")
    draw_label(draw, (1232, 625), "EXIT CODE = 1", 31, "#facc15", True)

    img.save(OUT_DIR / "article-03-audit.png", quality=95)


def integrity_gate() -> None:
    img, draw = base(
        "只读审计门禁",
        "Agent 可以提交代码，但不能单方面改变验收标准",
    )

    boxes = [
        (90, 250, 340, 410, "Agent PR", "业务代码 / 测试改动", "#dbeafe", "#2563eb"),
        (455, 250, 705, 410, "完整性审计", "禁止模式扫描", "#fef3c7", "#d97706"),
        (820, 250, 1070, 410, "Maven 测试", "编译与核心测试", "#dcfce7", "#16a34a"),
        (1185, 250, 1435, 410, "人工 Review", "事务 / SQL / 锁边界", "#ede9fe", "#7c3aed"),
    ]
    for x1, y1, x2, y2, title, desc, bg, accent in boxes:
        rounded(draw, (x1, y1, x2, y2), 22, bg, "#cbd5e1", 2)
        draw_label(draw, ((x1 + x2) // 2, y1 + 58), title, 35, accent, True)
        draw_label(draw, ((x1 + x2) // 2, y1 + 110), desc, 25, "#374151")

    for x in [340, 705, 1070]:
        arrow(draw, (x + 30, 330), (x + 105, 330), "#475569", 5)

    rounded(draw, (430, 520, 730, 690), 22, "#fee2e2", "#ef4444", 3)
    draw_label(draw, (580, 575), "命中 ALWAYS_TRUE", 23, "#b91c1c", True)
    draw_label(draw, (580, 625), "立即失败", 33, "#991b1b", True)
    arrow(draw, (580, 410), (580, 520), "#ef4444", 5)

    rounded(draw, (780, 530, 1410, 730), 22, "#ffffff", "#cbd5e1", 2)
    draw_label(draw, (820, 592), "CODEOWNERS：", 29, "#111827", True, "la")
    draw_label(draw, (820, 638), "/pipeline/ @platform-reviewers", 28, "#0f766e", False, "la")
    draw_label(draw, (820, 685), "守门脚本由平台或人类审批，Agent 不能直接改规则", 24, "#4b5563", False, "la")

    img.save(OUT_DIR / "article-03-integrity-gate.png", quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    audit_cover()
    integrity_gate()
    print(OUT_DIR / "article-03-audit.png")
    print(OUT_DIR / "article-03-integrity-gate.png")


if __name__ == "__main__":
    main()
