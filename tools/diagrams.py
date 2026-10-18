import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import *  # noqa: E402,F403

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- banner
def banner():
    w, h = 1280, 420
    b = ""
    b += text(64, 104, "SE3022 CASE STUDY  |  SLIIT  |  2026", size=13, fill=MUTED, weight=600, ls=2)
    b += text(60, 184, "Sellora", size=84, weight=700, ls=-2)
    b += text(64, 228, "Multi-tenant field sales and distribution platform", size=22, fill=TEXT, weight=500)
    b += text(64, 258, "for FMCG companies, built as event-driven microservices.", size=22, fill=MUTED)
    x = 64
    for label in (".NET 8", "Apache Kafka", "WSO2 IS + APIM", "PostgreSQL", "React", "Azure"):
        p, pw = pill(x, 300, label, size=13)
        b += p
        x += pw + 10

    # Right side: an abstract service mesh glyph.
    cx, cy, r = 1010, 210, 120
    names = ["ORG", "CAT", "INV", "ORD", "DEL", "NOT", "AUD"]
    pts = []
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / len(names)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a), n))
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="1.5"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r*0.55}" fill="none" stroke="{GRID}" stroke-dasharray="3 6"/>'
    for px, py, _ in pts:
        b += line(cx, cy, px, py, stroke=BORDER, sw=1)
    b += f'<circle cx="{cx}" cy="{cy}" r="38" fill="{CARD}" stroke="{BLUE}" stroke-width="1.5"/>'
    b += text(cx, cy - 2, "KAFKA", size=12, weight=700, anchor="middle", ls=1.5)
    b += text(cx, cy + 14, "event bus", size=11, fill=MUTED, anchor="middle")
    for px, py, n in pts:
        col = ORANGE if n == "ORD" else BORDER
        b += f'<rect x="{px-26}" y="{py-17}" width="52" height="34" rx="9" fill="{CARD_2}" stroke="{col}" stroke-width="1.5"/>'
        b += text(px, py + 4.5, n, size=12, weight=700, anchor="middle", font=MONO)
    return doc(w, h, b, "Sellora banner")


# ---------------------------------------------------------------- stats strip
def stats():
    items = [
        ("7", "microservices"),
        ("80+", "REST endpoints"),
        ("1,100+", "automated tests"),
        ("1,000+", "commits"),
        ("150+", "merged pull requests"),
        ("4", "two-week sprints"),
    ]
    w, h = 1280, 170
    gap = 16
    tw = (w - 2 * 32 - gap * 5) / 6
    b = ""
    for i, (num, label) in enumerate(items):
        x = 32 + i * (tw + gap)
        b += rect(x, 28, tw, 114, fill=CARD)
        b += f'<rect x="{x+20}" y="28" width="28" height="3" rx="1.5" fill="{BLUE}"/>'
        b += text(x + 20, 92, num, size=36, weight=700, ls=-1)
        b += text(x + 20, 120, label, size=14, fill=MUTED)
    return doc(w, h, b, "Project in numbers", grid=False)


