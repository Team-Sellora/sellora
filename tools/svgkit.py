"""Tiny helper for hand-built, dark-theme SVG diagrams.

Every visual in the showcase repo is generated from this file so the
palette, type and stroke weights stay identical across images.
"""
from xml.sax.saxutils import escape

# Palette (validated on the dark surface with the dataviz validator)
BG = "#0d1117"
CARD = "#161b22"
CARD_2 = "#1c2129"
BORDER = "#30363d"
GRID = "#21262d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
FAINT = "#6e7681"
BLUE = "#3987e5"
ORANGE = "#d95926"
AQUA = "#199e70"
RED = "#d03b3b"
GOOD = "#0ca30c"

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def doc(w, h, body, title="", grid=True):
    pattern = ""
    grid_rect = ""
    if grid:
        pattern = (
            '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1" fill="{GRID}"/></pattern>'
        )
        grid_rect = f'<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>"
        "<defs>"
        f"{pattern}"
        + "".join(
            f'<marker id="arr-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{col}"/></marker>'
            for name, col in (("m", MUTED), ("b", BLUE), ("o", ORANGE), ("a", AQUA), ("r", RED))
        )
        + "</defs>"
        f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>'
        f"{grid_rect}"
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{BORDER}"/>'
        f"{body}</svg>"
    )


def text(x, y, s, size=14, fill=TEXT, weight=400, anchor="start", font=SANS, ls=None, opacity=None):
    extra = f' letter-spacing="{ls}"' if ls is not None else ""
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'
    )


def rect(x, y, w, h, fill=CARD, stroke=BORDER, rx=10, sw=1, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'


def line(x1, y1, x2, y2, stroke=MUTED, sw=1.5, arrow=None, dash=None, opacity=None):
    m = f' marker-end="url(#arr-{arrow})"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{m}{d}{o}/>'


def path(d, stroke=MUTED, sw=1.5, arrow=None, dash=None, opacity=None, start_arrow=None):
    m = f' marker-end="url(#arr-{arrow})"' if arrow else ""
    if start_arrow:
        m += f' marker-start="url(#arr-{start_arrow})"'
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{m}{da}{o}/>'


def pill(x, y, label, fill=CARD_2, stroke=BORDER, color=TEXT, size=13, font=SANS, pad=12, h=28, weight=500):
    w = approx_width(label, size, font) + pad * 2
    return (
        rect(x, y, w, h, fill=fill, stroke=stroke, rx=h / 2)
        + text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, fill=color, anchor="middle", font=font, weight=weight)
    ), w


def approx_width(s, size, font=SANS):
    # Rough advance widths, generous so labels never collide.
    if font == MONO:
        return len(s) * size * 0.62
    wide = sum(1 for c in s if c in "MWmw@%")
    narrow = sum(1 for c in s if c in "ilIjt.,:;|'!() ")
    normal = len(s) - wide - narrow
    return size * (normal * 0.56 + wide * 0.82 + narrow * 0.3)


def card(x, y, w, h, title, sub=None, accent=None, title_size=17, sub_size=13, center=False, fill=CARD):
    out = rect(x, y, w, h, fill=fill, stroke=accent or BORDER, sw=1.5 if accent else 1)
    if accent:
        out += f'<rect x="{x+1}" y="{y+1}" width="4" height="{h-2}" rx="2" fill="{accent}"/>' if not center else ""
    if center:
        cx = x + w / 2
        ty = y + h / 2 + (-4 if sub else 6)
        out += text(cx, ty, title, size=title_size, weight=600, anchor="middle")
        if sub:
            out += text(cx, ty + 22, sub, size=sub_size, fill=MUTED, anchor="middle")
    else:
        out += text(x + 20, y + 32, title, size=title_size, weight=600)
        if sub:
            out += text(x + 20, y + 56, sub, size=sub_size, fill=MUTED)
    return out


def badge_num(cx, cy, n, color=BLUE):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="13" fill="{BG}" stroke="{color}" stroke-width="1.5"/>'
        + text(cx, cy + 4.5, str(n), size=13, weight=700, fill=TEXT, anchor="middle")
    )
