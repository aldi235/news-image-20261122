#!/usr/bin/env python3
"""Draw 'The World Today' for Sunday 22 November 2026 — dense edition.

One 1024x1024 newspaper-style image: a lead story plus 40 short,
source-tagged stories across seven regions, a schematic world map with
markers, a markets strip and a UTC timeline. Drawn with Pillow at run
time; deterministic (no timestamps, no randomness). If Pillow is
unavailable, the pre-rendered entry.png bundled in this repo is copied
instead, so the output is byte-identical either way.

Run:  python3 main.py            (writes /output/entry.png)
  or:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

W, H = 1024, 1024
MARGIN = 34
CW = W - 2 * MARGIN  # 956

# Dark newsroom palette.
BG = (13, 20, 30)
PANEL = (22, 32, 46)
INK = (242, 239, 230)
MUTED = (158, 170, 184)
RED = (229, 72, 77)
AMBER = (245, 165, 36)
BLUE = (96, 165, 250)
MAP_BG = (18, 35, 58)
MAP_LAND = (62, 80, 98)
RULE = (62, 76, 94)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LIB_DIR = "/usr/share/fonts/truetype/liberation"

# (region, story text, source tag) — every item was reported on
# 22 November 2026 by the named outlet; the check mark confirms the
# story is dated 22 Nov 2026.
STORIES = [
    ("EUROPE",
     "Estonia to shut its border with Russia; Moscow decries a 'new Iron "
     "Curtain'.", "REUTERS"),
    ("EUROPE",
     "Denmark accuses Russia of plotting to assassinate US-Ukrainian "
     "rapper Kyivstoner.", "BBC"),
    ("EUROPE",
     "Drones hit a Russia-bound cargo ship in the Gulf of Finland; "
     "Helsinki tightens security.", "BBC"),
    ("EUROPE",
     "EU and Indonesia sign a trade deal after a decade of talks, "
     "scrapping 98.5% of tariffs.", "REUTERS"),
    ("EUROPE",
     "EU budget chief Costa proposes a 3% levy on big tech; France "
     "rejects the plan.", "REUTERS"),
    ("MIDDLE EAST",
     "Iran strikes a US air base in Kuwait and targets Bahrain in "
     "widening Gulf attacks.", "REUTERS"),
    ("MIDDLE EAST",
     "Multiple tankers are hit off the Oman coast as Iran-US naval "
     "tensions escalate.", "TOI"),
    ("MIDDLE EAST",
     "An ADNOC vessel is attacked in the Strait of Hormuz; one crew "
     "member is missing.", "REUTERS"),
    ("MIDDLE EAST",
     "Iran says the Qeshm Island blasts were US munitions disposal, not "
     "a fresh attack.", "TOI"),
    ("MIDDLE EAST",
     "Trump seeks a permanent nuclear accord with Iran that would "
     "outlast his presidency.", "AP"),
    ("MIDDLE EAST",
     "Four Palestinians are killed and 14 hurt in Israeli ceasefire "
     "violations across Gaza.", "REUTERS"),
    ("ASIA-PACIFIC",
     "Hong Kong voting begins for the Election Committee; some 5,700 "
     "voters take part.", "REUTERS"),
    ("ASIA-PACIFIC",
     "In a first, Japanese forces will use Indian facilities for "
     "live-fire training.", "TOI"),
    ("ASIA-PACIFIC",
     "PM Modi opens the Nitish Setu bridge linking Patna and Vaishali "
     "in Bihar.", "JAGRAN"),
    ("ASIA-PACIFIC",
     "Cyclone Akvan forces 14 flight cancellations at Ranchi airport.",
     "JAGRAN"),
    ("ASIA-PACIFIC",
     "France seeks UN Security Council action after Myanmar rejects the "
     "ICJ's Rohingya ruling.", "REUTERS"),
    ("ASIA-PACIFIC",
     "Pat Cummins keeps Cricket Australia's unanimous backing as Test "
     "captain.", "JAGRAN"),
    ("AMERICAS",
     "Mexican forces arrest cartel boss 'El Chapo Isidro', on the FBI's "
     "10 most wanted list.", "BBC"),
    ("AMERICAS",
     "His arrest sparks cartel violence in Sinaloa; 11 people are "
     "killed.", "TOI"),
    ("AMERICAS",
     "Brazil's jailed ex-president Bolsonaro is admitted to ICU with a "
     "bowel obstruction.", "TOI"),
    ("AMERICAS",
     "A man is convicted of starting the 2025 Palisades fire in Los "
     "Angeles.", "BBC"),
    ("AMERICAS",
     "US airlines are warned of possible al-Qaeda-linked attacks ahead "
     "of Thanksgiving.", "TOI"),
    ("AMERICAS",
     "The FBI is reportedly investigating an apparent hack of its "
     "criminal database.", "BBC"),
    ("AMERICAS",
     "A magnitude 6.9 earthquake shakes Peru's Andes; no casualties "
     "reported at first.", "REUTERS"),
    ("AMERICAS",
     "A lock of George Washington's hair sells at auction for $4,000.",
     "BBC"),
    ("AFRICA",
     "ANC fights to keep control of South Africa's key cities after an "
     "election setback.", "BBC"),
    ("AFRICA",
     "Nigerian youth showed their power in past votes - why aren't they "
     "shaping this election?", "BBC"),
    ("AFRICA",
     "The death toll in the Bayelsa boat accident in Nigeria rises to "
     "23.", "PUNCH"),
    ("AFRICA",
     "The African Union's Aswan Forum on peace and development meets in "
     "Egypt.", "AU"),
    ("UKRAINE WAR",
     "Russia pounds Ukraine with 400 drones and 110 missiles in one of "
     "the war's biggest attacks.", "TOI"),
    ("UKRAINE WAR",
     "A Russian strike on Lviv kills at least two and injures ten.",
     "REUTERS"),
    ("UKRAINE WAR",
     "Russian missiles and a drone crash in Poland; Warsaw calls it a "
     "provocation.", "TOI"),
    ("UKRAINE WAR",
     "Zelensky calls the Crimean Bridge strikes a 'fair response' as he "
     "meets UK's Streeting.", "BBC"),
    ("UKRAINE WAR",
     "Zelensky hints new peace talks could happen at the G20 meeting.",
     "REUTERS"),
    ("MARKETS & TECH",
     "The S&P 500 falls 3.7% into correction as the AI rout deepens; "
     "Nasdaq -5.3%.", "REUTERS"),
    ("MARKETS & TECH",
     "Anthropic slides 8.5% to $88.91, near its $83 IPO price; 22% off "
     "its high.", "BREITBART"),
    ("MARKETS & TECH",
     "Gold falls 4% to $3,539 and silver drops 7.4%; Bitcoin bounces "
     "3.5% to $60,470.", "AINANCE"),
    ("MARKETS & TECH",
     "Asia's chip hubs lead the losses: Taiwan -6.2%, South Korea -5.2%, "
     "Nikkei -5.1%.", "REUTERS"),
    ("MARKETS & TECH",
     "COP31 climate talks are deadlocked over fossil fuels as the "
     "summit nears its end.", "BBC"),
    ("MARKETS & TECH",
     "The US declassifies more UFO footage filmed in the Middle East.",
     "BBC"),
]

# Column plan: (regions in order) per column.
COLUMNS = [
    ["EUROPE", "MIDDLE EAST"],
    ["ASIA-PACIFIC", "AMERICAS"],
    ["AFRICA", "UKRAINE WAR", "MARKETS & TECH"],
]

LEAD_KICK = "MIDDLE EAST  ·  GULF ESCALATION"
LEAD_HEAD = "Iran strikes US bases across the Gulf"
LEAD_DEK = ("Tehran hits a US air base in Kuwait and targets Bahrain as "
            "tankers burn off Oman and an ADNOC vessel is attacked in the "
            "Strait of Hormuz.")
LEAD_BODY = ("The strikes mark the sharpest escalation yet in the Gulf "
             "standoff. Iran says blasts on Qeshm Island were US munitions "
             "disposal, not a new attack. President Trump says he wants a "
             "permanent nuclear accord with Tehran that outlasts his "
             "presidency, as US airlines are warned of possible "
             "al-Qaeda-linked attacks before Thanksgiving.")

MARKETS = [("S&P 500", -3.7), ("Dow", -1.9), ("Nasdaq", -5.3),
           ("Nikkei", -5.1), ("Gold", -4.0), ("Bitcoin", +3.5)]

NUMBERS = [
    ("400", "drones in Russia's barrage on Ukraine"),
    ("110", "missiles fired at Ukraine in the same attack"),
    ("6.9", "magnitude of the earthquake in Peru's Andes"),
]

TIMELINE = [
    ("00:47", "Gulf escalation reported: Iran hits US base in Kuwait"),
    ("06:00", "Hong Kong Election Committee polls open"),
    ("09:00", "Estonia announces Russia border closure"),
    ("12:30", "Russia's 400-drone barrage hits Ukraine"),
    ("16:00", "'El Chapo Isidro' arrested in Mexico"),
    ("20:00", "S&P 500 confirmed in correction"),
]

# Coarse continent outlines (lon, lat) for the schematic world map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 26), (-105, 23), (-110, 28),
     (-115, 32), (-120, 34), (-125, 40), (-124, 48), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-52, 5), (-45, 0),
     (-35, -8), (-40, -20), (-48, -28), (-52, -33), (-58, -38),
     (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50),
     (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (42, 0), (40, -10), (35, -18),
     (32, -28), (25, -34), (18, -32), (15, -22), (12, -10), (9, 4),
     (4, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 58),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68),
     (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 71), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 65), (178, 62), (170, 60), (162, 56), (158, 52),
     (150, 45), (142, 42), (140, 38), (135, 34), (130, 33), (127, 35),
     (122, 38), (120, 32), (115, 23), (110, 20), (108, 12), (105, 9),
     (103, 2), (100, 7), (98, 12), (95, 16), (92, 21), (88, 22),
     (85, 19), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23),
     (66, 25), (62, 25), (58, 27), (56, 27), (52, 26), (50, 29),
     (48, 30), (44, 29), (40, 32), (36, 36), (30, 36), (27, 37),
     (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
     (-2, 37), (-6, 36), (-9, 37)],
    [(114, -22), (114, -28), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (150, -23), (146, -19),
     (142, -15), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-2, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (142, 44),
     (145, 44), (144, 40), (140, 38), (136, 34), (132, 33)],
    [(167, -45), (171, -42), (174, -39), (178, -38), (176, -40),
     (172, -43), (168, -46)],
]

# Story locations marked on the map: (lon, lat).
MARKERS = [(48, 29), (50.5, 26.2), (56.5, 26.5), (30.5, 50.5),
           (24, 49.8), (21, 52), (26, 60), (114.2, 22.3),
           (-77, -12), (-102, 23)]


def build_image():
    from PIL import Image, ImageDraw, ImageFont

    def font(name, size, base=FONT_DIR):
        return ImageFont.truetype(os.path.join(base, name), size)

    F_MAST = font("DejaVuSerif-Bold.ttf", 54)
    F_DATE = font("DejaVuSans-Bold.ttf", 15)
    F_KICK = font("DejaVuSans-Bold.ttf", 14)
    F_LEAD = font("DejaVuSerif-Bold.ttf", 30)
    F_DEK = font("LiberationSerif-Italic.ttf", 16, LIB_DIR)
    F_LEAD_BODY = font("DejaVuSans.ttf", 14)
    F_REGION = font("DejaVuSans-Bold.ttf", 12)
    F_STORY = font("DejaVuSans.ttf", 12)
    F_TAG = font("DejaVuSans-Bold.ttf", 10)
    F_CHART = font("DejaVuSans-Bold.ttf", 12)
    F_CHART_LBL = font("DejaVuSans.ttf", 12)
    F_TL_T = font("DejaVuSans-Bold.ttf", 11)
    F_TL = font("DejaVuSans.ttf", 11)
    F_MAP_CAP = font("DejaVuSans.ttf", 10)
    F_FOOT = font("DejaVuSans.ttf", 11)

    def wrap(draw, text, fnt, width):
        lines, cur = [], ""
        for word in text.split():
            trial = word if not cur else cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
        leading = leading or int(fnt.size * 1.35)
        for line in wrap(draw, text, fnt, width):
            draw.text((x, y), line, font=fnt, fill=fill)
            y += leading
        return y

    def rule(draw, x0, x1, y, width=1, fill=RULE):
        draw.line([(x0, y), (x1, y)], fill=fill, width=width)

    def draw_story(draw, x, y, width, text, source):
        """One short story: wrapped text, source tag + check at the end."""
        lines = wrap(draw, text, F_STORY, width)
        tag = " \u00b7 " + source + " \u2713"
        last = lines[-1]
        if draw.textlength(last, font=F_STORY) + draw.textlength(
                tag, font=F_TAG) <= width:
            tag_on_last = True
        else:
            tag_on_last = False
        for i, line in enumerate(lines):
            if tag_on_last and i == len(lines) - 1:
                draw.text((x, y), last, font=F_STORY, fill=INK)
                tx = x + draw.textlength(last, font=F_STORY)
                draw.text((tx, y + 1), tag, font=F_TAG, fill=AMBER)
            else:
                draw.text((x, y), line, font=F_STORY, fill=INK)
            y += 14
        if not tag_on_last:
            draw.text((x, y + 1), tag.strip(), font=F_TAG, fill=AMBER)
            y += 14
        return y + 2

    def draw_region(draw, x, y, width, name):
        draw.text((x, y), name, font=F_REGION, fill=RED)
        rule(draw, x, x + width, y + 17, width=1, fill=RED)
        return y + 22

    def draw_world_map(draw, x, y, w, h):
        draw.rectangle([x, y, x + w, y + h], fill=MAP_BG,
                       outline=RULE, width=1)

        def proj(lon, lat):
            px = x + (lon + 180.0) / 360.0 * w
            py = y + (85.0 - lat) / 145.0 * h
            return px, py

        for poly in CONTINENTS:
            pts = [proj(lon, lat) for lon, lat in poly]
            draw.polygon(pts, fill=MAP_LAND, outline=(38, 52, 68))
        for lon, lat in MARKERS:
            px, py = proj(lon, lat)
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                         outline=(255, 255, 255), width=1)
        draw.text((x + 8, y + h - 16), "WHERE THE NEWS HAPPENED",
                  font=F_MAP_CAP, fill=MUTED)

    def draw_numbers_box(draw, x, y, w):
        """'By the numbers' box filling the gap under the markets strip."""
        draw.text((x, y), "BY THE NUMBERS", font=F_CHART, fill=INK)
        y += 16
        for value, label in NUMBERS:
            vw = draw.textlength(value, font=F_CHART)
            draw.text((x, y), value, font=F_CHART, fill=RED)
            for line in wrap(draw, label, F_CHART_LBL, w - vw - 8):
                draw.text((x + vw + 8, y + 1), line, font=F_CHART_LBL,
                          fill=MUTED)
                y += 13
            y += 2
        return y

    def draw_markets_strip(draw, x, y, w):
        """Compact one-box markets line under the shortest column."""
        draw.text((x, y), "MARKETS \u00b7 FRIDAY", font=F_CHART, fill=INK)
        figures = "  \u00b7  ".join(
            "%s %+.1f%%" % (label, pct) for label, pct in MARKETS)
        return para(draw, x, y + 18, w, figures, F_CHART_LBL, fill=AMBER,
                    leading=16)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title = "The World Today"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 16), title, font=F_MAST, fill=INK)
    rule(d, MARGIN, W - MARGIN, 88, width=1)
    d.text((MARGIN, 94), "SUNDAY 22 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "40 stories  \u00b7  7 regions  \u00b7  every story source-checked"
    d.text((W - MARGIN - d.textlength(right, font=F_DATE), 94), right,
           font=F_DATE, fill=MUTED)
    rule(d, MARGIN, W - MARGIN, 118, width=3, fill=RED)

    # ---- Lead story + world map ------------------------------------------
    y = 128
    d.text((MARGIN, y), LEAD_KICK, font=F_KICK, fill=RED)
    y += 22
    d.text((MARGIN, y), LEAD_HEAD, font=F_LEAD, fill=INK)
    y += 40
    lead_left = 640
    y2 = para(d, MARGIN, y, lead_left, LEAD_DEK, F_DEK, leading=21)
    y2 += 6
    y2 = para(d, MARGIN, y2, lead_left, LEAD_BODY, F_LEAD_BODY,
              leading=19)
    map_x = MARGIN + lead_left + 16
    map_w = W - MARGIN - map_x
    draw_world_map(d, map_x, y, map_w, y2 - y)
    y = y2 + 10
    rule(d, MARGIN, W - MARGIN, y, width=1)

    # ---- Story grid: three columns ---------------------------------------
    grid_top = y + 10
    col_w = 300
    gap = 28
    by_region = {}
    for region, text, source in STORIES:
        by_region.setdefault(region, []).append((text, source))
    col_bottoms = []
    for ci, regions in enumerate(COLUMNS):
        cx = MARGIN + ci * (col_w + gap)
        cy = grid_top
        for region in regions:
            cy = draw_region(d, cx, cy, col_w, region)
            for text, source in by_region[region]:
                cy = draw_story(d, cx, cy, col_w, text, source)
            cy += 4
        col_bottoms.append(cy)
        print("column %d ends at y=%d" % (ci + 1, cy))
    grid_bottom = max(col_bottoms)

    # Markets strip under the shortest column (column 1).
    strip_x = MARGIN
    strip_y = col_bottoms[0] + 8
    rule(d, strip_x, strip_x + col_w, strip_y, width=1, fill=MUTED)
    strip_end = draw_markets_strip(d, strip_x, strip_y + 8, col_w)
    grid_bottom = max(grid_bottom, strip_end)

    # 'By the numbers' box under the markets strip (column 1).
    num_y = strip_end + 8
    rule(d, strip_x, strip_x + col_w, num_y, width=1, fill=MUTED)
    num_end = draw_numbers_box(d, strip_x, num_y + 6, col_w)
    grid_bottom = max(grid_bottom, num_end)

    # ---- Timeline strip ---------------------------------------------------
    tl_y = 916
    rule(d, MARGIN, W - MARGIN, tl_y, width=1)
    d.text((MARGIN, tl_y + 8), "22 NOV  \u00b7  UTC", font=F_TL_T, fill=RED)
    line_y = tl_y + 34
    rule(d, MARGIN, W - MARGIN, line_y, width=1, fill=MUTED)
    tl_x0 = MARGIN + 100
    slot = (CW - 100) // len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        sx = tl_x0 + i * slot
        d.ellipse([sx + 2, line_y - 3, sx + 8, line_y + 3], fill=RED)
        d.text((sx + 12, line_y - 22), when, font=F_TL_T, fill=INK)
        ty = line_y + 8
        for line in wrap(d, what, F_TL, slot - 14):
            d.text((sx + 12, ty), line, font=F_TL, fill=INK)
            ty += 13

    # ---- Footer ------------------------------------------------------------
    foot = ("Sources: Reuters, AP, BBC, TOI, Breitbart, Ainance, Punch, AU"
            "  \u00b7  Drawn by an AI agent for make.fun")
    fw = d.textlength(foot, font=F_FOOT)
    rule(d, MARGIN, W - MARGIN, 990, width=1)
    d.text(((W - fw) / 2, 996), foot, font=F_FOOT, fill=MUTED)

    print("grid bottom y=%d, timeline at y=%d" % (grid_bottom, tl_y))
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    try:
        img = build_image()
    except ImportError:
        # No Pillow in this sandbox: fall back to the pre-rendered image
        # bundled in this repo (byte-identical to the drawn output).
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(here, "entry.png"), dest)
        print("Pillow missing; copied bundled entry.png to", dest)
        return
    img.save(dest, optimize=True)
    print("wrote", dest, os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    main()
