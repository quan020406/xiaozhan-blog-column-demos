from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "animations" / "article-03"
ASSET_DIR = OUT / "assets"
W, H = 960, 540
PUBLIC_BASE_URL = "https://raw.githack.com/quan020406/xiaozhan-blog-column-demos/main/animations/article-03"

FONT_CANDIDATES = (
    ("Noto Sans SC (TrueType).otf", "Noto Sans SC Bold (TrueType).otf"),
    ("NotoSansSC-VF.ttf", "NotoSansSC-VF.ttf"),
    ("msyh.ttc", "msyhbd.ttc"),
    ("simhei.ttf", "simhei.ttf"),
)


def font_dirs() -> list[Path]:
    return [
        Path(os.environ.get("SystemRoot", r"C:\Windows")) / "Fonts",
        Path.home() / ".fonts",
        Path("/usr/share/fonts"),
        Path("/Library/Fonts"),
    ]


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


REGULAR_FONT, BOLD_FONT = select_fonts()


def f(size: int, bold: bool = False) -> ImageFont.ImageFont:
    selected = BOLD_FONT if bold else REGULAR_FONT
    if selected:
        return ImageFont.truetype(str(selected), size)
    return ImageFont.load_default(size=size)


def text(draw: ImageDraw.ImageDraw, xy, value: str, size=24, fill="#111827", bold=False, anchor="mm"):
    draw.text(xy, value, font=f(size, bold), fill=fill, anchor=anchor)