# ---------------------------------------------------------------- architecture
def architecture():
    w, h = 1280, 900
    b = text(64, 70, "System architecture", size=28, weight=700)
    b += text(64, 98, "How a request reaches a service, and how services talk to each other.", size=15, fill=MUTED)

    # Client
    b += card(440, 136, 400, 70, "Web console", "React 19  ·  TanStack Router  ·  Vercel", center=True)

    # Edge
    b += card(300, 276, 460, 84, "WSO2 API Manager", "Gateway  ·  token validation  ·  throttling", center=True)
    b += card(860, 276, 356, 84, "WSO2 Identity Server", "OAuth2 / OIDC  ·  PKCE  ·  SCIM2", center=True, accent=AQUA)
    for x in (300, 860):
        p, _ = pill(x + 12, 262, "AWS EC2", size=11, h=22, pad=9, color=MUTED, fill=BG)
        b += p

    b += line(600, 206, 600, 274, stroke=BLUE, sw=1.75, arrow="b")
    b += text(612, 246, "HTTPS + bearer token", size=13, fill=MUTED)
    b += path("M840 171 H1038 V274", stroke=AQUA, sw=1.75, arrow="a", dash="6 5")
    b += text(870, 160, "Sign in with Authorization Code + PKCE", size=13, fill=MUTED)
    b += line(762, 318, 858, 318, stroke=MUTED, sw=1.5, dash="4 4")
    b += text(810, 308, "key manager", size=12, fill=MUTED, anchor="middle")

    # Services container
    cy0, cy1 = 420, 700
    b += rect(64, cy0, 1152, cy1 - cy0, fill="none", stroke=BORDER, rx=14, dash="6 6")
    b += text(88, cy0 + 30, "AZURE APP SERVICE  ·  STAGING AND PRODUCTION SLOTS  ·  ONE DOCKER IMAGE PER SERVICE",
              size=12, fill=MUTED, weight=600, ls=1.2)
    b += line(530, 360, 530, cy0 - 2, stroke=BLUE, sw=1.75, arrow="b")
    b += text(542, 396, "routes /{service}/v1", size=13, fill=MUTED, font=MONO)

    services = [
        ("Organization", "Hierarchy, staff, shops, scope", None),
        ("Catalog", "Products, categories, prices", None),
        ("Inventory", "Stock per owner, reservations", None),
        ("Order", "Orders, GPS checkout, cash", ORANGE),
        ("Delivery", "Jobs, live tracking, returns", None),
        ("Notification", "Email receipts with retries", None),
        ("Audit & Reporting", "Tamper-evident log, reports", None),
    ]
    cw, ch, g = 262, 84, 20
    row1x = (w - (4 * cw + 3 * g)) / 2
    row2x = (w - (3 * cw + 2 * g)) / 2
    for i, (t, s, acc) in enumerate(services):
        if i < 4:
            x, y = row1x + i * (cw + g), cy0 + 52
        else:
            x, y = row2x + (i - 4) * (cw + g), cy0 + 52 + ch + 18
        b += card(x, y, cw, ch, t, s, accent=acc)
    b += text(w / 2, cy1 - 18,
              "Order is the only service that calls others synchronously (Organization, Catalog, Inventory). Everything after that is asynchronous.",
              size=13, fill=MUTED, anchor="middle")

    # Data layer
    ky = 760
    b += rect(64, ky, 772, 92, fill=CARD, stroke=BLUE, sw=1.5)
    b += text(88, ky + 32, "Apache Kafka", size=17, weight=600)
    b += text(212, ky + 32, "on Confluent Cloud", size=13, fill=MUTED)
    x = 88
    for t in ("hierarchy", "catalog", "inventory", "order", "delivery"):
        p, pw = pill(x, ky + 48, f"sellora.{t}.v1", size=11, font=MONO, h=26, pad=8,
                     stroke=ORANGE if t == "order" else BORDER)
        b += p
        x += pw + 6
    b += card(852, ky, 364, 92, "PostgreSQL 16", "Azure Flexible Server, one DB per service")
    b += line(414, cy1 + 2, 414, ky - 2, stroke=BLUE, sw=1.75, arrow="b")
    b += text(426, cy1 + 38, "outbox publish  /  idempotent consume", size=13, fill=MUTED)
    b += line(1034, cy1 + 2, 1034, ky - 2, stroke=MUTED, sw=1.5, arrow="m")
    b += text(1046, cy1 + 38, "EF Core", size=13, fill=MUTED)
    return doc(w, h, b, "Sellora system architecture")


