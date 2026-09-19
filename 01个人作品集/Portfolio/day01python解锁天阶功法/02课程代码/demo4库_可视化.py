#rap刚需肯定是节奏，我们现在就来点beat

# 所谓的库其实就是python自带或者我们去下载的一些有很多现成功能的工具箱
# 科学运算 numpy ，表格处理 pandas ，爬虫 requests .....
# 认识一个简单的库，random
# 我想要生成一个随机数
# 1.导入随机库 import 库的名字
# 1.下载课程资源 2.提交作业 3.班主任截图暗号领取福利 4.周三来上课


import time

name = '李四'
se = 1
# 打印标题，营造仪式感
print("="*40)
print(name+"        老师 · Python自我介绍RAP")
print("="*40)
time.sleep(se)

# ==================== RAP核心内容（逐句生成，全程押韵） ====================
print("\n🎤 节奏响起，准备出发！")
time.sleep(se)

print("hello everyone，this is AKA"+name)
time.sleep(se)

print("今年十八，意气风发！")
time.sleep(se)

print("编程教学，是我的家！")
time.sleep(se)

print("酷爱代码，笔生繁花！")
time.sleep(se)

print("带领学员，勇闯天涯！")
time.sleep(se)

print("学好Python，梦想不塌！")
time.sleep(se)

print("用心授课，不负韶华！")
time.sleep(se)

print("愿你前行，步步生花！")
time.sleep(se)

print("编程之路，一起出发！")
time.sleep(se)

# 结尾祝福
print("\n✨ 祝所有学员：代码无错，快乐相伴！")
time.sleep(0.5)
print("✨ Python第一课，我们正式启航！")

# =========================
# 新增：HTML 外化展示区
# 注意：上方原始教学代码不得改动
# =========================

AUTO_OPEN_HTML = True
OPEN_WITH_CHROME = True
ALLOW_DEFAULT_BROWSER_FALLBACK = True

import ast
import json
import os
import shutil
import webbrowser
from pathlib import Path


def _get_current_python_file_path():
    try:
        return Path(__file__).resolve()
    except NameError:
        return Path("demo4.py").resolve()


def _read_original_python_source(py_path):
    full_source = py_path.read_text(encoding="utf-8")
    marker = "# =========================\n# 新增：HTML 外化展示区"
    marker_index = full_source.find(marker)
    if marker_index == -1:
        return full_source
    return full_source[:marker_index].rstrip()


def _safe_eval_print_arg(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _safe_eval_print_arg(node.left)
        right = _safe_eval_print_arg(node.right)

        if isinstance(node.op, ast.Mult):
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, int) and isinstance(right, str):
                return left * right

        if isinstance(node.op, ast.Add):
            return str(left) + str(right)

    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            else:
                parts.append(ast.unparse(value))
        return "".join(parts)

    try:
        return ast.literal_eval(node)
    except Exception:
        try:
            return ast.unparse(node)
        except Exception:
            return ""


def _safe_eval_sleep_arg(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    try:
        value = ast.literal_eval(node)
        if isinstance(value, (int, float)):
            return float(value)
    except Exception:
        pass

    return 1.0


def _get_keyword_value(call_node, keyword_name, default_value):
    for keyword in call_node.keywords:
        if keyword.arg == keyword_name:
            try:
                return ast.literal_eval(keyword.value)
            except Exception:
                return default_value
    return default_value


def _is_print_call(node):
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print"
    )


def _is_time_sleep_call(node):
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and node.value.func.attr == "sleep"
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id == "time"
        and len(node.value.args) >= 1
    )


def _has_emoji(text):
    for char in text:
        code = ord(char)
        if (
            0x1F300 <= code <= 0x1FAFF
            or 0x2600 <= code <= 0x27BF
            or 0x2300 <= code <= 0x23FF
        ):
            return True
    return False