def rounded(draw: ImageDraw.ImageDraw, box, radius=16, fill="#ffffff", outline="#cbd5e1", width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill="#334155", width=5):
    draw.line([start, end], fill=fill, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        sign = 1 if ex > sx else -1
        pts = [(ex, ey), (ex - sign * 18, ey - 11), (ex - sign * 18, ey + 11)]
    else:
        sign = 1 if ey > sy else -1
        pts = [(ex, ey), (ex - 11, ey - sign * 18), (ex + 11, ey - sign * 18)]
    draw.polygon(pts, fill=fill)


def frame_base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#f6f8fb")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 84), fill="#111827")
    draw.rectangle((0, 84, W, 89), fill="#0ea5e9")
    text(draw, (40, 31), title, 28, "#ffffff", True, "la")
    text(draw, (40, 63), subtitle, 16, "#cbd5e1", False, "la")
    return img, draw


def draw_pipeline_frame(step: int) -> Image.Image:
    img, draw = frame_base("CI 流水线拦截动画", "命中 ALWAYS_TRUE 后，流水线在 Maven 测试前停止")
    stages = [
        ("Agent PR", "提交业务改动", "#dbeafe", "#2563eb"),
        ("完整性审计", "扫描禁止模式", "#fef3c7", "#d97706"),
        ("ALWAYS_TRUE", "命中万能断言", "#fee2e2", "#dc2626"),
        ("EXIT_CODE=1", "阻断后续步骤", "#111827", "#facc15"),
        ("Maven 测试", "不再执行", "#e5e7eb", "#64748b"),
    ]
    y = 190
    xs = [70, 250, 430, 610, 790]
    for i, (title, desc, bg, accent) in enumerate(stages):
        active = i <= min(step, 4)
        fill = bg if active else "#f1f5f9"
        outline = accent if active else "#cbd5e1"
        rounded(draw, (xs[i], y, xs[i] + 130, y + 96), 18, fill, outline, 3 if active else 2)
        text(draw, (xs[i] + 65, y + 36), title, 20 if title != "ALWAYS_TRUE" else 18, accent if active else "#64748b", True)
        text(draw, (xs[i] + 65, y + 68), desc, 14, "#475569")
        if i < len(stages) - 1:
            arrow(draw, (xs[i] + 138, y + 48), (xs[i + 1] - 10, y + 48), "#334155" if i < step else "#cbd5e1", 5)

    if step >= 2:
        rounded(draw, (220, 340, 740, 445), 14, "#101828", "#101828")
        text(draw, (245, 374), "BrokenTest.java:1 [ALWAYS_TRUE] 禁止万能真断言", 19, "#f8fafc", False, "la")
        text(draw, (245, 414), "EXIT_CODE=1", 24, "#facc15", True, "la")
    else:
        rounded(draw, (220, 340, 740, 445), 14, "#ffffff", "#cbd5e1")
        text(draw, (480, 392), "等待审计输出", 22, "#64748b", True)

    if step >= 4:
        text(draw, (480, 492), "结论：禁止模式扫描失败，PR 在测试前被拦截。", 22, "#b91c1c", True)
    else:
        text(draw, (480, 492), "核心理解：防作弊 CI 是先验收边界，再跑测试。", 20, "#334155", True)
    return img


def draw_fake_green_frame(step: int) -> Image.Image:
    img, draw = frame_base("假绿色流水线对比动画", "CI 变绿不等于业务问题已经修好")
    text(draw, (240, 126), "正常修复", 24, "#16a34a", True)
    text(draw, (720, 126), "作弊修复", 24, "#dc2626", True)
    left = [
        ("失败测试", "#fee2e2", "#dc2626"),
        ("修业务逻辑", "#dbeafe", "#2563eb"),
        ("测试通过", "#dcfce7", "#16a34a"),
        ("CI 真绿", "#dcfce7", "#16a34a"),
    ]
    right = [
        ("失败测试", "#fee2e2", "#dc2626"),
        ("assertTrue(true)", "#fef3c7", "#d97706"),
        ("测试通过", "#dcfce7", "#16a34a"),
        ("CI 假绿", "#fee2e2", "#dc2626"),
    ]

    def path(items, x0):
        for i, (label, bg, accent) in enumerate(items):
            y = 170 + i * 78
            active = i <= step
            rounded(draw, (x0, y, x0 + 260, y + 52), 14, bg if active else "#f1f5f9", accent if active else "#cbd5e1")
            text(draw, (x0 + 130, y + 27), label, 20 if len(label) < 12 else 17, accent if active else "#64748b", True)
            if i < len(items) - 1:
                arrow(draw, (x0 + 130, y + 57), (x0 + 130, y + 73), accent if i < step else "#cbd5e1", 4)

    path(left, 110)
    path(right, 590)

    if step >= 3:
        rounded(draw, (80, 482, 880, 522), 10, "#ffffff", "#cbd5e1")
        text(draw, (480, 503), "区别：左边保留失败信号并修复根因；右边消音失败信号，问题还在。", 20, "#111827", True)
    return img


def draw_readonly_frame(step: int) -> Image.Image:
    img, draw = frame_base("只读门禁权限边界动画", "Agent 可以改业务代码，但不能单方面改验收标准")
    draw.line((480, 110, 480, 430), fill="#cbd5e1", width=3)
    text(draw, (240, 122), "Agent 可直接提交", 24, "#2563eb", True)
    text(draw, (720, 122), "需要独立审批", 24, "#7c3aed", True)

    writable = [("src/", "业务实现"), ("tests/", "测试补充")]
    guarded = [("pipeline/", "CI 守门脚本"), ("cheat_detector.py", "禁止模式规则")]

    for i, (name, desc) in enumerate(writable):
        y = 180 + i * 105
        active = step >= i
        rounded(draw, (105, y, 375, y + 76), 16, "#dbeafe" if active else "#f1f5f9", "#2563eb" if active else "#cbd5e1")
        text(draw, (150, y + 30), name, 24, "#2563eb" if active else "#64748b", True, "la")
        text(draw, (150, y + 58), desc, 16, "#475569", False, "la")

    for i, (name, desc) in enumerate(guarded):
        y = 180 + i * 105
        active = step >= i + 1
        rounded(draw, (585, y, 855, y + 76), 16, "#ede9fe" if active else "#f1f5f9", "#7c3aed" if active else "#cbd5e1")
        text(draw, (630, y + 30), name, 22 if len(name) < 15 else 18, "#7c3aed" if active else "#64748b", True, "la")
        text(draw, (630, y + 58), desc, 16, "#475569", False, "la")
        if active:
            text(draw, (820, y + 38), "Review", 16, "#7c3aed", True)

    if step >= 3:
        rounded(draw, (230, 430, 730, 505), 14, "#101828", "#101828")
        text(draw, (260, 462), "CODEOWNERS: /pipeline/ @platform-reviewers", 21, "#f8fafc", False, "la")
        text(draw, (260, 492), "规则变化必须经过平台或人类审批", 18, "#a7f3d0", False, "la")
    else:
        rounded(draw, (230, 430, 730, 505), 14, "#ffffff", "#cbd5e1")
        text(draw, (480, 468), "只读不是物理只读，而是审批权隔离。", 21, "#334155", True)
    return img


def save_gif(name: str, frames: list[Image.Image], duration: int = 700) -> None:
    path = ASSET_DIR / f"{name}.gif"
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
        disposal=2,
    )


