#!/usr/bin/env python3
"""Regenerate the PIIIX org-profile assets from live GitHub data.

    python3 profile/forge.py            # fetch via `gh`, write data.json + SVGs
    python3 profile/forge.py --offline  # rebuild SVGs from the committed data.json

Every number on the profile page (commits, merged PRs, last commit, the light
curve) comes from profile/data.json, which this script writes from the API.
Status words are the only hand-set field, in BODIES below.
"""
import json, math, os, random, subprocess, sys, collections, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
DATA = os.path.join(HERE, "data.json")
ORG = "PIIIX-org"

# ---- palette: sampled from the org avatar and piiix.org tokens.color.css ----
GROUND = "#0b0a09"
INK = "#f5f9fb"
STARS = "#d8d4cf"
MUTED = "#a8a29b"
RULE = "#434241"
ORANGE = "#fd9f13"
AMBER = "#ffc048"
RED = "#e62706"

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# ---- the bodies. orbit = distance from "shipped" (inner = closer). ----
BODIES = [
    dict(key="git-a-profile", name="git-a-profile", repo="git-a-profile", kind="planet",
         status="done", role="README forge", public=True, orbit=1),
    dict(key="elara", name="Elara", repo="chapters", kind="planet",
         status="in testing", role="second brain", public=True, orbit=2),
    dict(key="yildizim", name="Yildizim", repo="yildizim", kind="moon", moon_of="elara",
         status="prototype, paused", role="galaxy view for Elara", public=False),
    dict(key="inter-face", name="inter.face", repo="inter.face", kind="planet",
         status="in testing", role="art direction pipeline", public=True, orbit=3),
    dict(key="website-pitch-pipeline", name="website-pitch-pipeline", repo="website-pitch-pipeline",
         kind="planet", status="process being reworked", role="demo-site outreach", public=True, orbit=4),
    dict(key="vectory", name="Vectory", repo="vectory", kind="comet",
         status="on hold until funded", role="canvas that writes HTML/CSS", public=True),
]
BY_KEY = {b["key"]: b for b in BODIES}

# ---------------------------------------------------------------- data ----

def gh(*args):
    return subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=True).stdout

def fetch():
    out = {"fetched": dt.date.today().isoformat(), "bodies": {}}
    for b in BODIES:
        r = b["repo"]
        dates = gh("--paginate", f"repos/{ORG}/{r}/commits?per_page=100", "--jq", ".[].commit.author.date").split()
        days = sorted(dt.date.fromisoformat(x[:10]) for x in dates)
        weeks = collections.Counter((d - dt.timedelta(days=d.weekday())).isoformat() for d in days)
        prs = int(gh(f"search/issues?q=repo:{ORG}/{r}+is:pr+is:merged", "--jq", ".total_count"))
        meta = json.loads(gh(f"repos/{ORG}/{r}", "--jq", "{created_at,language,private}"))
        out["bodies"][b["key"]] = dict(
            commits=len(days), merged_prs=prs, first=days[0].isoformat(), last=days[-1].isoformat(),
            created=meta["created_at"][:10], language=meta["language"], private=meta["private"],
            weekly=dict(sorted(weeks.items())))
    return out

# -------------------------------------------------------------- helpers ----

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def write(name, svg):
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", os.path.relpath(path, HERE))

def starfield(w, h, n, seed, cls="tw"):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.5, 0.6, 0.8, 1.0, 1.3])
        o = rnd.uniform(0.25, 0.9)
        anim = f' class="{cls}" style="animation-delay:-{rnd.uniform(0, 6):.1f}s"' if rnd.random() < 0.18 else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{STARS}" opacity="{o:.2f}"{anim}/>')
    return "\n".join(out)

REDUCED = "@media (prefers-reduced-motion: reduce){ .spin,.tw,.pulse,.trace{animation:none !important} }"

def radius(commits):
    return 3 + 1.6 * math.log(max(commits, 1))

# ----------------------------------------------------------------- hero ----