# ---------------------------------------------------------------- hierarchy
def hierarchy():
    w, h = 1280, 600
    b = text(64, 70, "The business hierarchy", size=28, weight=700)
    b += text(64, 98, "Every record belongs to one company. Five roles act at five levels.", size=15, fill=MUTED)
    ents = [
        ("Company", "the tenant", "Company Admin", "runs the whole tenant"),
        ("Province", "first-class entity", "Area Manager", "can cover many provinces"),
        ("Agency", "local distributor", "Agency Operator", "registers shops"),
        ("Territory", "exactly one rep", "Sales Rep", "sells and collects cash"),
        ("Shop", "has GPS coordinates", "Shop Owner", "orders and confirms"),
    ]
    bw, gap = 184, 59
    x0 = (w - (5 * bw + 4 * gap)) / 2
    for i, (e, es, r, rs) in enumerate(ents):
        x = x0 + i * (bw + gap)
        b += card(x, 150, bw, 84, e, es, center=True, accent=BLUE if i == 3 else None)
        b += line(x + bw / 2, 236, x + bw / 2, 292, stroke=BORDER, sw=1.5, dash="3 4")
        b += rect(x + 8, 294, bw - 16, 70, fill=CARD_2, stroke=BORDER, rx=35)
        b += text(x + bw / 2, 324, r, size=14.5, weight=600, anchor="middle")
        b += text(x + bw / 2, 345, rs, size=12, fill=MUTED, anchor="middle")
        if i < 4:
            ax = x + bw
            b += line(ax + 4, 192, ax + gap - 6, 192, stroke=MUTED, arrow="m")
            b += text(ax + gap / 2, 182, "1 : N", size=12, fill=MUTED, anchor="middle", font=MONO)
    b += text(64, 418, "RULES THE SYSTEM ENFORCES", size=12, fill=MUTED, weight=600, ls=1.5)
    rules = [
        ("One rep per territory", "Territory to Sales Rep is strictly 1 : 1, so every sale has one owner."),
        ("Shops come from agencies", "Only an agency registers shops, and only in territories it was given."),
        ("Tenant comes from the token", "The company ID is read from the signed JWT, never from the request."),
    ]
    rw = (w - 128 - 2 * 20) / 3
    for i, (t, s) in enumerate(rules):
        x = 64 + i * (rw + 20)
        b += rect(x, 436, rw, 112, fill=CARD)
        b += text(x + 20, 472, t, size=16, weight=600)
        words, lines_, cur = s.split(), [], ""
        for wd in words:
            if approx_width(cur + " " + wd, 13.5) > rw - 40:
                lines_.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines_.append(cur)
        for j, ln in enumerate(lines_):
            b += text(x + 20, 500 + j * 21, ln, size=13.5, fill=MUTED)
    return doc(w, h, b, "Sellora business hierarchy")


# ---------------------------------------------------------------- event map
def events():
    w, h = 1280, 680
    b = text(64, 70, "Event flow", size=28, weight=700)
    b += text(64, 98, "Five services publish facts. Four services react to them in their own time.",
              size=15, fill=MUTED)
    cols = {"p": 64, "t": 520, "c": 976}
    cw = 240
    for key, label in (("p", "PRODUCER"), ("t", "KAFKA TOPIC"), ("c", "CONSUMERS")):
        b += text(cols[key], 146, label, size=12, fill=MUTED, weight=600, ls=1.5)
    prods = ["Organization", "Catalog", "Inventory", "Order", "Delivery"]
    topics = ["hierarchy", "catalog", "inventory", "order", "delivery"]
    cons = ["Inventory", "Notification", "Delivery", "Audit & Reporting"]
    py = [170 + i * 82 for i in range(5)]
    cy = [190 + i * 100 for i in range(4)]
    links = {
        "hierarchy": ["Inventory", "Audit & Reporting"],
        "catalog": ["Audit & Reporting"],
        "inventory": ["Notification", "Audit & Reporting"],
        "order": ["Inventory", "Notification", "Delivery", "Audit & Reporting"],
        "delivery": ["Inventory", "Notification", "Audit & Reporting"],
    }
    # Draw links first so boxes sit on top.
    for i, t in enumerate(topics):
        y = py[i] + 28
        hot = t == "order"
        b += line(cols["p"] + cw, y, cols["t"] - 4, y, stroke=ORANGE if hot else MUTED, sw=1.75 if hot else 1.25,
                  arrow="o" if hot else "m")
        for c in links[t]:
            j = cons.index(c)
            y2 = cy[j] + 28
            x1, x2 = cols["t"] + cw, cols["c"] - 4
            mx = (x1 + x2) / 2
            b += path(f"M{x1} {y} C{mx} {y} {mx} {y2} {x2} {y2}",
                      stroke=ORANGE if hot else MUTED, sw=1.75 if hot else 1.1,
                      arrow="o" if hot else "m", opacity=1 if hot else 0.55)
    for i, p in enumerate(prods):
        b += card(cols["p"], py[i], cw, 56, p, None, title_size=16, accent=ORANGE if p == "Order" else None)
    for i, t in enumerate(topics):
        y = py[i]
        b += rect(cols["t"], y, cw, 56, fill=CARD_2, stroke=ORANGE if t == "order" else BORDER, rx=28)
        b += text(cols["t"] + cw / 2, y + 33, f"sellora.{t}.v1", size=14, font=MONO, anchor="middle")
    for j, c in enumerate(cons):
        b += card(cols["c"], cy[j], cw, 56, c, None, title_size=16)
    b += rect(64, 592, 1152, 52, fill=CARD, rx=10)
    b += text(88, 623, "Outbox on every producer  ·  deduplication on every consumer  ·  a dead-letter topic per consumer  ·  ordering by Kafka key",
              size=13.5, fill=MUTED)
    return doc(w, h, b, "Sellora event flow")