CSS = """
:root{color-scheme:light;--page:#f6f8fb;--ink:#111827;--muted:#64748b;--line:#cbd5e1;--blue:#2563eb;--red:#dc2626;--green:#16a34a;--amber:#d97706;--violet:#7c3aed}
*{box-sizing:border-box}body{margin:0;font-family:"Microsoft YaHei","Noto Sans SC","Segoe UI",Arial,sans-serif;background:var(--page);color:var(--ink)}
main{width:min(1120px,calc(100vw - 28px));margin:0 auto;padding:24px 0 40px}header{display:flex;justify-content:space-between;gap:18px;align-items:flex-end;margin-bottom:18px}
h1{margin:0 0 8px;font-size:30px;line-height:1.2;letter-spacing:0}.lead{margin:0;color:var(--muted);line-height:1.7}.controls{display:flex;gap:10px;flex-wrap:wrap}button{min-height:38px;border:1px solid var(--line);background:#fff;border-radius:8px;padding:0 14px;font-weight:700;cursor:pointer}.primary{background:var(--blue);border-color:var(--blue);color:#fff}
.stage{background:#fff;border:1px solid var(--line);border-radius:8px;padding:22px;overflow:hidden}.timeline{position:relative;height:360px}.box{position:absolute;width:170px;min-height:86px;border-radius:8px;border:2px solid var(--line);background:#fff;display:grid;place-items:center;text-align:center;padding:10px;transition:.45s ease;box-shadow:0 10px 24px rgba(15,23,42,.08)}.box strong{display:block;font-size:20px}.box span{display:block;color:var(--muted);font-size:14px;margin-top:6px;line-height:1.45}.box.active{transform:translateY(-8px);border-width:3px}.blue{background:#dbeafe;border-color:var(--blue);color:var(--blue)}.amber{background:#fef3c7;border-color:var(--amber);color:var(--amber)}.red{background:#fee2e2;border-color:var(--red);color:var(--red)}.green{background:#dcfce7;border-color:var(--green);color:var(--green)}.dark{background:#111827;border-color:#111827;color:#facc15}.gray{background:#e5e7eb;border-color:#94a3b8;color:#475569}.arrow{position:absolute;height:4px;background:#334155;transform-origin:left center;transition:.45s ease}.arrow::after{content:"";position:absolute;right:-1px;top:-8px;border-left:16px solid #334155;border-top:10px solid transparent;border-bottom:10px solid transparent}.arrow.dim{background:#cbd5e1}.arrow.dim::after{border-left-color:#cbd5e1}
.terminal{background:#101828;color:#f8fafc;border-radius:8px;padding:16px;font-family:Consolas,"Courier New",monospace;line-height:1.65;min-height:104px}.terminal .warn{color:#facc15}.note{margin-top:16px;padding:14px 16px;border:1px solid var(--line);border-left:5px solid var(--blue);border-radius:8px;background:#fff;color:#334155;line-height:1.7}.split{display:grid;grid-template-columns:1fr 1fr;gap:18px}.lane{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;min-height:380px}.lane h2{margin:0 0 16px}.step{min-height:52px;border:2px solid var(--line);border-radius:8px;margin:0 0 22px;padding:12px 14px;font-weight:800;text-align:center;transition:.4s}.down{height:22px;text-align:center;color:#64748b;margin-top:-17px}.guard-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.guard-column{position:relative;min-height:390px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px}.guard-column h2{margin:0 0 18px}.guard-card{border:2px solid var(--line);border-radius:8px;padding:16px;margin-bottom:20px;transition:.4s}.guard-card strong{display:block;font-size:22px}.guard-card span{display:block;margin-top:6px;color:var(--muted)}.code{background:#101828;color:#f8fafc;border-radius:8px;padding:14px 16px;font-family:Consolas,"Courier New",monospace;line-height:1.7}.embed{margin-top:22px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px}.embed textarea{width:100%;min-height:88px;border:1px solid var(--line);border-radius:8px;padding:10px;font-family:Consolas,"Courier New",monospace}
@media(max-width:760px){header{display:block}.controls{margin-top:14px}.split,.guard-grid{grid-template-columns:1fr}.timeline{height:620px}.box{left:50%!important;transform:translateX(-50%)}.box.active{transform:translate(-50%,-8px)}.arrow{display:none}}
"""


