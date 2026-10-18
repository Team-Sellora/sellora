"""Charts built from real git data on the dev branches (see stats.json)."""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import BG, BLUE, BORDER, GRID, MUTED, TEXT, CARD  # noqa: E402

OUT = sys.argv[1]
STATS = json.load(open(sys.argv[2]))

plt.rcParams.update({
    "font.family": "Inter",
    "svg.fonttype": "path",
    "text.color": TEXT,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.edgecolor": BORDER,
    "font.size": 12,
})

W, DPI = 12.8, 100


def frame(fig):
    """Rounded dark card behind the whole figure, matching the diagrams."""
    fig.patch.set_alpha(0)
    fig.patches.append(FancyBboxPatch(
        (0.002, 0.004), 0.996, 0.992, boxstyle="round,pad=0,rounding_size=0.016",
        transform=fig.transFigure, facecolor=BG, edgecolor=BORDER, linewidth=1, zorder=-10))


def style(ax):
    ax.set_facecolor("none")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(length=0, labelsize=12)


def rounded_bars(ax, xs, ys, width, horizontal=False):
    """Bars with a 4px-style rounded data end, anchored square to the baseline."""
    for x, y in zip(xs, ys):
        if horizontal:
            ax.barh(x, y, height=width, color=BLUE, zorder=3)
        else:
            ax.bar(x, y, width=width, color=BLUE, zorder=3)


# ---------------------------------------------------------------- weekly commits
def commits_timeline():
    weekly = {}
    for wk, _repo, n in STATS["weekly"]:
        weekly[wk] = weekly.get(wk, 0) + n
    weeks = sorted(weekly)
    vals = [weekly[w] for w in weeks]
    import datetime as dt
    labels = [dt.date.fromisoformat(w).strftime("%d %b") for w in weeks]

    fig = plt.figure(figsize=(W, 5.0), dpi=DPI)
    frame(fig)
    ax = fig.add_axes([0.065, 0.14, 0.9, 0.56])
    style(ax)
    xs = list(range(len(weeks)))
    bands = [("Sprint 1", 0, 1), ("Sprint 2", 2, 3), ("Sprint 3", 4, 5), ("Sprint 4", 6, 7), ("Wrap-up", 8, 8)]
    for i, (name, a, b) in enumerate(bands):
        if i % 2 == 0:
            ax.axvspan(a - 0.5, b + 0.5, color=CARD, zorder=0, lw=0)
        ax.text((a + b) / 2, max(vals) * 1.13, name.upper(), ha="center", va="bottom",
                fontsize=10.5, color=MUTED, fontweight=600)
    ax.bar(xs, vals, width=0.56, color=BLUE, zorder=3)
    for x, v in zip(xs, vals):
        ax.text(x, v + max(vals) * 0.02, f"{v}", ha="center", va="bottom", fontsize=11.5, color=TEXT, zorder=4)
    ax.set_xticks(xs, labels)
    ax.set_xlim(-0.5, len(xs) - 0.5)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_yticks([0, 100, 200, 300])
    ax.yaxis.grid(True, color=GRID, lw=1, zorder=1)
    ax.set_axisbelow(True)
    ax.set_xlabel("Week starting", fontsize=11.5, labelpad=8)
    fig.text(0.05, 0.89, "Commit activity across all repositories", fontsize=21, fontweight=700, color=TEXT)
    fig.text(0.05, 0.825, f"{sum(vals):,} commits on the dev branches by week. "
             "The Sprint 1 peak is Organization, the template every service was cloned from.", fontsize=12.5, color=MUTED)
    fig.savefig(os.path.join(OUT, "chart-commits.svg"), transparent=True)
    plt.close(fig)


# ---------------------------------------------------------------- code and tests per repo
def code_and_tests():
    repos = {
        "Web console": ("sellora-web", "TypeScript"),
        "Organization": ("sellora-organization", "C#"),
        "Order": ("sellora-order", "C#"),
        "Delivery": ("sellora-delivery", "C#"),
        "Inventory": ("sellora-inventory", "C#"),
        "Notification": ("sellora-notification", "C#"),
        "Catalog": ("sellora-catalog", "C#"),
    }
    tests = STATS["tests"]
    loc = {k: STATS["per_repo"][r]["loc"].get(lang, 0) / 1000 for k, (r, lang) in repos.items()}
    order = sorted(loc, key=loc.get)  # smallest at bottom for barh -> largest at top

    fig = plt.figure(figsize=(W, 5.6), dpi=DPI)
    frame(fig)
    fig.text(0.05, 0.895, "Where the code and the tests live", fontsize=21, fontweight=700, color=TEXT)
    fig.text(0.05, 0.835, "Non-blank lines (generated files excluded) and automated test cases, per repository.",
             fontsize=12.5, color=MUTED)
    panels = [
        (0.155, "Lines of code (thousands)", [loc[k] for k in order], lambda v: f"{v:.1f}k"),
        (0.62, "Automated tests", [tests[repos[k][0]] for k in order], lambda v: f"{v}"),
    ]
    for left, title, vals, fmt in panels:
        ax = fig.add_axes([left, 0.09, 0.32, 0.64])
        style(ax)
        ax.spines["bottom"].set_visible(False)
        ys = list(range(len(order)))
        ax.barh(ys, vals, height=0.5, color=BLUE, zorder=3)
        for y, v in zip(ys, vals):
            ax.text(v + max(vals) * 0.02, y, fmt(v), va="center", fontsize=11.5, color=TEXT)
        ax.set_yticks(ys, order if left < 0.5 else [""] * len(order))
        ax.set_xticks([])
        ax.set_xlim(0, max(vals) * 1.18)
        ax.set_title(title.upper(), loc="left", fontsize=10.5, color=MUTED, fontweight=600, pad=12)
        for lbl in ax.get_yticklabels():
            lbl.set_color(TEXT)
            lbl.set_fontsize(12.5)
    fig.savefig(os.path.join(OUT, "chart-code-and-tests.svg"), transparent=True)
    plt.close(fig)


commits_timeline()
code_and_tests()
print("charts ok")