def hero(data):
    W, H = 1200, 480
    CX, CY = 720, 250
    SQ = 0.38  # orbital plane tilt
    ORBITS = {1: 120, 2: 200, 3: 275, 4: 345}
    PERIOD = {1: 26, 2: 38, 3: 52, 4: 68}      # seconds per revolution
    PHASE = {1: 200, 2: 320, 3: 40, 4: 130}    # static start angle, degrees
    g = []
    g.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img"
  aria-labelledby="t d"><title id="t">The PIIIX system</title>
  <desc id="d">An orange star with four planets on tilted orbits: git-a-profile closest, then Elara with its moon Yildizim, inter.face, and website-pitch-pipeline. Vectory is a comet parked at the far end of a long dashed orbit. Distance from the star is distance from shipped.</desc>
  <style>
    .spin{{animation:spin linear infinite; transform-origin:0 0}}
    .rev{{animation-direction:reverse}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .tw{{animation:tw 6s ease-in-out infinite}}
    @keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
    .pulse{{animation:pulse 7s ease-in-out infinite; transform-origin:{CX}px {CY}px}}
    @keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.06)}}}}
    text{{font-family:{MONO}; fill:{INK}}}
    .serif{{font-family:{SERIF}}}
    .mut{{fill:{MUTED}}}
    {REDUCED}
  </style>
  <defs>
    <radialGradient id="star"><stop offset="0" stop-color="#fff6e5"/><stop offset=".35" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/></radialGradient>
    <radialGradient id="corona"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".55"/><stop offset=".5" stop-color="{ORANGE}" stop-opacity=".12"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
    <radialGradient id="planet" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="{INK}"/><stop offset=".6" stop-color="{STARS}"/><stop offset="1" stop-color="#6b6864"/></radialGradient>
    <radialGradient id="dim" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="{MUTED}"/><stop offset="1" stop-color="#3a3836"/></radialGradient>
    <linearGradient id="tail" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{STARS}" stop-opacity=".7"/><stop offset="1" stop-color="{STARS}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="{GROUND}"/>
  {starfield(W, H, 170, 3)}''')

    # orbits (drawn flat, in the tilted plane)
    for k, rx in ORBITS.items():
        g.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{rx*SQ:.1f}" fill="none" stroke="{STARS}" stroke-opacity=".22" stroke-width="1"/>')

    # comet orbit: star at the right focus; aphelion at x=110
    a, e = 345, 0.78
    c = a * e
    bb = a * math.sqrt(1 - e * e)
    g.append(f'<ellipse cx="{CX - c:.1f}" cy="{CY}" rx="{a}" ry="{bb*SQ:.1f}" fill="none" stroke="{STARS}" stroke-opacity=".28" stroke-width="1" stroke-dasharray="3 7"/>')

    # the star
    g.append(f'<g class="pulse"><circle cx="{CX}" cy="{CY}" r="110" fill="url(#corona)"/></g>')
    g.append(f'<circle cx="{CX}" cy="{CY}" r="26" fill="url(#star)"/>')

    def planet_group(b, d):
        r = radius(d["commits"])
        fill = "url(#planet)"
        inner = [f'<circle r="{r:.1f}" fill="{fill}"/>']
        # label
        inner.append(f'<text x="{r+8:.0f}" y="4" font-size="12" class="serif">{esc(b["name"])}</text>')
        # moon: unlabeled in motion; named in the planet's own label instead
        for m in BODIES:
            if m.get("moon_of") == b["key"]:
                mr = 3.2
                md = r + 14
                inner.append(f'''<ellipse rx="{md}" ry="{md*SQ:.1f}" fill="none" stroke="{STARS}" stroke-opacity=".3" stroke-width=".8"/>
<g transform="scale(1,{SQ})"><g class="spin" style="animation-duration:9s"><g transform="translate({md},0)"><g class="spin rev" style="animation-duration:9s"><g transform="scale(1,{1/SQ:.3f})">
<circle r="{mr}" fill="url(#dim)"/>
</g></g></g></g></g>''')
        return "\n".join(inner)

    for b in BODIES:
        if b["kind"] != "planet":
            continue
        d = data["bodies"][b["key"]]
        rx, T, ph = ORBITS[b["orbit"]], PERIOD[b["orbit"]], PHASE[b["orbit"]]
        g.append(f'''<g transform="translate({CX},{CY}) scale(1,{SQ}) rotate({ph})">
  <g class="spin" style="animation-duration:{T}s"><g transform="translate({rx},0)">
    <g class="spin rev" style="animation-duration:{T}s"><g transform="rotate({-ph}) scale(1,{1/SQ:.3f})">
      {planet_group(b, d)}
    </g></g>
  </g></g>