# ---------------------------------------------------------------- checkout flow
def checkout():
    w, h = 1280, 760
    b = text(64, 70, "Fraud-proof cash collection", size=28, weight=700)
    b += text(64, 98, "The core idea of Sellora. A rep cannot change what was collected, because the rep never carries the receipt.",
              size=15, fill=MUTED)
    steps = [
        ("Rep opens checkout", ["At the shop, on the phone,", "for a cash sale order."]),
        ("GPS check-in", ["Server measures the distance", "to the shop. Must be 300 m", "or less. Fix under 5 min old."]),
        ("Record cash payment", ["Only allowed while the", "check-in is valid", "(10 minutes)."]),
        ("One transaction", ["Order confirmed, payment", "saved and both events", "written to the outbox."]),
    ]
    sw_, g = 260, 32
    x0 = (w - (4 * sw_ + 3 * g)) / 2
    for i, (t, lines_) in enumerate(steps):
        x = x0 + i * (sw_ + g)
        b += rect(x, 140, sw_, 150, fill=CARD, stroke=BLUE if i == 1 else BORDER, sw=1.5 if i == 1 else 1)
        b += badge_num(x + 30, 172, i + 1)
        b += text(x + 54, 177, t, size=16, weight=600)
        for j, ln in enumerate(lines_):
            b += text(x + 20, 218 + j * 21, ln, size=13.5, fill=MUTED)
        if i < 3:
            b += line(x + sw_ + 3, 215, x + sw_ + g - 4, 215, stroke=BLUE, sw=1.75, arrow="b")
    # rejection branch under step 2
    rx = x0 + sw_ + g
    b += line(rx + sw_ / 2, 292, rx + sw_ / 2, 336, stroke=RED, sw=1.5, arrow="r", dash="4 4")
    b += rect(rx, 340, sw_, 64, fill=CARD, stroke=RED, rx=10)
    b += text(rx + 20, 366, "Too far, stale or replayed", size=14, weight=600)
    b += text(rx + 20, 388, "Rejected. No payment possible.", size=13, fill=MUTED)

    # lower lane
    sx = x0 + 3 * (sw_ + g)
    b += path(f"M{sx + sw_/2} 292 V470 H{x0 + sw_ + 4}", stroke=BLUE, sw=1.75, arrow="b")
    b += rect(x0, 436, sw_, 68, fill=CARD_2, stroke=ORANGE, rx=34)
    b += text(x0 + sw_ / 2, 466, "sellora.order.v1", size=15, font=MONO, anchor="middle")
    b += text(x0 + sw_ / 2, 488, "OrderConfirmed + PaymentRecorded", size=12, fill=MUTED, anchor="middle")

    nx = x0 + sw_ + 120
    b += path(f"M{x0 + sw_/2} 506 V600 H{nx - 4}", stroke=ORANGE, sw=1.75, arrow="o")
    b += card(nx, 566, 250, 68, "Notification", "renders one receipt", center=True)
    b += path(f"M{x0 + sw_/2} 506 V690 H{nx - 4}", stroke=ORANGE, sw=1.75, arrow="o", dash="5 5")
    b += card(nx, 660, 250, 60, "Audit log", "append-only, tamper-evident", center=True)

    ex = nx + 250 + 110
    for k, (who, y) in enumerate((("Shop owner", 540), ("Agency", 620))):
        b += path(f"M{nx + 250} 600 C{nx+300} 600 {ex-60} {y+30} {ex-4} {y+30}", stroke=AQUA, sw=1.75, arrow="a")
        b += rect(ex, y, 300, 60, fill=CARD, stroke=AQUA, sw=1.5)
        b += text(ex + 20, y + 26, f"Email to {who.lower()}", size=15, weight=600)
        b += text(ex + 20, y + 46, "same record, same moment, with GPS", size=12.5, fill=MUTED)
    return doc(w, h, b, "Sellora fraud-proof checkout flow")