def _detect_event_kind(text):
    stripped = text.strip()

    if stripped and set(stripped) == {"="}:
        return "border"

    if "开阳老师" in stripped and "Python" in stripped:
        return "title"

    if "节奏响起" in stripped or "准备出发" in stripped:
        return "intro"

    if "祝所有学员" in stripped or "正式启航" in stripped or "Python第一课" in stripped:
        return "finale"

    rap_lines = [
        "hello everyone，this is AKA开阳！",
        "今年十八，意气风发！",
        "编程教学，是我的家！",
        "酷爱代码，笔生繁花！",
        "带领学员，勇闯天涯！",
        "学好Python，梦想不塌！",
        "用心授课，不负韶华！",
        "愿你前行，步步生花！",
        "编程之路，一起出发！",
    ]

    if stripped in rap_lines:
        return "rap"

    return "normal"


def _extract_print_and_sleep_events(original_source):
    tree = ast.parse(original_source)
    events = []

    for node in tree.body:
        if _is_print_call(node):
            call = node.value
            sep = _get_keyword_value(call, "sep", " ")
            end = _get_keyword_value(call, "end", "\n")

            arg_values = [_safe_eval_print_arg(arg) for arg in call.args]
            text = sep.join(str(value) for value in arg_values)
            if end not in ("", "\n"):
                text += str(end)

            display_text = text.replace("\r", "").strip("\n")
            events.append({
                "line": getattr(node, "lineno", 0),
                "text": display_text,
                "sleep_seconds": None,
                "kind": _detect_event_kind(display_text),
                "has_emoji": _has_emoji(display_text),
            })

        elif _is_time_sleep_call(node):
            sleep_seconds = _safe_eval_sleep_arg(node.value.args[0])
            for event in reversed(events):
                if event["sleep_seconds"] is None:
                    event["sleep_seconds"] = sleep_seconds
                    break

    for event in events:
        if event["sleep_seconds"] is None:
            if event["kind"] == "border":
                event["sleep_seconds"] = 0.45
            elif event["kind"] == "title":
                event["sleep_seconds"] = 0.85
            elif event["kind"] == "finale":
                event["sleep_seconds"] = 1.2
            else:
                event["sleep_seconds"] = 0.75

    return events


def _build_html(events, source_file_name):
    events_json = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    source_json = json.dumps(source_file_name, ensure_ascii=False).replace("</", "<\\/")

    html_template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>开阳老师 · Python 自我介绍 RAP</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {
    box-sizing: border-box;
}

:root {
    --gold: #ffd36a;
    --hot: #ff4fd8;
    --blue: #45d7ff;
    --green: #57ff9a;
    --dark: #060711;
    --panel: rgba(13, 16, 38, 0.82);
}

body {
    margin: 0;
    min-height: 100vh;
    overflow-x: hidden;
    color: #ffffff;
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", Arial, sans-serif;
    background:
        radial-gradient(circle at 20% 12%, rgba(255, 79, 216, 0.28), transparent 32%),
        radial-gradient(circle at 82% 18%, rgba(69, 215, 255, 0.22), transparent 34%),
        radial-gradient(circle at 50% 85%, rgba(255, 211, 106, 0.16), transparent 35%),
        linear-gradient(145deg, #02030a 0%, #080b18 42%, #111327 100%);
}

.stage-page {
    position: relative;
    min-height: 100vh;
    padding: 28px;
    overflow: hidden;
}

.noise {
    pointer-events: none;
    position: fixed;
    inset: 0;
    opacity: 0.08;
    background-image:
        linear-gradient(rgba(255,255,255,0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px);
    background-size: 36px 36px;
    mix-blend-mode: screen;
}

.spotlight {
    position: fixed;
    top: -12%;
    width: 34vw;
    height: 75vh;
    opacity: 0.36;
    filter: blur(12px);
    transform-origin: top center;
    background: linear-gradient(to bottom, rgba(255,255,255,0.28), rgba(255,255,255,0.04), transparent);
    clip-path: polygon(43% 0%, 57% 0%, 100% 100%, 0% 100%);
    animation: swing 4s ease-in-out infinite alternate;
}

.spotlight.left {
    left: 10%;
    transform: rotate(18deg);
}

.spotlight.right {
    right: 10%;
    transform: rotate(-18deg);
    animation-delay: -1.5s;
}

@keyframes swing {
    from { opacity: 0.16; transform: rotate(12deg); }
    to { opacity: 0.44; transform: rotate(-10deg); }
}

.stage-shell {
    position: relative;
    z-index: 2;
    max-width: 1180px;
    margin: 0 auto;
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 28px;
    padding: 26px;
    background: linear-gradient(180deg, rgba(8,10,28,0.88), rgba(5,6,14,0.72));
    box-shadow:
        0 28px 90px rgba(0,0,0,0.62),
        inset 0 0 42px rgba(69,215,255,0.08);
    backdrop-filter: blur(14px);
}

.stage-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,0.11);
}