</g>''')

    # the comet, parked at aphelion, tail away from the star
    cx_c = CX - c - a
    v = BY_KEY["vectory"]
    g.append(f'''<g transform="translate({cx_c:.1f},{CY})">
  <path d="M0,-2 L-80,-11 L-80,11 L0,2 Z" fill="url(#tail)" opacity=".8"/>
  <circle r="4.5" fill="url(#planet)"/>
  <text x="10" y="-10" font-size="12" class="serif">{esc(v["name"])}</text>
</g>''')
    g.append(f'''<text x="48" y="64" font-size="40" class="serif" letter-spacing="3">PIIIX</text>
</svg>''')
    write("system.svg", "\n".join(g))

# ------------------------------------------------------------ ephemeris ----

def ephemeris(data):
    """One almanac row per body: the tag system of this page."""
    W, H = 900, 44
    for b in BODIES:
        d = data["bodies"][b["key"]]
        cols = [("status", b["status"]), ("commits", str(d["commits"])),
                ("merged PRs", str(d["merged_prs"])), ("first light", d["first"]),
                ("last commit", d["last"]), ("source", "public" if not d["private"] else "private")]
        warn = b["key"] == "vectory"
        dot = RED if warn else ORANGE
        x = 250
        cells = []
        for label, val in cols:
            cells.append(f'<text x="{x}" y="15" font-size="8.5" class="mut" letter-spacing="1">{esc(label.upper())}</text>'
                         f'<text x="{x}" y="31" font-size="12">{esc(val)}</text>')
            x += 112 if label != "status" else 150
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(b['name'])} ephemeris: {esc(', '.join(f'{l} {v}' for l, v in cols))}">
<style>text{{font-family:{MONO};fill:{INK}}} .serif{{font-family:{SERIF}}} .mut{{fill:{MUTED}}}
.spin{{animation:spin 8s linear infinite;transform-origin:0 0}} @keyframes spin{{to{{transform:rotate(360deg)}}}} {REDUCED}</style>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<line x1="0" y1=".5" x2="{W}" y2=".5" stroke="{RULE}"/><line x1="0" y1="{H-.5}" x2="{W}" y2="{H-.5}" stroke="{RULE}"/>
<g transform="translate(22,{H/2})"><ellipse rx="11" ry="4.2" fill="none" stroke="{STARS}" stroke-opacity=".4"/><circle r="2.6" fill="{ORANGE}"/>
<g transform="scale(1,.38)"><g class="spin"><circle cx="11" cy="0" r="2.2" fill="{dot}"/></g></g></g>
<text x="44" y="27" font-size="15" class="serif">{esc(b["name"])}</text>
{''.join(cells)}
</svg>'''
        write(f"ephemeris/{b['key']}.svg", svg)

    # the almanac header: the page-level tags
    rows = [("LICENSE", "MIT"), ("CONTRIBUTING", "fork · PR · sign the CLA"), ("BODIES", str(len(BODIES))), ("STAR", "1")]
    x = 44
    cells = []
    for l, v in rows:
        cells.append(f'<text x="{x}" y="15" font-size="8.5" class="mut" letter-spacing="1">{l}</text><text x="{x}" y="31" font-size="12">{esc(v)}</text>')
        x += 90 if l != "CONTRIBUTING" else 220
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="PIIIX almanac: license MIT, contributing by fork, pull request and CLA, {len(BODIES)} bodies, 1 star">
<style>text{{font-family:{MONO};fill:{INK}}} .mut{{fill:{MUTED}}}</style>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<line x1="0" y1=".5" x2="{W}" y2=".5" stroke="{RULE}"/><line x1="0" y1="{H-.5}" x2="{W}" y2="{H-.5}" stroke="{RULE}"/>
<circle cx="22" cy="{H/2}" r="5" fill="{ORANGE}"/>
{''.join(cells)}
</svg>'''
    write("almanac.svg", svg)

# ----------------------------------------------------------- light curve ----

def lightcurve(data):
    """Commits per week per body, drawn the way photometry sheets plot a variable star."""
    weeks_all = sorted({w for b in data["bodies"].values() for w in b["weekly"]})
    start = dt.date.fromisoformat(weeks_all[0])
    end = dt.date.fromisoformat(data["fetched"])
    end -= dt.timedelta(days=end.weekday())
    weeks = []
    w = start
    while w <= end:
        weeks.append(w)
        w += dt.timedelta(days=7)
    L, R, T, ROW, GAP = 220, 40, 44, 40, 10
    W = 900
    H = T + len(BODIES) * (ROW + GAP) + 36
    px = (W - L - R) / max(len(weeks) - 1, 1)
    g = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="lt ld">
<title id="lt">Light curve: commits per week per body</title>
<desc id="ld">{esc('; '.join(f"{b['name']}: {data['bodies'][b['key']]['commits']} commits, last {data['bodies'][b['key']]['last']}" for b in BODIES))}</desc>
<style>text{{font-family:{MONO};fill:{INK}}} .serif{{font-family:{SERIF}}} .mut{{fill:{MUTED}}}
.trace{{stroke-dasharray:2000;stroke-dashoffset:2000;animation:draw 3s ease-out forwards}} @keyframes draw{{to{{stroke-dashoffset:0}}}} {REDUCED}
@media (prefers-reduced-motion: reduce){{.trace{{stroke-dashoffset:0}}}}</style>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<text x="24" y="24" font-size="14" class="serif">Light curve</text>
''']
    # month ticks
    for i, wk in enumerate(weeks):
        if wk.day <= 7:
            x = L + i * px
            g.append(f'<line x1="{x:.1f}" y1="{T-6}" x2="{x:.1f}" y2="{H-30}" stroke="{RULE}" stroke-dasharray="1 3"/>')
            g.append(f'<text x="{x:.1f}" y="{H-14}" font-size="9.5" class="mut" text-anchor="middle">{wk.strftime("%b")}</text>')
    y = T
    for b in BODIES:
        d = data["bodies"][b["key"]]
        peak = max(d["weekly"].values())
        base = y + ROW
        g.append(f'<line x1="{L}" y1="{base}" x2="{W-R}" y2="{base}" stroke="{RULE}"/>')
        g.append(f'<text x="24" y="{y+18}" font-size="13" class="serif">{esc(b["name"])}</text>')
        pts = []
        for i, wk in enumerate(weeks):
            v = d["weekly"].get(wk.isoformat(), 0)
            pts.append((L + i * px, base - (ROW - 6) * v / peak))
        poly = " ".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)
        area = f"{L},{base} " + poly + f" {pts[-1][0]:.1f},{base}"
        stroke = RED if b["kind"] == "comet" else (MUTED if "paused" in b["status"] else ORANGE)
        g.append(f'<polygon points="{area}" fill="{stroke}" opacity=".12"/>')
        g.append(f'<polyline class="trace" points="{poly}" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')
        for (x, yy), wk in zip(pts, weeks):
            if d["weekly"].get(wk.isoformat(), 0):
                g.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="1.8" fill="{INK}"/>')
        y += ROW + GAP
    g.append("</svg>")
    write("lightcurve.svg", "\n".join(g))

