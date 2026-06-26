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


def label(
    draw: ImageDraw.ImageDraw,
    xy,
    text: str,
    size: int = 30,
    fill: str = "#111827",
    bold: bool = False,
    anchor: str = "mm",
) -> None:
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(
    draw: ImageDraw.ImageDraw,
    box,
    radius: int = 22,
    fill: str = "#ffffff",
    outline: str = "#cbd5e1",
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill: str = "#475569", width: int = 5) -> None:
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


def base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#f6f8fb")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 132), fill="#111827")
    draw.rectangle((0, 132, W, 138), fill="#0ea5e9")
    label(draw, (80, 54), title, 42, "#ffffff", True, "la")
    label(draw, (80, 100), subtitle, 24, "#cbd5e1", False, "la")
    return img, draw


def workflow_cover() -> None:
    img, draw = base(
        "Human-in-the-loop 研发工作流",
        "Agent 负责执行，自动化负责拦截，人类负责不可外包的判断",
    )

    swimlanes = [
        (95, 200, 1505, 340, "任务定义", "业务不变量 / 验收标准 / 风险边界", "#dbeafe", "#2563eb"),
        (95, 385, 1505, 525, "Agent 执行", "读取有限上下文 / 修改允许文件 / 输出可审计 diff", "#fef3c7", "#d97706"),
        (95, 570, 1505, 710, "自动化门禁", "完整性扫描 / 单元测试 / 并发验证 / CI 阻断", "#dcfce7", "#16a34a"),
    ]
    for x1, y1, x2, y2, title, desc, bg, accent in swimlanes:
        rounded(draw, (x1, y1, x2, y2), 26, bg, accent, 3)
        label(draw, (145, y1 + 48), title, 34, accent, True, "la")
        label(draw, (145, y1 + 94), desc, 26, "#374151", False, "la")

    for x in [360, 640, 920, 1200]:
        arrow(draw, (x, 340), (x, 385), "#475569", 5)
        arrow(draw, (x, 525), (x, 570), "#475569", 5)

    rounded(draw, (210, 735, 645, 830), 20, "#ffffff", "#cbd5e1", 2)
    label(draw, (427, 771), "人类审批", 34, "#7c3aed", True)
    label(draw, (427, 810), "数据 / 权限 / 资金 / 发布窗口", 23, "#374151")

    rounded(draw, (955, 735, 1390, 830), 20, "#111827", "#111827", 2)
    label(draw, (1172, 771), "可发布变更", 34, "#facc15", True)
    label(draw, (1172, 810), "附带证据、范围和回滚条件", 23, "#e5e7eb")

    arrow(draw, (645, 782), (925, 782), "#475569", 6)
    label(draw, (785, 750), "签署高风险决策", 23, "#475569", True)

    img.save(OUT_DIR / "article-05-workflow.png", quality=95)


def five_gates() -> None:
    img, draw = base(
        "AI Agent 研发的五道生产门禁",
        "把生成能力放进工程系统，而不是让工程系统为生成能力让路",
    )

    gates = [
        ("需求门", "可量化验收\n业务不变量", "#dbeafe", "#2563eb"),
        ("上下文门", "按依赖提供\n来源可追踪", "#e0e7ff", "#4f46e5"),
        ("实现门", "限制路径\n控制变更面", "#fef3c7", "#d97706"),
        ("验证门", "测试先行\nCI 自动阻断", "#dcfce7", "#16a34a"),
        ("发布门", "人类签署\n高风险决策", "#ede9fe", "#7c3aed"),
    ]

    top_y = 255
    card_w = 245
    gap = 45
    x = 92
    centers: list[tuple[int, int]] = []
    for idx, (title, body, bg, accent) in enumerate(gates, 1):
        x1 = x + (idx - 1) * (card_w + gap)
        x2 = x1 + card_w
        rounded(draw, (x1, top_y, x2, top_y + 260), 26, bg, accent, 3)
        draw.ellipse((x1 + 82, top_y - 38, x1 + 162, top_y + 42), fill="#111827", outline=accent, width=4)
        label(draw, (x1 + 122, top_y + 3), str(idx), 34, "#ffffff", True)
        label(draw, (x1 + 122, top_y + 88), title, 34, accent, True)
        for line_no, line in enumerate(body.splitlines()):
            label(draw, (x1 + 122, top_y + 155 + line_no * 42), line, 27, "#374151")
        centers.append((x2, top_y + 130))

    for idx in range(4):
        sx, sy = centers[idx]
        ex = sx + gap - 16
        arrow(draw, (sx + 12, sy), (ex, sy), "#475569", 5)

    rounded(draw, (115, 610, 1485, 770), 26, "#ffffff", "#cbd5e1", 2)
    label(draw, (165, 664), "责任边界：", 31, "#111827", True, "la")
    label(draw, (345, 664), "Agent 高吞吐执行；自动化确定性拦截；人类保留问题定义、系统设计和风险决策。", 30, "#374151", False, "la")
    label(draw, (165, 720), "发布条件：", 31, "#111827", True, "la")
    label(draw, (345, 720), "证据齐全、变更受控、测试通过、风险有人签署、回滚路径明确。", 30, "#374151", False, "la")

    img.save(OUT_DIR / "article-05-five-gates.png", quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    workflow_cover()
    five_gates()
    print(OUT_DIR / "article-05-workflow.png")
    print(OUT_DIR / "article-05-five-gates.png")


if __name__ == "__main__":
    main()
