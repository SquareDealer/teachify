"""Generate README diagrams (light + dark SVG). Run: python3 .github/assets/make_diagrams.py"""
from pathlib import Path

OUT = Path(__file__).parent
SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(bg="#FAF7F2", ink="#1F1B16", muted="#6B6359", accent="#C2502E",
                  card="#FFFFFF", cardline="#E4DDD2", panel="#F3EDE3", line="#B9AE9F"),
    "dark": dict(bg="#11151B", ink="#ECE7DF", muted="#9A9389", accent="#E88A63",
                 card="#1A2029", cardline="#2E3641", panel="#151A21", line="#56606D"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, family=SANS, weight="400", anchor="start", style="normal", ls="0"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def arrow_defs(t):
    return (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{t["line"]}"/></marker></defs>')


def svg(w, h, t, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{esc(label)}">\n{arrow_defs(t)}\n<rect width="{w}" height="{h}" rx="18" fill="{t["bg"]}"/>\n'
            + "\n".join(body) + "\n</svg>\n")


def lesson_loop(t):
    W, H = 1200, 470
    b = []
    cols = [
        ("THEORY", [("Your material", "chapter · docs · lecture"),
                    ("Lesson", "short HTML + inline quiz"),
                    ("Notes from memory", "checked against the source")]),
        ("PRACTICE", [("Main task", "hint ladder · tests"),
                      ("Bug hunt", "in your own solution"),
                      ("Teach-back", "to a picky junior")]),
        ("REVIEW", None),
    ]
    x0, cw, gap, top = 60, 320, 60, 64
    for ci, (title, items) in enumerate(cols):
        x = x0 + ci * (cw + gap)
        b.append(text(x + 4, top - 18, title, 13, t["accent"], MONO, "600", ls="2"))
        b.append(f'<rect x="{x}" y="{top}" width="{cw}" height="{H - top - 48}" rx="14" fill="{t["panel"]}"/>')
        if items:
            for i, (name, sub) in enumerate(items):
                y = top + 22 + i * 112
                b.append(f'<rect x="{x + 18}" y="{y}" width="{cw - 36}" height="88" rx="10" fill="{t["card"]}" '
                         f'stroke="{t["cardline"]}" stroke-width="1.2"/>')
                n = ci * 3 + i + 1
                b.append(f'<circle cx="{x + 52}" cy="{y + 44}" r="17" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>')
                b.append(text(x + 52, y + 49, str(n), 15, t["accent"], MONO, "600", "middle"))
                b.append(text(x + 84, y + 40, name, 20, t["ink"], SERIF, "700"))
                b.append(text(x + 84, y + 64, sub, 14, t["muted"]))
            for i in range(2):
                cy = top + 22 + i * 112 + 44
                b.append(f'<line x1="{x + 52}" y1="{cy + 19}" x2="{x + 52}" y2="{cy + 112 - 21}" stroke="{t["line"]}" '
                         f'stroke-width="1.5" marker-end="url(#ah)"/>')
        else:
            cx = x + cw / 2
            b.append(text(cx, top + 64, "Spaced review", 22, t["ink"], SERIF, "700", "middle"))
            b.append(text(cx, top + 90, "closed-book quiz, mixed topics", 14, t["muted"], anchor="middle"))
            # timeline of review days
            ty = top + 170
            b.append(f'<line x1="{x + 46}" y1="{ty}" x2="{x + cw - 46}" y2="{ty}" stroke="{t["line"]}" stroke-width="1.5"/>')
            days = ["+1", "+3", "+7", "+21"]
            for k, d in enumerate(days):
                dx = x + 46 + k * (cw - 92) / 3
                filled = k < 3
                b.append(f'<circle cx="{dx}" cy="{ty}" r="9" fill="{t["accent"] if filled else t["panel"]}" '
                         f'stroke="{t["accent"]}" stroke-width="1.5"/>')
                b.append(text(dx, ty + 34, d, 15, t["ink"] if filled else t["muted"], MONO, "600", "middle"))
            b.append(text(cx, ty + 60, "days after the lesson", 13.5, t["muted"], anchor="middle"))
            # mastered badge
            my = top + 290
            b.append(f'<rect x="{x + 40}" y="{my}" width="{cw - 80}" height="54" rx="27" fill="none" '
                     f'stroke="{t["accent"]}" stroke-width="1.5"/>')
            b.append(text(cx, my + 24, "☑ Mastered", 18, t["accent"], SERIF, "700", "middle"))
            b.append(text(cx, my + 43, "≥ 80% three or more days later", 12.5, t["muted"], anchor="middle"))
        if ci < 2:
            ay = top + (H - top - 48) / 2
            b.append(f'<line x1="{x + cw + 10}" y1="{ay}" x2="{x + cw + gap - 10}" y2="{ay}" stroke="{t["line"]}" '
                     f'stroke-width="1.8" marker-end="url(#ah)"/>')
    return svg(W, H, t, b, "Lesson loop: theory, practice, spaced review")


def architecture(t):
    W, H = 1200, 470
    b = []
    # You
    b.append(f'<circle cx="92" cy="235" r="40" fill="none" stroke="{t["ink"]}" stroke-width="1.6"/>')
    b.append(text(92, 241, "You", 19, t["ink"], SERIF, "700", "middle"))
    b.append(f'<line x1="138" y1="235" x2="196" y2="235" stroke="{t["line"]}" stroke-width="1.8" '
             f'marker-start="url(#ah)" marker-end="url(#ah)"/>')
    # Tutor
    tx, ty, tw, th = 204, 105, 300, 260
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{t["card"]}" '
             f'stroke="{t["accent"]}" stroke-width="1.6"/>')
    b.append(text(tx + 24, ty + 40, "Tutor", 24, t["ink"], SERIF, "700"))
    b.append(text(tx + 24, ty + 62, "main thread · talks to you", 13.5, t["accent"], MONO))
    duties = ["diagnostic", "hint ladder", "Q&A, quizzes, grading", "bug-hunt debrief", "teach-back", "progress files"]
    for i, d in enumerate(duties):
        yy = ty + 100 + i * 26
        b.append(f'<circle cx="{tx + 30}" cy="{yy - 5}" r="3" fill="{t["muted"]}"/>')
        b.append(text(tx + 44, yy, d, 15.5, t["ink"]))
    # Subagents panel
    px, py, pw, ph = 578, 58, 584, 366
    b.append(text(px + 4, py - 16, "SUBAGENTS · NO DIALOGUE", 13, t["accent"], MONO, "600", ls="2"))
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{t["panel"]}"/>')
    b.append(f'<line x1="{tx + tw + 8}" y1="235" x2="{px - 8}" y2="235" stroke="{t["line"]}" stroke-width="1.8" '
             f'marker-end="url(#ah)"/>')
    agents = [
        ("source-ingester", "your files → Markdown", "parallel"),
        ("curriculum-planner", "map · diagnostic · roadmap", ""),
        ("theory-builder", "theory.html · cheat sheets", "parallel"),
        ("practice-builder", "tasks · tests · answer key", "parallel"),
        ("bug-injector", "plants bugs in your code", ""),
        ("fact-checker", "audits lessons and notes", "independent"),
    ]
    cw, chh = 266, 96
    for i, (name, sub, tag) in enumerate(agents):
        c, r = i % 2, i // 2
        x = px + 18 + c * (cw + 16)
        y = py + 18 + r * (chh + 16)
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="10" fill="{t["card"]}" '
                 f'stroke="{t["cardline"]}" stroke-width="1.2"/>')
        ny = y + 34 if tag else y + 42
        b.append(text(x + 18, ny, name, 16.5, t["ink"], MONO, "600"))
        b.append(text(x + 18, ny + 24, sub, 14, t["muted"]))
        if tag:
            tw_ = 7.2 * len(tag) + 18
            b.append(f'<rect x="{x + 18}" y="{y + 68}" width="{tw_}" height="18" rx="9" fill="none" '
                     f'stroke="{t["accent"]}" stroke-width="1"/>')
            b.append(text(x + 18 + tw_ / 2, y + 81, tag, 11, t["accent"], MONO, anchor="middle"))
    return svg(W, H, t, b, "Architecture: the tutor talks to you; six subagents do heavy work without dialogue")


for name, t in THEMES.items():
    (OUT / f"lesson-loop-{name}.svg").write_text(lesson_loop(t))
    (OUT / f"architecture-{name}.svg").write_text(architecture(t))
print("ok")