.title-wrap h1 {
    margin: 0;
    font-size: clamp(30px, 5vw, 58px);
    letter-spacing: 2px;
    line-height: 1.08;
    background: linear-gradient(90deg, #fff8d8, var(--gold), #ff8be7, #8cecff);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 38px rgba(255, 211, 106, 0.26);
}

.title-wrap p {
    margin: 10px 0 0;
    color: rgba(255,255,255,0.72);
    font-size: 15px;
}

.meta-card {
    min-width: 240px;
    padding: 14px 16px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.76);
    font-size: 13px;
    line-height: 1.7;
}

.main-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.65fr);
    gap: 22px;
    margin-top: 22px;
}

.performance-panel {
    position: relative;
    min-height: 560px;
    padding: 26px;
    border-radius: 26px;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 28%, rgba(255, 211, 106, 0.15), transparent 30%),
        linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.12);
}

.performance-panel::before {
    content: "";
    position: absolute;
    left: -18%;
    right: -18%;
    bottom: -22%;
    height: 42%;
    background:
        radial-gradient(ellipse at center, rgba(255, 211, 106, 0.22), transparent 58%),
        linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    filter: blur(10px);
}

.stage-border {
    position: relative;
    z-index: 2;
    min-height: 48px;
    padding: 12px 14px;
    border-radius: 16px;
    border: 1px dashed rgba(255,211,106,0.45);
    color: var(--gold);
    text-align: center;
    letter-spacing: 4px;
    font-family: Consolas, Monaco, monospace;
    background: rgba(255,211,106,0.06);
}

.rap-center {
    position: relative;
    z-index: 2;
    display: grid;
    place-items: center;
    min-height: 335px;
    padding: 26px 12px;
}

.mic-wrap {
    position: relative;
    width: 190px;
    height: 190px;
    display: grid;
    place-items: center;
    margin-bottom: 16px;
}

.wave {
    position: absolute;
    width: 92px;
    height: 92px;
    border-radius: 999px;
    border: 2px solid rgba(69,215,255,0.28);
    animation: wavePulse 1.8s linear infinite;
}

.wave.w2 {
    animation-delay: 0.6s;
    border-color: rgba(255,79,216,0.28);
}

.wave.w3 {
    animation-delay: 1.2s;
    border-color: rgba(255,211,106,0.28);
}

@keyframes wavePulse {
    from { transform: scale(0.55); opacity: 0.95; }
    to { transform: scale(2.18); opacity: 0; }
}

.microphone {
    position: relative;
    z-index: 2;
    width: 86px;
    height: 86px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 50px;
    background: radial-gradient(circle at 35% 30%, #ffffff, #adbbd8 45%, #30364f 76%);
    box-shadow:
        0 0 35px rgba(69,215,255,0.34),
        0 0 60px rgba(255,79,216,0.18);
    animation: micBounce 1.25s ease-in-out infinite alternate;
}

@keyframes micBounce {
    from { transform: translateY(0) rotate(-4deg); }
    to { transform: translateY(-10px) rotate(5deg); }
}

.beat-status {
    text-align: center;
    font-weight: 800;
    letter-spacing: 3px;
    color: var(--green);
    text-shadow: 0 0 18px rgba(87,255,154,0.65);
    margin-bottom: 16px;
}

.current-card {
    width: min(720px, 100%);
    min-height: 158px;
    padding: 24px;
    border-radius: 24px;
    text-align: center;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04)),
        rgba(0,0,0,0.24);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 18px 42px rgba(0,0,0,0.34);
}