def html_page(slug: str, title: str, lead: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
      <div class="controls">
        <button class="primary" id="play">播放</button>
        <button id="reset">重置</button>
      </div>
    </header>
    {body}
    <section class="embed">
      <strong>iframe 调用</strong>
      <textarea readonly><iframe src="{PUBLIC_BASE_URL}/{slug}.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe></textarea>
    </section>
  </main>
</body>
</html>
"""


def ci_gate_html() -> str:
    body = """
<section class="stage">
  <div class="timeline" id="timeline">
    <div class="box blue" style="left:20px;top:110px" data-step="0"><div><strong>Agent PR</strong><span>提交业务改动</span></div></div>
    <div class="box amber" style="left:210px;top:110px" data-step="1"><div><strong>完整性审计</strong><span>扫描禁止模式</span></div></div>
    <div class="box red" style="left:400px;top:110px" data-step="2"><div><strong>ALWAYS_TRUE</strong><span>命中万能断言</span></div></div>
    <div class="box dark" style="left:590px;top:110px" data-step="3"><div><strong>EXIT_CODE=1</strong><span>阻断流水线</span></div></div>
    <div class="box gray" style="left:780px;top:110px" data-step="4"><div><strong>Maven 测试</strong><span>不再执行</span></div></div>
    <div class="arrow" style="left:190px;top:152px;width:36px"></div>
    <div class="arrow" style="left:380px;top:152px;width:36px"></div>
    <div class="arrow" style="left:570px;top:152px;width:36px"></div>
    <div class="arrow" style="left:760px;top:152px;width:36px"></div>
  </div>
  <div class="terminal" id="terminal">等待完整性审计输出...</div>
  <div class="note" id="note">防作弊 CI 的关键不是多跑一个脚本，而是在 Maven 测试之前先确认验收边界没有被削弱。</div>
</section>
<script>
let step=0,timer=null;const boxes=[...document.querySelectorAll('.box')],arrows=[...document.querySelectorAll('.arrow')],term=document.getElementById('terminal'),note=document.getElementById('note');
function paint(){boxes.forEach((b,i)=>b.classList.toggle('active',i<=step));arrows.forEach((a,i)=>a.classList.toggle('dim',i>=step));if(step<2){term.textContent='等待完整性审计输出...';note.textContent='防作弊 CI 的关键不是多跑一个脚本，而是在 Maven 测试之前先确认验收边界没有被削弱。'}else{term.innerHTML='BrokenTest.java:1 [ALWAYS_TRUE] 禁止万能真断言<br><span class="warn">EXIT_CODE=1</span>';note.textContent='脚本打印文件、行号和规则码，并以非零退出码阻断流水线。'}}function play(){clearInterval(timer);timer=setInterval(()=>{step=Math.min(4,step+1);paint();if(step===4)clearInterval(timer)},700)}function reset(){clearInterval(timer);step=0;paint()}document.getElementById('play').onclick=play;document.getElementById('reset').onclick=reset;paint();
</script>
"""
    return html_page("ci-gate", "CI 流水线拦截动画", "命中 ALWAYS_TRUE 后，流水线在 Maven 测试前停止。", body)


def fake_green_html() -> str:
    body = """
<section class="split">
  <div class="lane">
    <h2 style="color:#16a34a">正常修复</h2>
    <div class="step red" data-left="0">失败测试</div><div class="down">↓</div>
    <div class="step blue" data-left="1">修业务逻辑</div><div class="down">↓</div>
    <div class="step green" data-left="2">测试通过</div><div class="down">↓</div>
    <div class="step green" data-left="3">CI 真绿</div>
  </div>
  <div class="lane">
    <h2 style="color:#dc2626">作弊修复</h2>
    <div class="step red" data-right="0">失败测试</div><div class="down">↓</div>
    <div class="step amber" data-right="1">assertTrue(true)</div><div class="down">↓</div>
    <div class="step green" data-right="2">测试通过</div><div class="down">↓</div>
    <div class="step red" data-right="3">CI 假绿</div>
  </div>
</section>
<div class="note" id="note">左侧保留失败信号并修复根因；右侧只是消音失败信号，问题仍然存在。</div>
<script>
let step=0,timer=null;const left=[...document.querySelectorAll('[data-left]')],right=[...document.querySelectorAll('[data-right]')],note=document.getElementById('note');
function paint(){left.forEach((n,i)=>n.style.opacity=i<=step?'1':'.28');right.forEach((n,i)=>n.style.opacity=i<=step?'1':'.28');note.textContent=step<3?'CI 变绿只说明检查通过，不自动代表业务不变量已经恢复。':'对 Agent 来说，奖励函数不能是“让 CI 通过”，而应是“保持测试信号和业务不变量”。'}function play(){clearInterval(timer);timer=setInterval(()=>{step=Math.min(3,step+1);paint();if(step===3)clearInterval(timer)},800)}function reset(){clearInterval(timer);step=0;paint()}document.getElementById('play').onclick=play;document.getElementById('reset').onclick=reset;paint();
</script>
"""
    return html_page("fake-green", "假绿色流水线对比动画", "对比真正修复和作弊修复：两边都能绿，但含义完全不同。", body)


def readonly_gate_html() -> str:
    body = """
<section class="guard-grid">
  <div class="guard-column">
    <h2 style="color:#2563eb">Agent 可直接提交</h2>
    <div class="guard-card blue" data-open="0"><strong>src/</strong><span>业务实现</span></div>
    <div class="guard-card blue" data-open="1"><strong>tests/</strong><span>测试补充</span></div>
  </div>
  <div class="guard-column">
    <h2 style="color:#7c3aed">需要独立审批</h2>
    <div class="guard-card" data-guard="0"><strong>pipeline/</strong><span>CI 守门脚本</span></div>
    <div class="guard-card" data-guard="1"><strong>cheat_detector.py</strong><span>禁止模式规则</span></div>
  </div>
</section>
<div class="code" id="code">CODEOWNERS:
/pipeline/ @platform-reviewers
/ai_firm/cheat_detector.py @platform-reviewers</div>
<div class="note" id="note">只读不是物理只读，而是审批权隔离：Agent 可以提交代码，但不能单方面改变验收标准。</div>
<script>
let step=0,timer=null;const open=[...document.querySelectorAll('[data-open]')],guard=[...document.querySelectorAll('[data-guard]')],note=document.getElementById('note');
function paint(){open.forEach((n,i)=>n.style.opacity=i<=step?'1':'.3');guard.forEach((n,i)=>{n.style.opacity=i+1<=step?'1':'.3';n.classList.toggle('red',i+1<=step)});note.textContent=step<2?'业务代码可以交给 Agent 高吞吐修改，但验收标准必须由独立角色维护。':'如果 Agent 试图修改 pipeline 或规则文件，CODEOWNERS 会要求平台维护者审批。'}function play(){clearInterval(timer);timer=setInterval(()=>{step=Math.min(3,step+1);paint();if(step===3)clearInterval(timer)},850)}function reset(){clearInterval(timer);step=0;paint()}document.getElementById('play').onclick=play;document.getElementById('reset').onclick=reset;paint();
</script>
"""
    return html_page("readonly-gate", "只读门禁权限边界动画", "Agent 可以修改业务代码，但不能单方面改写裁判规则。", body)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_index() -> None:
    pages = [
        ("ci-gate.html", "CI 流水线拦截动画", "assets/ci-gate.gif"),
        ("fake-green.html", "假绿色流水线对比动画", "assets/fake-green.gif"),
        ("readonly-gate.html", "只读门禁权限边界动画", "assets/readonly-gate.gif"),
    ]
    cards = "\n".join(
        f'<article><h2>{title}</h2><a href="{href}"><img src="{gif}" alt="{title}"></a><p><a href="{href}">打开完整动画页</a></p></article>'
        for href, title, gif in pages
    )
    write_text(
        OUT / "index.html",
        f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>第三期动画辅助理解</title>
  <style>
    body{{margin:0;background:#f6f8fb;color:#111827;font-family:"Microsoft YaHei","Noto Sans SC","Segoe UI",Arial,sans-serif}}
    main{{width:min(1120px,calc(100vw - 28px));margin:0 auto;padding:28px 0 44px}}
    h1{{margin:0 0 8px;font-size:32px}}.lead{{color:#64748b;line-height:1.7;margin:0 0 22px}}
    .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}article{{background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:14px}}h2{{font-size:18px;margin:0 0 12px}}img{{width:100%;display:block;border-radius:8px;border:1px solid #e5e7eb}}a{{color:#2563eb;font-weight:700}}
    textarea{{width:100%;min-height:150px;border:1px solid #cbd5e1;border-radius:8px;padding:12px;font-family:Consolas,"Courier New",monospace}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
  <main>
    <h1>第三期动画辅助理解</h1>
    <p class="lead">包含 3 个 GIF 和 3 个完整 HTML 动画页，可通过在线渲染地址直接跳转或 iframe 嵌入。</p>
    <section class="grid">{cards}</section>
    <h2>iframe 示例</h2>
    <textarea readonly><iframe src="{PUBLIC_BASE_URL}/ci-gate.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe>
<iframe src="{PUBLIC_BASE_URL}/fake-green.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe>
<iframe src="{PUBLIC_BASE_URL}/readonly-gate.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe></textarea>
  </main>
</body>
</html>
""",
    )


