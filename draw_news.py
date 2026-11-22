#!/usr/bin/env python3
"""The World Today - Sunday 22 November 2026.

A deterministic 1024x1024 front page drawn with PIL: 38 short,
source-checked stories across 7 regions, a schematic world map with
story markers, a markets strip and a UTC timeline. Run twice and the
output PNG is byte-identical.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: dark newsroom -----------------------------------------------
INK = (13, 17, 23)        # page background
PANEL = (24, 30, 40)      # card background
PANEL2 = (30, 38, 51)     # lighter card
RULE = (58, 70, 88)       # hairlines
TXT = (232, 236, 241)     # main text
MUT = (158, 170, 186)     # muted text
RED = (226, 62, 52)       # lead red
AMBER = (240, 180, 60)    # accent amber
GREEN = (74, 190, 120)    # up / positive
BLUE = (96, 165, 250)     # links / markers
TEAL = (45, 190, 180)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font(SERIF, 46)
F_DATE = font(SANSB, 13)
F_KICK = font(SANSB, 11)
F_LEAD = font(SANSB, 21)
F_DECK = font(SANS, 13)
F_RHEAD = font(SANSB, 12)
F_HEAD = font(SANSB, 11)
F_BODY = font(SANS, 11)
F_SRC = font(SANSB, 9)
F_SMALL = font(SANS, 10)
F_TINY = font(SANSB, 9)
F_NUM = font(SANSB, 15)
F_MKT = font(SANSB, 11)
F_TL = font(SANSB, 10)


def wrap(drw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if drw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_story(drw, x, y, col_w, story, bottom):
    """One short story: headline (max 2 lines) + source tag line.
    Returns the y position after the story, or None if it overflows."""
    head, src = story
    lines = wrap(drw, head, F_BODY, col_w)[:2]
    need = len(lines) * 13 + 12 + 5
    if y + need > bottom:
        return None
    yy = y
    for ln in lines:
        drw.text((x, yy), ln, font=F_BODY, fill=TXT)
        yy += 13
    drw.text((x, yy + 1), src + "  ", font=F_SRC, fill=AMBER)
    drw.text((x + drw.textlength(src + "  ", font=F_SRC), yy + 1),
             "✓ 22 NOV", font=F_SRC, fill=GREEN)
    return y + need


def region_header(drw, x, y, col_w, name, count):
    drw.rectangle([x, y, x + col_w, y + 17], fill=PANEL2)
    drw.rectangle([x, y, x + 4, y + 17], fill=RED)
    drw.text((x + 10, y + 3), name.upper(), font=F_RHEAD, fill=TXT)
    tag = "%d STORIES" % count
    tw = drw.textlength(tag, font=F_TINY)
    drw.text((x + col_w - tw - 6, y + 4), tag, font=F_TINY, fill=MUT)
    return y + 23


# --- the news: 38 stories, 7 regions --------------------------------------
# (headline, source tag)
REGIONS = [
    ("Middle East", [
        ("Iran hits US bases in Bahrain for the fourth time in nine days",
         "AL JAZEERA"),
        ("Two tankers struck near Strait of Hormuz as hawks press Trump",
         "NY POST"),
        ("US jets hit missile site on Iran's Qeshm Island; Tehran denies damage",
         "DEFENSE DOMAIN"),
        ("Houthi missile damages Riyadh's PIF Tower; Saudi defences down drones",
         "DEFENSE DOMAIN"),
        ("Iran stages 14-tanker convoy off Kharg Island to break US blockade",
         "DEFENSE NEWS"),
        ("Taiz under Houthi siege enters third month as civilian deaths mount",
         "AFP"),
    ]),
    ("Europe", [
        ("Russia's biggest strike of the year: 110 missiles, 400 drones hit Kyiv",
         "CNN"),
        ("Russian missiles land in Poland near NATO troop exercise; jets scrambled",
         "CNN"),
        ("Triple-tap strike kills boy, 7, and paramedic, 20, in Kryvyi Rih",
         "CNN"),
        ("Trump, Putin and Xi hold historic trilateral in Shenzhen; no breakthrough",
         "AP"),
        ("Coalition of the Willing meets in Berlin, ready for direct Moscow talks",
         "CNN"),
        ("Russian helicopter suspected of violating Finnish airspace",
         "THE INDEPENDENT"),
    ]),
    ("North America", [
        ("S&P 500 slides into correction as Nasdaq sheds 5.3% in Friday rout",
         "AP"),
        ("Nvidia chief Jensen Huang resigns; shares dive 14% in a week",
         "AP"),
        ("Anthropic shares fall 9% a day after record $81.3bn IPO debut",
         "AP"),
        ("Mexico captures cartel boss 'El Chapo Isidro'; 11 killed in operation",
         "AFP"),
        ("FBI probes second suspected breach of its crime database in months",
         "AFP"),
        ("US open to Latin American UN chief, envoy Waltz says amid gridlock",
         "AP"),
    ]),
    ("Asia-Pacific", [
        ("EU and Indonesia sign trade deal covering 730 million people",
         "DUMPLING NEWS"),
        ("Asian shares head for worst week since 2020 as AI gloom spreads",
         "STRAITS TIMES"),
        ("World Court rules Myanmar committed genocide against Rohingya",
         "AP"),
        ("Mongolia's president resigns amid street protests",
         "AFP"),
        ("China's CE-25A electric passenger plane completes first crewed flight",
         "GLOBAL NEXUS"),
        ("Japan-Russia tensions rise after two suspected airspace violations",
         "GLOBAL NEXUS"),
        ("US approved nearly 900,000 AI chips for Chinese firms on Pentagon list",
         "DUMPLING NEWS"),
    ]),
    ("Africa", [
        ("Sudan's Tasis Alliance seizes Blue Nile's key Bau region",
         "AFP"),
        ("25 migrants deported from US arrive in Liberia",
         "AFP"),
        ("Boat capsizes en route to burial in Nigeria; at least 24 dead",
         "AFP"),
        ("Next climate summit set for Addis Ababa, Ethiopia, in November 2027",
         "AP"),
    ]),
    ("Latin America", [
        ("Magnitude 6.7 quake hits Peru's Andes; no damage or casualties",
         "AFP"),
        ("Brazil lawmaker calls online strategy behind Lula win 'ethically dubious'",
         "AFP"),
        ("Colombia mine blast kills two workers; two missing as rescue goes on",
         "GLOBAL NEXUS"),
        ("El Salvador troops reclaim Haitian stadium in gang fight",
         "DUMPLING NEWS"),
        ("Three US citizens among four convicted in Honduras trafficking case",
         "AFP"),
    ]),
    ("Climate & Tech", [
        ("COP31 in Antalya goes into overtime; draft omits fossil fuels",
         "AP"),
        ("Bitcoin plunges below $56,000; Ethereum near $1,600 in crypto rout",
         "MOODVECTOR"),
        ("UN talks on lethal autonomous weapons fall short of enforceable rules",
         "UN NEWS"),
        ("Gold suffers worst week since March, down 9.2% to $3,527",
         "TOPSTEP"),
    ]),
]

MARKETS = [
    ("S&P 500", "7,176", "-7.1% wk", False),
    ("NASDAQ", "25,552", "-8.7% wk", False),
    ("DOW", "49,097", "-6.8% wk", False),
    ("GOLD", "$3,527", "-9.2% wk", False),
    ("SILVER", "$40.89", "-16.4% wk", False),
    ("BRENT", "$91", "-5.5% wk", False),
    ("WTI", "$82.45", "-5.5% wk", False),
    ("DXY", "103.97", "+0.4% wk", True),
]

TIMELINE = [
    ("02:00", "COP31 overtime"),
    ("05:30", "Asia shares slide"),
    ("08:15", "Drones hit Russian ship"),
    ("11:00", "Coalition meets Berlin"),
    ("14:00", "Streeting visits Kyiv"),
    ("18:40", "IRGC claims strikes"),
    ("20:30", "Tankers hit"),
    ("23:30", "Bahrain fire"),
]

NUMBERS = [
    ("110", "missiles fired at Kyiv in one night"),
    ("120+", "vessels attacked in Hormuz since Feb"),
    ("-7.1%", "S&P 500's week - into correction"),
    ("$3,527", "gold, worst week since March"),
    ("14", "tankers in Iran's blockade-run convoy"),
]

# Rough schematic continent outlines (lon, lat) - hand-drawn, not traced.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    # South America
    [(-78, 7), (-62, 9), (-52, 5), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-80, -3),
     (-78, 7)],
    # Africa
    [(-17, 15), (-10, 31), (10, 37), (30, 32), (35, 28), (43, 12),
     (51, 11), (48, -2), (40, -10), (36, -19), (33, -26), (20, -35),
     (15, -27), (12, -18), (9, -1), (-8, 4), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (5, 58), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 70), (45, 68), (68, 73),
     (100, 77), (130, 72), (160, 70), (178, 66), (162, 60), (142, 50),
     (140, 40), (130, 33), (122, 30), (110, 20), (105, 9), (100, 7),
     (92, 16), (88, 22), (80, 8), (76, 10), (72, 20), (66, 25),
     (60, 25), (56, 27), (52, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (30, 36), (26, 40), (23, 36), (19, 42), (12, 44),
     (3, 43), (-10, 36)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19), (150, -23),
     (153, -27), (150, -37), (140, -38), (132, -32), (124, -33), (115, -35),
     (114, -22)],
]

MARKERS = [  # (lon, lat, number)
    (50.6, 26.2, "1"), (56.5, 26.6, "2"), (30.5, 50.4, "3"),
    (46.7, 24.7, "4"), (114.1, 22.5, "5"), (30.7, 36.9, "6"),
    (-77.0, -9.0, "7"), (-10.8, 6.3, "8"), (32.5, 15.6, "9"),
    (33.4, 47.9, "10"),
]


def build():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    mx = 24  # margin

    # ---- masthead ------------------------------------------------------
    d.text((mx, 14), "THE WORLD TODAY", font=F_TITLE, fill=TXT)
    d.text((mx, 66), "SUNDAY 22 NOVEMBER 2026  •  38 STORIES  •  7 REGIONS  •  ALL SOURCE-CHECKED",
           font=F_KICK, fill=AMBER)
    d.text((W - mx - d.textlength("EDITION No. 22 — 2026", font=F_DATE), 20),
           "EDITION No. 22 — 2026", font=F_DATE, fill=MUT)
    d.text((W - mx - d.textlength("FRONT PAGE  •  1024 × 1024", font=F_DATE), 42),
           "FRONT PAGE  •  1024 × 1024", font=F_DATE, fill=MUT)
    d.rectangle([mx, 82, W - mx, 85], fill=RED)

    # ---- lead story ----------------------------------------------------
    ly, lh = 94, 74
    d.rectangle([mx, ly, W - mx, ly + lh], fill=PANEL)
    d.rectangle([mx, ly, mx + 6, ly + lh], fill=RED)
    d.text((mx + 16, ly + 8), "LEAD  •  THE GULF ON EDGE", font=F_KICK, fill=RED)
    lead = "Iran strikes US bases in Bahrain again — fourth attack in nine days"
    d.text((mx + 16, ly + 26), lead, font=F_LEAD, fill=TXT)
    deck = ("IRGC claims Patriot radar hits at al-Riffa and Awali; Bahrain says an industrial "
            "site burned, no injuries. Two tankers hit near Hormuz as a 14-ship convoy forms.")
    for i, ln in enumerate(wrap(d, deck, F_DECK, W - 2 * mx - 32)):
        d.text((mx + 16, ly + 50 + i * 15), ln, font=F_DECK, fill=MUT)

    # ---- map + by the numbers ------------------------------------------
    my, mh = 178, 116
    map_x0, map_x1 = mx, 664
    d.rectangle([map_x0, my, map_x1, my + mh], fill=PANEL)
    d.text((map_x0 + 10, my + 6), "WHERE IT HAPPENED", font=F_KICK, fill=AMBER)

    def project(lon, lat):
        px = map_x0 + 14 + (lon + 170) / 360.0 * (map_x1 - map_x0 - 28)
        py = my + 26 + (75 - lat) / 130.0 * (mh - 34)
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=PANEL2, outline=RULE)
    # graticule
    for lon in (-120, -60, 0, 60, 120):
        x0, y0 = project(lon, 75)
        x1, y1 = project(lon, -55)
        d.line([x0, y0, x1, y1], fill=(40, 48, 62), width=1)
    for num_lon, num_lat, num in MARKERS:
        cx, cy = project(num_lon, num_lat)
        if num == "10":  # Kryvyi Rih sits almost on top of Kyiv: nudge the dot
            d.line([cx, cy, cx + 12, cy + 9], fill=TXT, width=1)
            cx, cy = cx + 12, cy + 9
        if num == "1":  # Bahrain and Hormuz markers crowd each other
            d.line([cx, cy, cx - 11, cy - 8], fill=TXT, width=1)
            cx, cy = cx - 11, cy - 8
        if num == "2":
            d.line([cx, cy, cx + 11, cy - 8], fill=TXT, width=1)
            cx, cy = cx + 11, cy - 8
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=TXT, width=1)
        tw = d.textlength(num, font=F_TINY)
        d.text((cx - tw / 2, cy - 5), num, font=F_TINY, fill=TXT)

    # by the numbers
    nx0, nx1 = 676, W - mx
    d.rectangle([nx0, my, nx1, my + mh], fill=PANEL)
    d.text((nx0 + 10, my + 6), "BY THE NUMBERS", font=F_KICK, fill=AMBER)
    yy = my + 26
    for val, label in NUMBERS:
        d.text((nx0 + 10, yy), val, font=F_NUM, fill=AMBER)
        vw = d.textlength(val, font=F_NUM)
        d.text((nx0 + 16 + vw, yy + 3), label, font=F_SMALL, fill=TXT)
        yy += 18

    # ---- stories: three columns ----------------------------------------
    sy, sbot = 304, 872
    cols = [
        [REGIONS[0], REGIONS[1]],
        [REGIONS[2], REGIONS[3]],
        [REGIONS[4], REGIONS[5], REGIONS[6]],
    ]
    col_w = (W - 2 * mx - 2 * 16) // 3
    for ci, groups in enumerate(cols):
        x = mx + ci * (col_w + 16)
        y = sy
        for name, stories in groups:
            y = region_header(d, x, y, col_w, name, len(stories))
            for st in stories:
                nxt = draw_story(d, x, y, col_w, st, sbot)
                if nxt is None:
                    break
                y = nxt
            y += 6

    # ---- markets strip ---------------------------------------------------
    ky, kh = 882, 46
    d.rectangle([mx, ky, W - mx, ky + kh], fill=PANEL)
    d.text((mx + 10, ky + 6), "MARKETS — WEEK TO FRI 20 NOV", font=F_KICK, fill=AMBER)
    cell_w = (W - 2 * mx - 20) / len(MARKETS)
    yy = ky + 24
    for i, (name, val, chg, up) in enumerate(MARKETS):
        cx = mx + 10 + i * cell_w
        d.text((cx, yy), name, font=F_TINY, fill=MUT)
        d.text((cx, yy + 11), val + "  " + chg, font=F_MKT,
               fill=GREEN if up else RED)

    # ---- UTC timeline -----------------------------------------------------
    ty, th = 938, 56
    d.rectangle([mx, ty, W - mx, ty + th], fill=PANEL)
    d.text((mx + 10, ty + 5), "THE DAY IN UTC", font=F_KICK, fill=AMBER)
    d.line([mx + 10, ty + 38, W - mx - 10, ty + 38], fill=RULE, width=2)
    span = W - 2 * mx - 40
    for i, (t, label) in enumerate(TIMELINE):
        cx = mx + 20 + i * span / (len(TIMELINE) - 1)
        d.ellipse([cx - 4, ty + 34, cx + 4, ty + 42], fill=AMBER)
        tw = d.textlength(t, font=F_TL)
        d.text((cx - tw / 2, ty + 22), t, font=F_TL, fill=AMBER)
        lines = wrap(d, label, F_SMALL, 118)
        ly2 = ty + 45
        for ln in lines[:1]:
            lw = d.textlength(ln, font=F_SMALL)
            d.text((max(mx + 4, min(cx - lw / 2, W - mx - lw - 4)), ly2), ln,
                   font=F_SMALL, fill=MUT)

    # ---- footer ------------------------------------------------------------
    d.text((mx, 1002),
           "Sources: AP · Reuters · CNN · AFP · Al Jazeera · NY Post · ISW · Topstep — every story date-checked 22 Nov 2026.",
           font=F_SMALL, fill=MUT)
    d.text((mx, 1014),
           "Drawn with Python + PIL. Deterministic build: run twice, byte-identical output.",
           font=F_SMALL, fill=MUT)

    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
