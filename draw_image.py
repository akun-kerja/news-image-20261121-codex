"""Draw the front page for Saturday, 21 November 2026.

One 1024x1024 PNG, drawn with Pillow from shapes and type only: a
masthead, a lead story on the market rout that pushed the S&P 500 into
correction with a small drawn chart scene, then five short dispatches
in two rows, an in-brief band, and a source line at the foot.
Run: python3 draw_image.py
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 232)
PANEL = (233, 228, 212)
INK = (24, 28, 34)
MUTED = (96, 100, 98)
RULE = (196, 189, 170)
RED = (168, 46, 36)
NAVY = (32, 58, 84)
GOLD = (186, 138, 54)
GREEN = (46, 110, 68)
CHART = (28, 44, 66)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def face(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def fit(text, max_width, start, bold=True, minimum=12):
    for size in range(start, minimum - 1, -1):
        f = face(size, bold)
        if d.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
    return face(minimum, bold)


def wrap(text, width, font):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if d.textbbox((0, 0), test, font=font)[2] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(text, x, y, width, font, fill=INK, leading=5, max_lines=3):
    for s in wrap(text, width, font)[:max_lines]:
        d.text((x, y), s, font=font, fill=fill)
        y += font.size + leading
    return y


def hline(y, x1=40, x2=984, fill=RULE, thick=1):
    d.line((x1, y, x2, y), fill=fill, width=thick)


def dispatch(x, y, width, number, kicker, headline, body, accent, head_size=20, body_size=12):
    d.text((x, y), number, font=face(24, True), fill=accent)
    d.text((x + 44, y + 3), kicker.upper(), font=face(10, True), fill=MUTED)
    hy = y + 24
    hf = fit(headline, width - 44, head_size, True, 14)
    hy = para(headline, x + 44, hy, width - 44, hf, fill=INK, leading=2, max_lines=2)
    para(body, x + 44, hy + 5, width - 44, face(body_size), fill=(58, 63, 64), leading=3, max_lines=3)


# Masthead
d.rectangle((0, 0, W, 8), fill=RED)
d.text((40, 24), "THE DAILY GLOBE", font=face(38, True), fill=INK)
d.text((712, 38), "SATURDAY EDITION", font=face(13, True), fill=NAVY)
hline(80, fill=INK, thick=2)
d.text((41, 92), "WORLD NEWS", font=face(13, True), fill=RED)
d.text((41, 111), "SATURDAY, 21 NOVEMBER 2026", font=face(18, True), fill=INK)
d.text((800, 114), "SIX STORIES. ONE DAY.", font=face(12, True), fill=MUTED)
hline(140, fill=INK, thick=2)

# Lead story: the market rout, with a drawn falling-chart scene.
d.rounded_rectangle((40, 154, 984, 472), radius=6, fill=PANEL)
d.rectangle((40, 154, 50, 472), fill=RED)
d.text((68, 172), "NEW YORK  •  MARKETS — FRIDAY'S CLOSE", font=face(13, True), fill=RED)
d.text((68, 198), "SELL-OFF DRAGS", font=fit("SELL-OFF DRAGS", 545, 40), fill=INK)
d.text((68, 242), "S&P INTO CORRECTION", font=fit("S&P INTO CORRECTION", 545, 40), fill=RED)
para("US stocks fall 3.7% as the AI sell-off deepens. The Nasdaq "
     "drops 5.3% and wipes out all of its 2026 gains, while the Dow "
     "joins the S&P 500 in correction territory.",
     68, 296, 545, face(17), fill=INK, leading=7, max_lines=3)
d.text((68, 420), "S&P 500 6,910  •  NASDAQ 22,618  •  FRIDAY", font=face(12, True), fill=NAVY)

# Chart scene: grid, falling bars and a red trend line.
cx0, cy0, cx1, cy1 = 648, 172, 960, 452
d.rectangle((cx0, cy0, cx1, cy1), fill=CHART)
for gy in range(cy0 + 40, cy1 - 10, 52):
    d.line((cx0 + 8, gy, cx1 - 8, gy), fill=(52, 70, 96), width=1)
bars = [210, 196, 176, 188, 158, 132, 108, 82]
bx = cx0 + 18
for bh in bars:
    d.rectangle((bx, cy1 - 30 - bh, bx + 26, cy1 - 30), fill=(214, 182, 110))
    bx += 36
d.line((cx0 + 18, cy0 + 46, cx1 - 30, cy1 - 96), fill=(214, 84, 66), width=4)
d.ellipse((cx1 - 44, cy1 - 110, cx1 - 16, cy1 - 82), fill=(214, 84, 66))
d.text((cx0 + 10, cy1 - 24), "-3.7%", font=face(13, True), fill=(232, 214, 160))
d.text((cx1 - 96, cy1 - 24), "FIVE-DAY SLIDE", font=face(11, True), fill=(200, 208, 220))
d.text((cx0 + 4, cy1 + 8), "WALL STREET, FRIDAY", font=face(11, True), fill=MUTED)

# Middle row: two dispatches.
hline(492, fill=INK, thick=2)
dispatch(40, 510, 458, "02", "Warsaw • Poland",
         "Russian missiles land in Poland; Tusk cries provocation",
         "Two missiles and a suspected drone come down on Polish "
         "soil as allies hold exercises; leaders rally to Warsaw.", RED, head_size=22, body_size=13)
d.line((502, 510, 502, 632), fill=RULE, width=1)
dispatch(524, 510, 460, "03", "Junin • Peru",
         "Magnitude 6.8 quake shakes Peru's Andes",
         "The tremor strikes the Junin region and is felt in Lima, "
         "about 320 km away, Peru's geophysical institute says.", NAVY, head_size=22, body_size=13)

# In brief: four one-line items fill the middle band.
d.rounded_rectangle((40, 644, 984, 706), radius=4, fill=PANEL)
d.text((56, 662), "IN BRIEF", font=face(12, True), fill=RED)
d.text((150, 655), "India logs record foreign inflows", font=face(12, True), fill=INK)
d.text((150, 676), "into shares in November.", font=face(12), fill=(58, 63, 64))
d.text((400, 655), "Mamdani sets 2032 to close", font=face(12, True), fill=INK)
d.text((400, 676), "New York's Rikers Island jail.", font=face(12), fill=(58, 63, 64))
d.text((620, 655), "GTA 6 sets $3.8bn record", font=face(12, True), fill=INK)
d.text((620, 676), "on its first day.", font=face(12), fill=(58, 63, 64))
d.text((820, 655), "Gen Z protests spread", font=face(12, True), fill=INK)
d.text((820, 676), "to 25 European states.", font=face(12), fill=(58, 63, 64))

# Bottom row: three dispatches.
hline(718, fill=INK, thick=2)
dispatch(40, 736, 300, "04", "Antalya • Turkiye",
         "COP31 talks run past deadline on fossil fuels",
         "Nearly 200 nations fail to agree in overtime as the "
         "climate summit stretches beyond its close.", RED, head_size=19, body_size=13)
d.line((350, 736, 350, 946), fill=RULE, width=1)
dispatch(368, 736, 300, "05", "Washington • United States",
         "FBI crime database reportedly hacked",
         "The bureau investigates a breach of its national crime "
         "database as computer outages continue in the US.", NAVY, head_size=19, body_size=13)
d.line((678, 736, 678, 946), fill=RULE, width=1)
dispatch(696, 736, 288, "06", "London • Health",
         "Cancer pill trial gives hope on pancreas",
         "The pill daraxonrasib makes tumours undetectable on scans "
         "in one in 12 patients in an early trial.", GREEN, head_size=19, body_size=13)

# Footer
hline(966, fill=INK, thick=2)
d.text((41, 978), "A DAY OF SELL-OFFS, A QUAKE, AND A SUMMIT RUNNING LATE",
       font=fit("A DAY OF SELL-OFFS, A QUAKE, AND A SUMMIT RUNNING LATE", 780, 13), fill=INK)
d.text((906, 978), "01 / 01", font=face(12, True), fill=RED)
d.text((41, 998), "Sources: One Turn world news 21 November 2026 · Horizon world news 21 November 2026 · The Daily Short 21 November 2026",
       font=fit("Sources: One Turn world news 21 November 2026 · Horizon world news 21 November 2026 · The Daily Short 21 November 2026", 940, 11, False, 9), fill=MUTED)
d.rectangle((0, 1016, W, 1024), fill=RED)

im.save("entry.png", format="PNG", optimize=True)
print("saved entry.png")