def write_iframe_snippets() -> None:
    write_text(
        OUT / "iframe-snippets.md",
        """# 第三期动画 iframe 调用

在线渲染基础地址：

`https://raw.githack.com/quan020406/xiaozhan-blog-column-demos/main/animations/article-03/`

## CI 流水线拦截动画

```html
<iframe src="https://raw.githack.com/quan020406/xiaozhan-blog-column-demos/main/animations/article-03/ci-gate.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe>
```

## 假绿色流水线对比动画

```html
<iframe src="https://raw.githack.com/quan020406/xiaozhan-blog-column-demos/main/animations/article-03/fake-green.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe>
```

## 只读门禁权限边界动画

```html
<iframe src="https://raw.githack.com/quan020406/xiaozhan-blog-column-demos/main/animations/article-03/readonly-gate.html" width="100%" height="620" loading="lazy" style="border:0;border-radius:8px;"></iframe>
```
""",
    )


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    save_gif("ci-gate", [draw_pipeline_frame(i) for i in [0, 1, 2, 3, 4, 4]], 700)
    save_gif("fake-green", [draw_fake_green_frame(i) for i in [0, 1, 2, 3, 3]], 800)
    save_gif("readonly-gate", [draw_readonly_frame(i) for i in [0, 1, 2, 3, 3]], 850)
    write_text(OUT / "ci-gate.html", ci_gate_html())
    write_text(OUT / "fake-green.html", fake_green_html())
    write_text(OUT / "readonly-gate.html", readonly_gate_html())
    write_index()
    write_iframe_snippets()
    for path in [
        ASSET_DIR / "ci-gate.gif",
        ASSET_DIR / "fake-green.gif",
        ASSET_DIR / "readonly-gate.gif",
        OUT / "ci-gate.html",
        OUT / "fake-green.html",
        OUT / "readonly-gate.html",
        OUT / "index.html",
        OUT / "iframe-snippets.md",
    ]:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