.current-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(69,215,255,0.12);
    color: #b8f2ff;
    font-size: 13px;
    letter-spacing: 1px;
}

.current-emoji {
    font-size: 48px;
    line-height: 1;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 18px rgba(255,211,106,0.45));
}

.current-lyric {
    font-size: clamp(26px, 4.8vw, 48px);
    font-weight: 900;
    line-height: 1.22;
    letter-spacing: 1px;
    text-shadow:
        0 0 18px rgba(255,255,255,0.16),
        0 0 26px rgba(69,215,255,0.20);
}

.current-lyric.rap {
    color: #ffffff;
}

.current-lyric.intro {
    color: var(--green);
    animation: glowIntro 0.9s ease-in-out infinite alternate;
}

.current-lyric.finale {
    color: #fff1a8;
    animation: finaleGlow 0.8s ease-in-out infinite alternate;
}

@keyframes glowIntro {
    from { text-shadow: 0 0 12px rgba(87,255,154,0.5); }
    to { text-shadow: 0 0 35px rgba(87,255,154,0.95), 0 0 60px rgba(69,215,255,0.35); }
}

@keyframes finaleGlow {
    from { text-shadow: 0 0 12px rgba(255,211,106,0.55); transform: scale(1); }
    to { text-shadow: 0 0 34px rgba(255,211,106,0.95), 0 0 70px rgba(255,79,216,0.38); transform: scale(1.025); }
}

.beat-bars {
    position: relative;
    z-index: 2;
    height: 92px;
    display: flex;
    align-items: end;
    justify-content: center;
    gap: 7px;
    margin-top: 16px;
}

.beat-bars span {
    width: 10px;
    height: 24px;
    border-radius: 999px 999px 2px 2px;
    background: linear-gradient(to top, var(--blue), var(--hot), var(--gold));
    box-shadow: 0 0 16px rgba(69,215,255,0.35);
    animation: beat 0.75s ease-in-out infinite alternate;
}

.beat-bars span:nth-child(2n) {
    animation-delay: 0.16s;
}

.beat-bars span:nth-child(3n) {
    animation-delay: 0.32s;
}

.beat-bars span:nth-child(4n) {
    animation-delay: 0.48s;
}

@keyframes beat {
    from { height: 18px; opacity: 0.58; }
    to { height: 86px; opacity: 1; }
}

.timeline-panel {
    padding: 20px;
    border-radius: 24px;
    background: var(--panel);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: inset 0 0 28px rgba(255,255,255,0.04);
}

.timeline-panel h2 {
    margin: 0 0 14px;
    font-size: 20px;
    color: #fff4cf;
}

.timeline {
    display: grid;
    gap: 10px;
    max-height: 510px;
    overflow: auto;
    padding-right: 6px;
}

.timeline::-webkit-scrollbar {
    width: 6px;
}

.timeline::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 999px;
}

.line-item {
    display: grid;
    grid-template-columns: 42px 1fr;
    gap: 10px;
    align-items: center;
    padding: 10px;
    border-radius: 16px;
    color: rgba(255,255,255,0.64);
    background: rgba(255,255,255,0.045);
    border: 1px solid transparent;
    transition: 0.25s ease;
}

.line-num {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: rgba(255,255,255,0.75);
    background: rgba(255,255,255,0.08);
    font-size: 12px;
    font-family: Consolas, Monaco, monospace;
}

.line-text {
    font-size: 14px;
    line-height: 1.45;
}

.line-item.active {
    color: #ffffff;
    transform: translateX(4px);
    border-color: rgba(255,211,106,0.48);
    background: linear-gradient(90deg, rgba(255,211,106,0.18), rgba(69,215,255,0.08));
    box-shadow: 0 0 28px rgba(255,211,106,0.12);
}

.line-item.active .line-num {
    background: var(--gold);
    color: #191000;
    font-weight: 900;
}

.knowledge {
    position: relative;
    z-index: 2;
    margin-top: 22px;
    padding: 20px;
    border-radius: 24px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
}

