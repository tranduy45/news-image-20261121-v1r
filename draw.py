"""News-image-20261121 v1r: draws Saturday 21 November 2026's world news
as one 1024x1024 front page, from wire-verified facts.

Layout (my own design): masthead, region bar, number strip, timeline,
3 hero stories, 12 small cards, a world map, an ALSO list of 21 more
stories, and a DATE CHECK strip for items first reported on 19-20 Nov
that must not be presented as 21 Nov news.

Every headline and brief below was written fresh in this session from
wire reports read today. No text was copied from any earlier entry.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (176, 30, 40)
GRAY = (90, 90, 90)
RULE = (201, 194, 180)
GOLD = (184, 134, 11)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        raise RuntimeError("font missing: " + path)
    return ImageFont.truetype(path, size)


def wrap_text(text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- data

SUBLINE = ("Russia strikes Ukraine anew  \u00b7  COP31 runs into overtime  "
           "\u00b7  Rahul's hundred puts India on top")

REGIONS = [
    ("EUROPE", 9, (31, 78, 121)),
    ("ASIA-PACIFIC", 13, (176, 30, 40)),
    ("AMERICAS", 5, (46, 125, 50)),
    ("OCEANIA", 3, (184, 134, 11)),
    ("MIDEAST", 4, (106, 61, 154)),
    ("AFRICA", 2, (69, 90, 100)),
]

NUMBERS = [
    ("2", "dead in the Kryvyi Rih strike"),
    ("$8bn", "EU payout to Ukraine"),
    ("110", "Rahul's hundred, Wellington"),
    ("$14bn", "Taiwan arms sale awaits OK"),
    ("600", "women killed in S. Africa"),
    ("10,000", "Rohingya to resettle"),
]

TIMELINE = ("OVERNIGHT  Missiles hit Kryvyi Rih   \u00b7   MORNING  COP31 into "
            "overtime   \u00b7   LUNCH  Rahul 93*, India 239/1   \u00b7   "
            "EVENING  Denmark plot")

# num, city, tag, region, headline, brief, source
HEROES = [
    (1, "KYIV", "WAR", "EUROPE",
     "Russia pounds Ukraine anew",
     "Overnight strikes hit Kryvyi Rih: 2 dead, 42 hurt, four of them "
     "children; Kyiv's bridges are hit again after Putin vowed retaliation.",
     "AP  \u00b7  REUTERS  \u00b7  CONFIRMED"),
    (2, "ANTALYA", "CLIMATE", "EUROPE",
     "COP31 runs into overtime",
     "Talks slip past Friday's deadline with no deal; a third draft is due "
     "Saturday, fossil-fuel language stripped and the $120bn target dropped.",
     "REUTERS  \u00b7  AP  \u00b7  CONFIRMED"),
    (3, "WELLINGTON", "SPORT", "OCEANIA",
     "Rahul's hundred puts India on top",
     "KL Rahul makes 110 and Padikkal 78 not out as India reach 288/1 on "
     "Day 3, chasing New Zealand's 368 at the Basin Reserve.",
     "REUTERS  \u00b7  ANI  \u00b7  CONFIRMED"),
]

CARDS = [
    (4, "WASHINGTON", "POLITICS", "AMERICAS",
     "Trump floats Miller for 2028",
     "Trump jokingly asks his new chief of staff if he wants the top job.",
     "AFP"),
    (5, "TEHRAN", "DIPLOMACY", "MIDEAST",
     "Iran seeks a deal; Trump says no",
     "Tehran says it still wants diplomacy; Trump calls its terms unacceptable.",
     "REUTERS"),
    (6, "HODEIDAH", "MIDEAST", "MIDEAST",
     "Houthis claim more Saudi strikes",
     "Rebels claim strikes on Saudi targets after jets hit Hodeidah port.",
     "AP  \u00b7  DAWN"),
    (7, "BRUSSELS", "EUROPE", "EUROPE",
     "EU demands a seat at Ukraine talks",
     "European leaders press US envoys for a place at the table on Ukraine.",
     "DAWN"),
    (8, "COPENHAGEN", "EUROPE", "EUROPE",
     "Denmark names a Russian murder plot",
     "Moscow plotted to kill a US-Ukrainian rapper, Denmark says.",
     "AP"),
    (9, "WARSAW", "EUROPE", "EUROPE",
     "Poland calls it a provocation",
     "Missiles and a drone land in the south-east; Tusk cries provocation.",
     "AP"),
    (10, "DHAKA", "ASIA", "ASIA-PACIFIC",
     "Arson flares in Bangladesh unrest",
     "Fresh attacks erupt as Hasina's planned return from exile stirs unrest.",
     "AP"),
    (11, "WASHINGTON", "TECH", "AMERICAS",
     "Trump backs Huang's return",
     "Trump repeats his call for the ousted chip chief to return; the board says no.",
     "NST"),
    (12, "ULAANBAATAR", "ASIA", "ASIA-PACIFIC",
     "Mongolia's president quits",
     "Khurelsukh quits amid graft claims; a snap vote follows.",
     "AP"),
    (13, "DOHA", "SPORT", "ASIA-PACIFIC",
     "Shaheens rout UAE in Rising Stars",
     "Defending champions open the Asia Cup with a 61-run win in Doha.",
     "DAWN"),
    (14, "GAZA", "MIDEAST", "MIDEAST",
     "Israeli forces kill 3 in Gaza push",
     "Strikes in central Gaza kill three Palestinians in a fresh operation, medics say.",
     "DAWN"),
    (15, "NAYPYIDAW", "ASIA", "ASIA-PACIFIC",
     "Myanmar rejects genocide ruling",
     "Naypyidaw calls the world court's genocide finding unfair; the vote was 9\u20136.",
     "AP"),
]

# num, city, one-line item (kept short so each fits two lines)
ALSO = [
    (16, "KUALA LUMPUR", "Malaysia to resettle 10,000 Rohingya in T\u00fcrkiye"),
    (17, "JAKARTA", "Prabowo, Xi launch trade partnership talks"),
    (18, "EUROPE", "Youth march in 25 countries over living costs"),
    (19, "KYIV", "EU pays out a record \u20ac7.9bn to Ukraine"),
    (20, "HODEIDAH", "UN warns port strikes threaten Yemen aid"),
    (21, "ISLAMABAD", "Pakistan take Blind Asia Cup after washout"),
    (22, "DUBLIN", "Ireland thrash Pakistan by nine wickets"),
    (23, "SYDNEY", "Cummins camp hits out at \u2018hysteria\u2019"),
    (24, "MANCHESTER", "Pochettino vows to rebuild Utd \u2018from scratch\u2019"),
    (25, "BRASILIA", "Lula recognises Raoni\u2019s ancestral land"),
    (26, "SHENZHEN", "Trump, Xi, Putin hail \u2018historic\u2019 summit"),
    (27, "TOKYO", "Japan to buy 8m barrels of Saudi crude"),
    (28, "WASHINGTON", "AI firms back child-safety charter"),
    (29, "TOKYO", "China\u2019s snub may boost Takaichi at home"),
    (30, "NEW DELHI", "India \u2018takes note\u2019 of the G-3 summit"),
    (31, "ABUJA", "Tinubu seeks end to jail for suicide bids"),
    (32, "S. AFRICA", "581 women killed in three months"),
    (33, "NEW DELHI", "Indian seafarer still missing after tanker attack"),
    (34, "TAIPEI", "Taiwan awaits $14bn arms sale OK"),
    (35, "WASHINGTON", "Measles cases climb after US loses status"),
    (36, "CANBERRA", "Australia eases backpacker visa curbs"),
]

DATE_CHECK = ("Left out on purpose \u2014 first reported before Saturday: "
    "Anthropic\u2019s day-two plunge  \u00b7  Riemann claim  \u00b7  "
    "Shenzhen summit  \u00b7  Gupta sentence  \u00b7  Pete Rose "
    "pardon  \u00b7  Senate 51\u201348 Iran vote  \u00b7  ICJ Myanmar "
    "ruling  \u00b7  Riyadh tower strike  \u00b7  Hormuz tanker "
    "fire  \u00b7  EU \u20ac1bn aid  \u00b7  US Iran sanctions  "
    "\u00b7  GTA VI $2.36bn  \u00b7  NZ 368  \u00b7  Senegal boat")

FOOTER = ("Attested: every date checked against wire reports on 21 November "
    "2026. Sources: Reuters, AP, AFP, BBC, Dawn, The Hindu, NST, Manila "
    "Times, UN News. Original flat drawings, not photographs.")

# map dots: (lon, lat) for stories 1-15, equirectangular projection
MAP_DOTS = {
    1: (30.5, 50.4), 2: (30.7, 36.9), 3: (174.8, -41.3),
    4: (-77.0, 38.9), 5: (51.4, 35.7), 6: (42.9, 14.8),
    7: (4.4, 50.8), 8: (12.6, 55.7), 9: (21.0, 52.2),
    10: (90.4, 23.8), 11: (-77.0, 38.0), 12: (106.9, 47.9),
    13: (51.5, 25.3), 14: (34.5, 31.5), 15: (96.1, 19.8),
}

# rough continent outlines, (lon, lat) points, drawn as filled blobs
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
     (-70, 45), (-80, 32), (-90, 21), (-105, 20), (-115, 30), (-125, 40),
     (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 5), (-50, -5), (-40, -20), (-55, -35), (-70, -55),
     (-75, -40), (-80, -15), (-80, 10)],
    [(-10, 36), (-5, 44), (0, 50), (10, 57), (20, 60), (30, 70), (40, 68),
     (30, 60), (20, 55), (10, 45), (0, 40), (-10, 36)],
    [(-17, 15), (-10, 30), (10, 37), (30, 32), (43, 12), (50, 10),
     (40, -5), (35, -20), (20, -35), (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(40, 68), (60, 70), (90, 75), (120, 73), (150, 70), (170, 66),
     (160, 60), (140, 45), (130, 35), (120, 25), (105, 10), (95, 8),
     (85, 20), (75, 25), (60, 25), (50, 30), (40, 40), (40, 68)],
    [(113, -22), (125, -12), (142, -11), (150, -22), (150, -37),
     (140, -38), (130, -32), (115, -33), (113, -22)],
]


# ---------------------------------------------------------------- helpers

class Checker:
    """Collects layout violations while drawing; render() reports them."""

    def __init__(self):
        self.problems = []

    def text_block(self, label, lines, font, width, max_lines, box_h,
                   used_h):
        for line in lines:
            if font.getlength(line) > width + 0.5:
                self.problems.append(
                    "%s: line too wide: %r" % (label, line))
        if len(lines) > max_lines:
            self.problems.append(
                "%s: %d lines, max %d" % (label, len(lines), max_lines))
        if used_h > box_h + 0.5:
            self.problems.append(
                "%s: block %.1fpx tall, box %.1fpx" % (label, used_h, box_h))


def draw_wrapped(d, x, y, lines, font, fill, leading):
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, font, bg, fg):
    w = font.getlength(text) + 12
    bbox = font.getbbox(text)
    h = (bbox[3] - bbox[1]) + 8
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + 6, y + 4), text, font=font, fill=fg)
    return w


# ---------------------------------------------------------------- art

def art_hero(d, num, x, y, w, h):
    """Flat illustration panel for one hero story."""
    x, y, w, h = int(x), int(y), int(w), int(h)
    if num == 1:
        d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
        # skyline: dark blocks with lit windows
        for bx, bw, bh in ((8, 42, 52), (58, 30, 70), (96, 48, 44),
                           (152, 34, 62), (194, 44, 50), (246, 38, 66),
                           (292, 22, 40)):
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                        fill=(8, 12, 26))
            for wy in range(y + h - bh + 8, y + h - 6, 14):
                for wx in range(x + bx + 6, x + bx + bw - 4, 12):
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 196, 66))
        # explosions
        for ex, ey, r in ((70, 26, 9), (210, 18, 7), (270, 34, 8)):
            d.ellipse([x + ex - r, y + ey - r, x + ex + r, y + ey + r],
                      fill=(255, 140, 40))
            d.ellipse([x + ex - r // 2, y + ey - r // 2,
                       x + ex + r // 2, y + ey + r // 2],
                      fill=(255, 220, 120))
        f = load_font("DejaVuSans-Bold.ttf", 11)
        chip(d, x + 8, y + 8, "2 DEAD \u00b7 42 HURT", f, RED, (255, 255, 255))
        chip(d, x + w - 92, y + 8, "OVERNIGHT", f, (40, 40, 40),
             (255, 255, 255))
        lab = "KRYVYI RIH"
        lf = load_font("DejaVuSans-Bold.ttf", 12)
        d.rectangle([x + w - 118, y + h - 22, x + w - 4, y + h - 4],
                    fill=(8, 12, 26))
        d.text((x + w - 112, y + h - 20), lab, font=lf,
               fill=(255, 196, 66))
    elif num == 2:
        d.rectangle([x, y, x + w, y + h], fill=(14, 94, 94))
        cx, cy, r = x + 62, y + 52, 40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 120))
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 200, 330,
                   fill=(40, 120, 60))
        d.line([cx, cy, cx + r, cy - 6], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        f = load_font("DejaVuSans-Bold.ttf", 11)
        chip(d, x + 128, y + 8, "3RD DRAFT DUE SAT", f, RED, (255, 255, 255))
        d.text((x + 140, y + 38), "OVERTIME",
               font=load_font("DejaVuSans-Bold.ttf", 20), fill=(255, 255, 255))
        d.text((x + 140, y + 62), "NO DEAL",
               font=load_font("DejaVuSans-Bold.ttf", 20), fill=(255, 220, 80))
        # thermometer
        d.rounded_rectangle([x + w - 26, y + 14, x + w - 14, y + h - 26],
                            radius=6, fill=(255, 255, 255))
        d.rounded_rectangle([x + w - 24, y + h - 40, x + w - 16, y + h - 28],
                            radius=4, fill=RED)
        d.ellipse([x + w - 30, y + h - 26, x + w - 10, y + h - 6], fill=RED)
        d.text((x + 14, y + h - 22), "144 \u2192 80",
               font=load_font("DejaVuSans-Bold.ttf", 14), fill=(255, 255, 255))
    else:
        d.rectangle([x, y, x + w, y + h], fill=(150, 110, 60))
        d.rectangle([x, y, x + w, y + 16], fill=(60, 120, 60))
        d.rectangle([x + 30, y + 30, x + w - 30, y + h - 14],
                    fill=(190, 150, 90))
        d.line([x + 30, y + 52, x + w - 30, y + 52], fill=(255, 255, 255),
               width=2)
        for sx in (150, 162, 174):
            d.rectangle([x + sx, y + 34, x + sx + 5, y + 52],
                        fill=(255, 220, 80))
        d.ellipse([x + 240, y + 62, x + 254, y + 76], fill=(200, 30, 30))
        d.text((x + 16, y + 30), "110",
               font=load_font("DejaVuSerif-Bold.ttf", 44),
               fill=(255, 255, 255))
        d.text((x + w - 74, y + h - 22), "288/1",
               font=load_font("DejaVuSans-Bold.ttf", 14), fill=(255, 220, 80))


def art_card(d, num, x, y, w, h):
    """Small flat illustration for one of the 12 cards."""
    x, y, w, h = int(x), int(y), int(w), int(h)
    f = load_font("DejaVuSans-Bold.ttf", 15)
    if num == 4:
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        d.text((x + 8, y + 6), "2028", font=load_font("DejaVuSerif-Bold.ttf", 26),
               fill=(255, 210, 90))
        for i in range(5):
            d.text((x + 8 + i * 16, y + h - 18), "\u2605", font=f,
                   fill=(255, 255, 255))
        d.rectangle([x, y + h - 6, x + w, y + h], fill=RED)
    elif num == 5:
        for i, col in enumerate(((178, 34, 34), (255, 255, 255),
                                 (178, 34, 34), (255, 255, 255),
                                 (178, 34, 34))):
            d.rectangle([x, y + i * h // 5, x + w // 2, y + (i + 1) * h // 5],
                        fill=col)
        d.rectangle([x + w // 2, y, x + w, y + h // 3], fill=(0, 122, 61))
        d.rectangle([x + w // 2, y + h // 3, x + w, y + 2 * h // 3],
                    fill=(255, 255, 255))
        d.rectangle([x + w // 2, y + 2 * h // 3, x + w, y + h],
                    fill=(200, 30, 30))
        d.ellipse([x + w // 2 + 22, y + h // 2 - 9, x + w // 2 + 40,
                   y + h // 2 + 9], outline=RED, width=2)
    elif num == 6:
        d.rectangle([x, y, x + w, y + h], fill=(20, 90, 90))
        cx, cy, r = x + w // 2, y + h // 2, 20
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255),
                  width=3)
        d.line([cx - r - 6, cy, cx + r + 6, cy], fill=(255, 255, 255), width=2)
        d.line([cx, cy - r - 6, cx, cy + r + 6], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    elif num == 7:
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        import math
        cx, cy = x + w // 2, y + h // 2
        for k in range(12):
            a = math.radians(k * 30 - 90)
            sx, sy = cx + int(26 * math.cos(a)), cy + int(18 * math.sin(a))
            d.text((sx - 4, sy - 7), "\u2605",
                   font=load_font("DejaVuSans.ttf", 11), fill=(255, 210, 0))
    elif num == 8:
        d.rectangle([x, y, x + w, y + h], fill=(200, 30, 40))
        d.rectangle([x + w // 2 - 6, y, x + w // 2 + 6, y + h],
                    fill=(255, 255, 255))
        d.rectangle([x, y + h // 2 - 6, x + w, y + h // 2 + 6],
                    fill=(255, 255, 255))
    elif num == 9:
        d.rectangle([x, y, x + w, y + h], fill=(60, 64, 70))
        d.polygon([(x + 30, y + 12), (x + 120, y + 12), (x + 132, y + h // 2),
                   (x + 120, y + h - 12), (x + 30, y + h - 12)],
                  fill=(200, 200, 200))
        d.polygon([(x + 132, y + h // 2), (x + 148, y + h // 2 - 8),
                   (x + 148, y + h // 2 + 8)], fill=RED)
        d.polygon([(x + 30, y + 12), (x + 14, y + 4), (x + 22, y + h // 2)],
                  fill=(255, 140, 40))
        d.text((x + 52, y + h // 2 - 10), "KH-101",
               font=load_font("DejaVuSans-Bold.ttf", 12), fill=(40, 40, 40))
    elif num == 10:
        d.rectangle([x, y, x + w, y + h], fill=(50, 30, 20))
        cx = x + w // 2
        d.polygon([(cx, y + 6), (cx + 22, y + h - 12), (cx - 22, y + h - 12)],
                  fill=(255, 120, 20))
        d.polygon([(cx, y + 24), (cx + 11, y + h - 12), (cx - 11, y + h - 12)],
                  fill=(255, 220, 80))
    elif num == 11:
        d.rectangle([x, y, x + w, y + h], fill=(10, 10, 10))
        d.line([x + 10, y + 12, x + 60, y + 12, x + 60, y + 34, x + 120,
                y + 34], fill=(0, 200, 80), width=2)
        d.line([x + 10, y + 40, x + 40, y + 40, x + 40, y + h - 10],
               fill=(0, 200, 80), width=2)
        for px, py in ((60, 12), (120, 34), (40, 40)):
            d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3],
                      fill=(0, 200, 80))
        d.text((x + 88, y + h - 22), "NVDA", font=f, fill=(0, 220, 90))
    elif num == 12:
        d.rectangle([x, y, x + w, y + h], fill=(31, 78, 121))
        d.rectangle([x + 52, y + 14, x + 102, y + h - 10], fill=(255, 255, 255))
        d.rectangle([x + 66, y + 20, x + 88, y + 26], fill=NAVY)
    elif num == 13:
        d.rectangle([x, y, x + w, y + h], fill=(0, 100, 60))
        for sx in (62, 72, 82):
            d.rectangle([x + sx, y + 10, x + sx + 4, y + 32],
                        fill=(255, 220, 80))
        d.ellipse([x + 112, y + 30, x + 124, y + 42], fill=(200, 30, 30))
        d.text((x + 8, y + h - 20), "SHAHEENS",
               font=load_font("DejaVuSans-Bold.ttf", 11), fill=(255, 255, 255))
    elif num == 14:
        d.rectangle([x, y, x + w, y + h], fill=(70, 70, 78))
        for bx, bw, bh in ((10, 34, 34), (50, 28, 44), (84, 36, 30),
                           (124, 22, 40)):
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                        fill=(40, 40, 48))
            for wy in range(y + h - bh + 6, y + h - 4, 10):
                for wx in range(x + bx + 5, x + bx + bw - 5, 10):
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 196, 66))
    else:
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        cx = x + w // 2
        d.line([cx, y + 8, cx, y + h - 10], fill=(255, 210, 90), width=3)
        d.line([cx - 30, y + 16, cx + 30, y + 16], fill=(255, 210, 90), width=3)
        for s in (-1, 1):
            d.arc([cx + s * 30 - 14, y + 16, cx + s * 30 + 14, y + 40],
                  0, 180, fill=(255, 210, 90), width=3)
            d.line([cx + s * 30 - 14, y + 28, cx + s * 30 + 14, y + 28],
                   fill=(255, 210, 90), width=2)


def draw_map(d, x, y, w, h, chk):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + 6), "WHERE IT HAPPENED",
           font=load_font("DejaVuSans-Bold.ttf", 11), fill=(255, 255, 255))
    mx, my, mw, mh = x + 6, y + 24, w - 12, h - 30

    def proj(lon, lat):
        return (mx + (lon + 180) / 360.0 * mw,
                my + (90 - lat) / 180.0 * mh)

    for blob in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in blob]
        d.polygon(pts, fill=(210, 180, 130))
    fnum = load_font("DejaVuSans-Bold.ttf", 8)
    for num, (lon, lat) in MAP_DOTS.items():
        px, py = proj(lon, lat)
        if num == 11:  # nudge off Washington DC (story 4 sits there)
            px += 10
            py += 12
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = fnum.getlength(str(num))
        d.text((px - tw / 2, py - 5), str(num), font=fnum,
               fill=(255, 255, 255))
    d.text((x + 8, y + h - 14), "Red numbers mark stories 1\u201315.",
           font=load_font("DejaVuSans.ttf", 9), fill=(200, 200, 200))


# ---------------------------------------------------------------- render

def render():
    chk = Checker()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([5, 5, W - 6, H - 6], outline=NAVY, width=2)

    M = 22                      # side margin
    CW = W - 2 * M              # content width

    # ---- top meta line
    f_meta = load_font("DejaVuSans.ttf", 11)
    f_meta_b = load_font("DejaVuSans-Bold.ttf", 11)
    d.text((M, 12), "No. 21  \u00b7  make.fun", font=f_meta, fill=GRAY)
    right = "36 STORIES  \u00b7  6 REGIONS  \u00b7  ONE PAGE"
    d.text((W - M - f_meta_b.getlength(right), 12), right, font=f_meta_b,
           fill=RED)

    # ---- masthead
    f_title = load_font("DejaVuSerif-Bold.ttf", 46)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - f_title.getlength(t)) / 2, 30), t, font=f_title, fill=RED)
    f_date = load_font("DejaVuSerif-Bold.ttf", 50)
    t = "SATURDAY 21 NOVEMBER 2026"
    d.text(((W - f_date.getlength(t)) / 2, 78), t, font=f_date, fill=NAVY)
    f_sub = load_font("DejaVuSans.ttf", 13)
    chk.text_block("subline", [SUBLINE], f_sub, CW, 1, 16, 16)
    d.text(((W - f_sub.getlength(SUBLINE)) / 2, 130), SUBLINE, font=f_sub,
           fill=RED)

    # ---- region bar
    y = 148
    total = sum(c for _, c, _ in REGIONS)
    rx = M
    f_reg = load_font("DejaVuSans-Bold.ttf", 11)
    for name, count, col in REGIONS:
        seg_w = CW * count / total
        d.rectangle([rx, y, rx + seg_w, y + 20], fill=col)
        label = "%s %d" % (name, count)
        d.text((rx + (seg_w - f_reg.getlength(label)) / 2, y + 4), label,
               font=f_reg, fill=(255, 255, 255))
        rx += seg_w

    # ---- number strip
    y = 172
    cell_w = CW / 6
    f_num = load_font("DejaVuSerif-Bold.ttf", 30)
    f_lab = load_font("DejaVuSans.ttf", 10)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * cell_w
        d.text((cx + (cell_w - f_num.getlength(num)) / 2, y + 2), num,
               font=f_num, fill=NAVY)
        lines = wrap_text(lab, f_lab, cell_w - 12)
        chk.text_block("number %s" % num, lines, f_lab, cell_w - 12, 2, 24,
                       len(lines) * 13)
        draw_wrapped(d, cx + 6, y + 36, lines, f_lab, GRAY, 13)
        if i:
            d.line([cx, y + 4, cx, y + 52], fill=RULE, width=1)
    d.line([M, y + 56, W - M, y + 56], fill=INK, width=1)

    # ---- timeline
    y = 236
    f_tl_b = load_font("DejaVuSans-Bold.ttf", 11)
    f_tl = load_font("DejaVuSans.ttf", 11)
    chk.text_block("timeline", [TIMELINE], f_tl, W - M - (M + 190), 1, 16, 16)
    d.text((M, y), "SATURDAY BY THE HOURS", font=f_tl_b, fill=RED)
    d.text((M + 190, y), TIMELINE, font=f_tl, fill=INK)
    d.line([M, y + 18, W - M, y + 18], fill=INK, width=1)

    # ---- heroes
    hy = 262
    hw = (CW - 20) / 3
    f_kick = load_font("DejaVuSans-Bold.ttf", 11)
    f_head = load_font("DejaVuSans-Bold.ttf", 19)
    f_brief = load_font("DejaVuSans.ttf", 12)
    f_src = load_font("DejaVuSans.ttf", 10)
    for i, (num, city, tag, _reg, head, brief, src) in enumerate(HEROES):
        hx = M + i * (hw + 10)
        art_hero(d, num, hx, hy, hw, 88)
        ky = hy + 96
        d.text((hx, ky), "%d  \u00b7  %s  \u00b7  %s" % (num, city, tag),
               font=f_kick, fill=RED)
        hlines = wrap_text(head, f_head, hw)
        chk.text_block("hero %d headline" % num, hlines, f_head, hw, 2, 48,
                       len(hlines) * 24)
        draw_wrapped(d, hx, ky + 16, hlines, f_head, INK, 24)
        blines = wrap_text(brief, f_brief, hw)
        chk.text_block("hero %d brief" % num, blines, f_brief, hw, 3, 45,
                       len(blines) * 15)
        draw_wrapped(d, hx, ky + 16 + len(hlines) * 24 + 4, blines, f_brief,
                     INK, 15)
        d.text((hx, ky + 16 + len(hlines) * 24 + 4 + len(blines) * 15 + 4),
               src, font=f_src, fill=GRAY)

    # ---- 12 small cards, two rows of six
    card_w = (CW - 50) / 6
    f_chead = load_font("DejaVuSans-Bold.ttf", 13)
    f_cbrief = load_font("DejaVuSans.ttf", 11)
    f_csrc = load_font("DejaVuSans.ttf", 9)
    for row in range(2):
        cy = 470 + row * 152
        for col in range(6):
            num, city, tag, _reg, head, brief, src = CARDS[row * 6 + col]
            cx = M + col * (card_w + 10)
            art_card(d, num, cx, cy, card_w, 48)
            ky = cy + 54
            d.text((cx, ky), "%d  \u00b7  %s" % (num, city),
                   font=f_kick, fill=RED)
            hlines = wrap_text(head, f_chead, card_w)
            chk.text_block("card %d headline" % num, hlines, f_chead,
                           card_w, 2, 34, len(hlines) * 17)
            draw_wrapped(d, cx, ky + 14, hlines, f_chead, INK, 17)
            blines = wrap_text(brief, f_cbrief, card_w)
            chk.text_block("card %d brief" % num, blines, f_cbrief, card_w,
                           3, 44, len(blines) * 14)
            draw_wrapped(d, cx, ky + 14 + len(hlines) * 17 + 3, blines,
                         f_cbrief, INK, 14)
            d.text((cx, ky + 14 + len(hlines) * 17 + 3 + len(blines) * 14 + 3),
                   src, font=f_csrc, fill=GRAY)

    # ---- map + ALSO list
    my = 782
    map_w = 300
    draw_map(d, M, my, map_w, 164, chk)
    ax = M + map_w + 14
    aw = W - M - ax
    f_also_h = load_font("DejaVuSans-Bold.ttf", 12)
    d.text((ax, my), "ALSO ON SATURDAY 21 NOVEMBER", font=f_also_h, fill=RED)
    f_also = load_font("DejaVuSans.ttf", 10)
    col_w = (aw - 20) / 3
    for i, (num, city, text) in enumerate(ALSO):
        col, r = divmod(i, 7)
        ix = ax + col * (col_w + 10)
        iy = my + 18 + r * 22
        line = "%d. %s \u2014 %s" % (num, city, text)
        lines = wrap_text(line, f_also, col_w)
        chk.text_block("also %d" % num, lines, f_also, col_w, 2, 22,
                       len(lines) * 11)
        draw_wrapped(d, ix, iy, lines, f_also, INK, 11)

    # ---- DATE CHECK strip
    dy = 958
    f_dc_b = load_font("DejaVuSans-Bold.ttf", 11)
    f_dc = load_font("DejaVuSans.ttf", 10)
    d.rectangle([M, dy, W - M, dy + 40], outline=RED, width=1)
    d.text((M + 8, dy + 3), "DATE CHECK", font=f_dc_b, fill=RED)
    dc_lines = wrap_text(DATE_CHECK, f_dc, CW - 16)
    chk.text_block("date check", dc_lines, f_dc, CW - 16, 2, 24,
                   len(dc_lines) * 12)
    draw_wrapped(d, M + 8, dy + 16, dc_lines, f_dc, INK, 12)

    # ---- footer
    f_ft = load_font("DejaVuSans.ttf", 9)
    chk.text_block("footer", [FOOTER], f_ft, CW, 1, 12, 12)
    d.text(((W - f_ft.getlength(FOOTER)) / 2, 1004), FOOTER, font=f_ft,
           fill=GRAY)

    return img, chk.problems


if __name__ == "__main__":
    image, problems = render()
    for p in problems:
        print("OVERFLOW:", p)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    image.save(out, format="PNG")
    print("wrote", out, image.size, os.path.getsize(out), "bytes")
    print("problems:", len(problems))
