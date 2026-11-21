"""Draw the World News front page for Saturday 21 November 2026.

Reads nothing but the DejaVu fonts on this machine and writes
entry.png: a 1024x1024 newspaper front page with a masthead, the six
lead stories of the day, and an in-brief box. Deterministic output:
same bytes on every run.
"""

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
MARGIN = 48
CONTENT = WIDTH - 2 * MARGIN

NAVY = (13, 27, 62)
NAVY_LIGHT = (203, 212, 232)
GOLD = (198, 148, 42)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (96, 96, 96)
BOX = (240, 240, 236)
RULE = (205, 205, 205)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def wrap(draw, text, font, width):
    """Split text into lines that fit width, measured with the font."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, font, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    # Masthead: navy band, paper name and date.
    draw.rectangle([0, 0, WIDTH, 116], fill=NAVY)
    title = ImageFont.truetype(SERIF_BOLD, 62)
    date = ImageFont.truetype(SANS, 22)
    draw.text((WIDTH / 2, 14), "WORLD NEWS", font=title,
              fill="white", anchor="ma")
    draw.text((WIDTH / 2, 84), "SATURDAY, 21 NOVEMBER 2026", font=date,
              fill=NAVY_LIGHT, anchor="ma")
    draw.rectangle([0, 116, WIDTH, 120], fill=GOLD)

    # Lead story: the markets rout.
    y = 140
    kicker = ImageFont.truetype(SANS_BOLD, 20)
    headline = ImageFont.truetype(SERIF_BOLD, 40)
    summary = ImageFont.truetype(SANS, 22)
    draw.text((MARGIN, y), "MARKETS", font=kicker, fill=RED)
    y += 30
    lead_head = wrap(draw, "Stocks plunge as Wall Street rout deepens",
                     headline, CONTENT)
    y = draw_lines(draw, lead_head, headline, MARGIN, y, INK, 44)
    lead_sum = wrap(
        draw,
        "The S&P 500 fell 3.7% into correction territory and the Nasdaq "
        "dropped 5.3%, wiping out its gains for 2026.",
        summary, CONTENT)
    y = draw_lines(draw, lead_sum, summary, MARGIN, y + 6, GREY, 27)
    y += 12
    draw.line([MARGIN, y, WIDTH - MARGIN, y], fill=RULE, width=2)
    y += 12

    # The other five stories, one block each.
    stories = [
        ("EUROPE", "Russian missiles land in Poland",
         "Prime Minister Donald Tusk called it a deliberate provocation."),
        ("PERU", "Magnitude 6.8 quake strikes Junín",
         "The tremor shook central Peru and was felt across Lima."),
        ("CLIMATE", "COP31 misses fossil-fuel deadline",
         "Negotiators blew past the deadline for a fossil-fuel deal."),
        ("UNITED STATES", "FBI crime database reportedly hacked",
         "Reports said attackers breached the bureau's crime database."),
        ("HEALTH", "Pancreatic cancer trial shows promise",
         "Daraxonrasib left tumours undetectable in one in twelve patients."),
    ]
    kicker_small = ImageFont.truetype(SANS_BOLD, 17)
    head_small = ImageFont.truetype(SERIF_BOLD, 28)
    sum_small = ImageFont.truetype(SANS, 20)
    for tag, head, text in stories:
        draw.text((MARGIN, y), tag, font=kicker_small, fill=RED)
        y += 20
        head_lines = wrap(draw, head, head_small, CONTENT)
        y = draw_lines(draw, head_lines, head_small, MARGIN, y, INK, 32)
        sum_lines = wrap(draw, text, sum_small, CONTENT)
        y = draw_lines(draw, sum_lines, sum_small, MARGIN, y + 2, GREY, 24)
        y += 10
        draw.line([MARGIN, y, WIDTH - MARGIN, y], fill=RULE, width=1)
        y += 10

    # In-brief box: four short items in two columns. It ends a little
    # above the footer so the two never touch.
    box_top = y + 2
    box_bottom = HEIGHT - 36
    draw.rectangle([MARGIN, box_top, WIDTH - MARGIN, box_bottom], fill=BOX)
    brief_head = ImageFont.truetype(SANS_BOLD, 20)
    brief_text = ImageFont.truetype(SANS, 19)
    draw.text((MARGIN + 16, box_top + 12), "IN BRIEF",
              font=brief_head, fill=NAVY)
    briefs = [
        "India posts record foreign investment inflows.",
        "Mamdani pledges to close Rikers by 2032.",
        "GTA 6 sets a $3.8bn first-day sales record.",
        "Gen Z protests spread across 25 European states.",
    ]
    col_w = (CONTENT - 32 - 24) // 2
    row_y = box_top + 46
    for i, item in enumerate(briefs):
        col_x = MARGIN + 16 + (i % 2) * (col_w + 24)
        item_y = row_y + (i // 2) * 52
        lines = wrap(draw, "\u2022  " + item, brief_text, col_w)
        draw_lines(draw, lines, brief_text, col_x, item_y, INK, 24)

    # Footer.
    foot = ImageFont.truetype(SERIF, 18)
    draw.text((WIDTH / 2, HEIGHT - 28),
              "World News \u2014 Saturday, 21 November 2026",
              font=foot, fill=GREY, anchor="ma")

    image.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