.knowledge h2 {
    margin: 0 0 14px;
    color: #b8f2ff;
}

.knowledge-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}

.knowledge-card {
    min-height: 98px;
    padding: 15px;
    border-radius: 18px;
    background: rgba(0,0,0,0.22);
    border: 1px solid rgba(255,255,255,0.11);
}

.knowledge-card strong {
    display: block;
    color: var(--gold);
    margin-bottom: 8px;
    font-size: 15px;
}

.knowledge-card span {
    color: rgba(255,255,255,0.70);
    font-size: 13px;
    line-height: 1.55;
}

.confetti-layer {
    pointer-events: none;
    position: fixed;
    inset: 0;
    z-index: 5;
    overflow: hidden;
}

.confetti {
    position: absolute;
    top: -20px;
    width: 10px;
    height: 18px;
    border-radius: 3px;
    background: var(--gold);
    animation: confettiDrop 3.2s linear forwards;
}

@keyframes confettiDrop {
    to {
        transform: translateY(110vh) rotate(720deg);
        opacity: 0;
    }
}

.star {
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 12px #ffffff;
    animation: twinkle 1.3s ease-in-out infinite alternate;
}

@keyframes twinkle {
    from { opacity: 0.2; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1.6); }
}

@media (max-width: 920px) {
    .main-grid {
        grid-template-columns: 1fr;
    }

    .stage-header {
        flex-direction: column;
    }

    .meta-card {
        width: 100%;
    }

    .knowledge-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 560px) {
    .stage-page {
        padding: 14px;
    }

    .stage-shell {
        padding: 16px;
        border-radius: 20px;
    }

    .performance-panel {
        padding: 16px;
        min-height: 520px;
    }

    .knowledge-grid {
        grid-template-columns: 1fr;
    }
}
</style>
</head>
<body>
<div class="stage-page">
    <div class="noise"></div>
    <div class="spotlight left"></div>
    <div class="spotlight right"></div>
    <div class="confetti-layer" id="confettiLayer"></div>

    <main class="stage-shell">
        <header class="stage-header">
            <div class="title-wrap">
                <h1>开阳老师 · Python 自我介绍 RAP</h1>
                <p>把 print 顺序执行、time.sleep 节奏控制，外化成一场 Python RAP 舞台播放器。</p>
            </div>
            <div class="meta-card">
                <div>主题：Python RAP 舞台播放器</div>
                <div>源码读取：<span id="sourceFile"></span></div>
                <div>播放方式：按原代码 print + sleep 节奏逐句出现</div>
            </div>
        </header>

        <section class="main-grid">
            <section class="performance-panel">
                <div class="stage-border" id="stageBorder">========================================</div>

                <div class="rap-center">
                    <div class="mic-wrap">
                        <div class="wave"></div>
                        <div class="wave w2"></div>
                        <div class="wave w3"></div>
                        <div class="microphone">🎤</div>
                    </div>

                    <div class="beat-status" id="beatStatus">BEAT READY</div>

                    <div class="current-card">
                        <div class="current-label" id="currentLabel">等待舞台启动</div>
                        <div class="current-emoji" id="currentEmoji">🎧</div>
                        <div class="current-lyric" id="currentLyric">Python RAP 即将开始</div>
                    </div>
                </div>

                <div class="beat-bars" aria-hidden="true">
                    <span></span><span></span><span></span><span></span><span></span>
                    <span></span><span></span><span></span><span></span><span></span>
                    <span></span><span></span><span></span><span></span><span></span>
                    <span></span><span></span><span></span>
                </div>
            </section>

            <aside class="timeline-panel">
                <h2>逐句 RAP 播放列表</h2>
                <div class="timeline" id="timeline"></div>
            </aside>
        </section>

        <section class="knowledge">
            <h2>课堂知识点</h2>
            <div class="knowledge-grid">
                <div class="knowledge-card">
                    <strong>import time</strong>
                    <span>导入 Python 标准库 time，让程序拥有“等待”和“控制节奏”的能力。</span>
                </div>
                <div class="knowledge-card">
                    <strong>time.sleep 控制节奏</strong>
                    <span>每次 sleep 都像 Rap 的停顿，让上一句歌词停留指定秒数。</span>
                </div>
                <div class="knowledge-card">
                    <strong>print 顺序执行</strong>
                    <span>print 会按照代码从上到下的顺序，一句一句输出内容。</span>
                </div>
                <div class="knowledge-card">
                    <strong>程序从上往下运行</strong>
                    <span>Python 不会乱跳，默认按照文件顺序执行，这就是课堂第一课的核心。</span>
                </div>
            </div>
        </section>
    </main>