# --------------------------------------------------------------- footer ----

def footer(data):
    W, H = 1200, 120
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The PIIIX star low on a dark horizon">
<style>text{{font-family:{MONO};fill:{MUTED}}} .serif{{font-family:{SERIF};fill:{INK}}} .tw{{animation:tw 6s ease-in-out infinite}} @keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}} {REDUCED}</style>
<defs><radialGradient id="star"><stop offset="0" stop-color="#fff6e5"/><stop offset=".35" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/></radialGradient>
<radialGradient id="corona"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".5"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
<clipPath id="sky"><rect width="{W}" height="{H-28}"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
{starfield(W, H-30, 70, 11)}
<g clip-path="url(#sky)"><circle cx="{W-160}" cy="{H-26}" r="70" fill="url(#corona)"/><circle cx="{W-160}" cy="{H-26}" r="18" fill="url(#star)"/></g>
<rect y="{H-28}" width="{W}" height="28" fill="#141312"/>
<line x1="0" y1="{H-28}" x2="{W}" y2="{H-28}" stroke="{RULE}"/>
<text x="48" y="52" font-size="22" class="serif">PIIIX</text>
</svg>'''
    write("footer.svg", svg)

# ----------------------------------------------------------------- main ----

if __name__ == "__main__":
    if "--offline" in sys.argv:
        data = json.load(open(DATA))
    else:
        data = fetch()
        json.dump(data, open(DATA, "w"), indent=1)
        print("wrote data.json")
    hero(data)
    ephemeris(data)
    lightcurve(data)
    footer(data)