# ---------------------------------------------------------------- CI/CD
def cicd():
    w, h = 1280, 500
    b = text(64, 70, "Delivery pipeline", size=28, weight=700)
    b += text(64, 98, "Same pipeline in every service repository. Nothing reaches an environment without passing CI.",
              size=15, fill=MUTED)

    def stage(x, y, wd, title, sub, acc=None):
        return card(x, y, wd, 70, title, sub, accent=acc, title_size=15.5, sub_size=12.5)

    b += text(64, 148, "EVERY PULL REQUEST", size=12, fill=MUTED, weight=600, ls=1.5)
    y = 164
    b += stage(64, y, 210, "Feature branch", "named after the Jira key")
    b += line(278, y + 35, 306, y + 35, arrow="m")
    b += stage(310, y, 210, "Review", "teammate + CodeRabbit")
    b += line(524, y + 35, 552, y + 35, arrow="m")
    # CI box
    b += rect(556, y - 10, 470, 112, fill=CARD, stroke=BLUE, sw=1.5)
    b += text(578, y + 20, "CI on GitHub Actions", size=15.5, weight=600)
    chips = ["restore", "build", "tests on real PostgreSQL + Kafka", "coverage", "SonarQube gate",
             "Docker build", "health check"]
    cx, cyy = 578, y + 36
    for c in chips:
        cw_ = approx_width(c, 12) + 20
        if cx + cw_ > 1006:
            cx, cyy = 578, cyy + 34
        p, pw = pill(cx, cyy, c, size=12, h=26, pad=10)
        b += p
        cx += pw + 8
    b += line(1030, y + 35, 1058, y + 35, arrow="b", stroke=BLUE)
    b += stage(1062, y, 154, "Merge", "into dev")

    b += text(64, 318, "EVERY MERGE", size=12, fill=MUTED, weight=600, ls=1.5)
    y = 334
    b += stage(64, y, 250, "Push to dev", "image to Docker Hub")
    b += line(318, y + 35, 346, y + 35, arrow="m")
    b += stage(350, y, 250, "Staging slot", "startup + /health check", acc=BLUE)
    b += line(604, y + 35, 632, y + 35, arrow="m")
    b += stage(636, y, 250, "Release", "pull request into main")
    b += line(890, y + 35, 918, y + 35, arrow="m")
    b += stage(922, y, 294, "Production slot", "same checks, own secrets", acc=GOOD)
    b += text(64, 450, "Also on: branch protection on main and dev  ·  Dependabot  ·  CodeQL  ·  secrets only in GitHub environments",
              size=13.5, fill=MUTED)
    return doc(w, h, b, "Sellora CI/CD pipeline")


save("banner.svg", banner())
save("stats.svg", stats())
save("architecture.svg", architecture())
save("hierarchy.svg", hierarchy())
save("event-flow.svg", events())
save("checkout-flow.svg", checkout())
save("cicd.svg", cicd())
print("ok")