</div>

<script>
const RAP_EVENTS = __EVENTS_JSON__;
const SOURCE_FILE = __SOURCE_JSON__;

const timeline = document.getElementById("timeline");
const currentLyric = document.getElementById("currentLyric");
const currentEmoji = document.getElementById("currentEmoji");
const currentLabel = document.getElementById("currentLabel");
const beatStatus = document.getElementById("beatStatus");
const stageBorder = document.getElementById("stageBorder");
const sourceFile = document.getElementById("sourceFile");
const confettiLayer = document.getElementById("confettiLayer");

sourceFile.textContent = SOURCE_FILE;

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function labelByKind(kind) {
    const labels = {
        border: "舞台开场边框",
        title: "标题亮相",
        intro: "开场动画",
        rap: "当前歌词高亮",
        finale: "收尾仪式",
        normal: "终端输出"
    };
    return labels[kind] || "终端输出";
}

function findEmoji(text) {
    const match = text.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2300}-\u{23FF}]/u);
    return match ? match[0] : "";
}

function renderTimeline() {
    timeline.innerHTML = "";
    RAP_EVENTS.forEach((event, index) => {
        const item = document.createElement("div");
        item.className = "line-item";
        item.dataset.index = index;

        const num = document.createElement("div");
        num.className = "line-num";
        num.textContent = String(index + 1).padStart(2, "0");

        const text = document.createElement("div");
        text.className = "line-text";
        text.textContent = event.text || "(空输出)";

        item.appendChild(num);
        item.appendChild(text);
        timeline.appendChild(item);
    });
}

