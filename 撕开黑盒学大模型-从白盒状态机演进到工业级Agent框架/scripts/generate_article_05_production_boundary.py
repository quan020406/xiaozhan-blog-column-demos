from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "article-05-production-boundary.png"
FONT_NAMES = (
    "NotoSansSC-VF.ttf",
    "Noto Sans SC (TrueType).otf",
    "msyh.ttc",
    "simhei.ttf",
    "PingFang.ttc",
    "NotoSansCJK-Regular.ttc",
)


def font_dirs() -> list[Path]:
    roots = [
        Path.home() / ".fonts",
        Path("/System/Library/Fonts"),
        Path("/usr/share/fonts"),
        Path("/usr/share/fonts/opentype/noto"),
    ]
    system_root = os.environ.get("SystemRoot")
    if system_root:
        roots.append(Path(system_root) / "Fonts")
    return roots


def font_candidates() -> list[Path]:
    candidates: list[Path] = []
    if os.environ.get("ARTICLE_FONT"):
        candidates.append(Path(os.environ["ARTICLE_FONT"]))
    for root in font_dirs():
        for name in FONT_NAMES:
            candidates.append(root / name)
    return candidates


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for candidate in font_candidates():
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str) -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=2)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, color: str = "#14213d", bold: bool = False) -> None:
    draw.text(xy, value, fill=color, font=font(size, bold=bold))


def bullet(draw: ImageDraw.ImageDraw, x: int, y: int, value: str, color: str) -> None:
    draw.ellipse((x, y + 8, x + 10, y + 18), fill=color)
    text(draw, (x + 20, y), value, 28, "#25324b")


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    draw.line((start, end), fill=color, width=5)
    x, y = end
    draw.polygon([(x, y), (x - 16, y - 10), (x - 16, y + 10)], fill=color)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1600, 900), "#f7f8fb")
    draw = ImageDraw.Draw(img)

    text(draw, (70, 42), "从 Demo Trace 到生产级 Agent：上线边界图", 46, "#111827", True)
    text(draw, (72, 104), "证据来自 v4_langchain/trace.json：call_model -> call_tool -> finalize", 26, "#4b5563")

    rounded(draw, (70, 180, 500, 720), "#ffffff", "#d1d5db")
    text(draw, (105, 220), "当前 Demo 已证明", 34, "#0f766e", True)
    bullet(draw, 112, 295, "状态图节点可执行", "#0f766e")
    bullet(draw, 112, 355, "条件路由可分支", "#0f766e")
    bullet(draw, 112, 415, "工具结果进入 state", "#0f766e")
    bullet(draw, 112, 475, "trace.json 可回放节点", "#0f766e")
    bullet(draw, 112, 535, "最终答案来自工具结果", "#0f766e")

    nodes = [
        ("call_model", "next=tool"),
        ("call_tool", "tool_result=48.0"),
        ("finalize", "answer=预算结果是 48.0"),
    ]
    y = 250
    for idx, (name, desc) in enumerate(nodes):
        rounded(draw, (585, y, 1015, y + 100), "#eef2ff", "#818cf8")
        text(draw, (625, y + 18), name, 31, "#3730a3", True)
        text(draw, (625, y + 57), desc, 24, "#4338ca")
        if idx < len(nodes) - 1:
            arrow(draw, (800, y + 105), (800, y + 145), "#6366f1")
        y += 160

    rounded(draw, (1100, 180, 1530, 720), "#fff7ed", "#fb923c")
    text(draw, (1135, 220), "生产上线仍缺口", 34, "#c2410c", True)
    bullet(draw, 1142, 295, "没有 checkpoint 恢复", "#ea580c")
    bullet(draw, 1142, 355, "没有 timeout / retry 记录", "#ea580c")
    bullet(draw, 1142, 415, "没有参数 schema 校验", "#ea580c")
    bullet(draw, 1142, 475, "没有人工审批断点", "#ea580c")
    bullet(draw, 1142, 535, "没有 token / 成本指标", "#ea580c")
    bullet(draw, 1142, 595, "没有多租户隔离字段", "#ea580c")

    arrow(draw, (500, 450), (585, 450), "#64748b")
    arrow(draw, (1015, 450), (1100, 450), "#64748b")

    rounded(draw, (70, 780, 1530, 850), "#111827", "#111827")
    text(
        draw,
        (105, 800),
        "结论：Demo 能证明“状态推进可见”，但还不能证明“失败可恢复、风险可控制、成本可审计”。",
        30,
        "#ffffff",
        True,
    )

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