function activateTimeline(index) {
    document.querySelectorAll(".line-item").forEach(item => item.classList.remove("active"));

    const active = document.querySelector(`.line-item[data-index="${index}"]`);
    if (active) {
        active.classList.add("active");
        active.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

function createStars() {
    for (let i = 0; i < 42; i++) {
        const star = document.createElement("div");
        star.className = "star";
        star.style.left = Math.random() * 100 + "vw";
        star.style.top = Math.random() * 100 + "vh";
        star.style.animationDelay = Math.random() * 1.2 + "s";
        document.body.appendChild(star);

        setTimeout(() => {
            star.remove();
        }, 4600);
    }
}

function createConfetti() {
    const colors = ["#ffd36a", "#ff4fd8", "#45d7ff", "#57ff9a", "#ffffff"];

    for (let i = 0; i < 100; i++) {
        const piece = document.createElement("div");
        piece.className = "confetti";
        piece.style.left = Math.random() * 100 + "vw";
        piece.style.background = colors[Math.floor(Math.random() * colors.length)];
        piece.style.animationDelay = Math.random() * 1.1 + "s";
        piece.style.transform = `rotate(${Math.random() * 360}deg)`;
        confettiLayer.appendChild(piece);

        setTimeout(() => {
            piece.remove();
        }, 4600);
    }
}

function activateEvent(event, index) {
    activateTimeline(index);

    const text = event.text || "";
    const kind = event.kind || "normal";
    const emoji = event.has_emoji ? findEmoji(text) : "";

    currentLyric.textContent = text || "(空输出)";
    currentLyric.className = "current-lyric " + kind;
    currentLabel.textContent = labelByKind(kind);

    if (emoji) {
        currentEmoji.textContent = emoji;
        currentEmoji.style.display = "block";
    } else if (kind === "rap") {
        currentEmoji.textContent = "🎙️";
        currentEmoji.style.display = "block";
    } else if (kind === "finale") {
        currentEmoji.textContent = "✨";
        currentEmoji.style.display = "block";
    } else {
        currentEmoji.textContent = "🎧";
        currentEmoji.style.display = "block";
    }

    if (kind === "border") {
        stageBorder.textContent = text;
        beatStatus.textContent = "STAGE BORDER ONLINE";
    }

    if (kind === "title") {
        beatStatus.textContent = "TITLE DROP";
    }

    if (kind === "intro") {
        beatStatus.textContent = "灯光打开 · 舞台启动 · BEAT READY";
        document.body.classList.add("lights-on");
    }

    if (kind === "rap") {
        beatStatus.textContent = "FLOW PLAYING · " + Number(event.sleep_seconds || 0).toFixed(1) + "s PAUSE";
    }

    if (kind === "finale") {
        beatStatus.textContent = "FINAL CEREMONY · PYTHON 第一课正式启航";
        createStars();
        createConfetti();
    }
}

async function openingCountdown() {
    const beats = ["3", "2", "1", "BEAT READY"];
    for (const beat of beats) {
        beatStatus.textContent = beat;
        await wait(520);
    }
}

async function playRapStage() {
    renderTimeline();
    await openingCountdown();

    for (let index = 0; index < RAP_EVENTS.length; index++) {
        const event = RAP_EVENTS[index];
        activateEvent(event, index);

        const seconds = Number(event.sleep_seconds || 0.8);
        const pause = Math.max(360, seconds * 1000);
        await wait(pause);
    }

    beatStatus.textContent = "SHOW END · 代码无错，快乐相伴";
}

playRapStage();
</script>
</body>
</html>
'''
    return (
        html_template
        .replace("__EVENTS_JSON__", events_json)
        .replace("__SOURCE_JSON__", source_json)
    )


def _find_chrome_executable():
    candidate_paths = []

    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        program_files_x86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")

        candidate_paths.extend([
            Path(program_files) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(program_files_x86) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(local_app_data) / "Google" / "Chrome" / "Application" / "chrome.exe",
        ])

    elif sys_platform := os.environ.get("OSTYPE", ""):
        pass

    extra_candidates = [
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]

    for candidate in extra_candidates:
        if candidate:
            candidate_paths.append(Path(candidate))

    mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    candidate_paths.append(mac_chrome)

    for path in candidate_paths:
        try:
            if path and Path(path).exists():
                return str(path)
        except Exception:
            continue

    return None


def _open_html_file(html_path):
    print(f"HTML 已生成：{html_path}")

    if not AUTO_OPEN_HTML:
        print("AUTO_OPEN_HTML = False，仅生成 HTML，不自动打开浏览器。")
        return

    file_url = html_path.as_uri()

    try:
        chrome_path = _find_chrome_executable() if OPEN_WITH_CHROME else None

        if OPEN_WITH_CHROME and chrome_path:
            webbrowser.register(
                "chrome-for-python-rap-stage",
                None,
                webbrowser.BackgroundBrowser(chrome_path)
            )
            webbrowser.get("chrome-for-python-rap-stage").open(file_url)
            print(f"已优先使用 Google Chrome 打开：{html_path}")
            return

        if OPEN_WITH_CHROME and not chrome_path:
            print("未找到 Google Chrome。")

        if ALLOW_DEFAULT_BROWSER_FALLBACK:
            webbrowser.open(file_url)
            print(f"已使用系统默认浏览器打开：{html_path}")
        else:
            print("ALLOW_DEFAULT_BROWSER_FALLBACK = False，未打开浏览器。")

    except Exception as error:
        print(f"浏览器打开失败，但程序不中断。HTML 文件路径：{html_path}")
        print(f"失败原因：{error}")


def _generate_rap_stage_html():
    py_path = _get_current_python_file_path()
    original_source = _read_original_python_source(py_path)
    events = _extract_print_and_sleep_events(original_source)

    html_file = py_path.with_name("demo4_RAP舞台_HTML外化展示.html")
    html_content = _build_html(events, py_path.name)
    html_file.write_text(html_content, encoding="utf-8")

    _open_html_file(html_file)


_generate_rap_stage_html()