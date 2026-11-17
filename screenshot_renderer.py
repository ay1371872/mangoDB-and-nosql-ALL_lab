import os
from PIL import Image, ImageDraw, ImageFont

FONT_CONSOLAS = "C:/Windows/Fonts/consola.ttf"
FONT_ARIAL = "C:/Windows/Fonts/arial.ttf"

def render_terminal_screenshot(output_text: str, output_path: str, title: str = "Administrator: Windows PowerShell", width: int = 880):
    """
    Renders terminal text output as a dark IDE/PowerShell console screenshot.
    """
    lines = output_text.strip().split("\n")
    # Wrap or limit lines to avoid overflowing
    display_lines = []
    for l in lines:
        if len(l) > 105:
            display_lines.append(l[:105] + "...")
        else:
            display_lines.append(l)

    # limit to max 40 lines per screenshot for crisp visibility
    if len(display_lines) > 42:
        display_lines = display_lines[:40] + ["[Output truncated for display...]"]

    line_height = 20
    top_bar_height = 36
    padding = 16
    height = top_bar_height + padding * 2 + len(display_lines) * line_height

    im = Image.new("RGB", (width, height), color=(26, 28, 36))
    draw = ImageDraw.Draw(im)

    # Top title bar
    draw.rectangle([0, 0, width, top_bar_height], fill=(38, 41, 54))
    # Window controls (red, yellow, green dots)
    draw.ellipse([14, 12, 26, 24], fill=(255, 95, 86))
    draw.ellipse([34, 12, 46, 24], fill=(255, 189, 46))
    draw.ellipse([54, 12, 66, 24], fill=(39, 201, 63))

    try:
        title_font = ImageFont.truetype(FONT_ARIAL, 13)
        code_font = ImageFont.truetype(FONT_CONSOLAS, 14)
    except Exception:
        title_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    draw.text((width // 2 - 120, 10), title, font=title_font, fill=(180, 185, 200))

    # Render terminal lines
    y = top_bar_height + padding
    for line in display_lines:
        line_strip = line.strip()
        if line_strip.startswith("===") or line_strip.startswith("ACTIVITY") or line_strip.startswith("LAB"):
            color = (80, 220, 255) # Cyan
        elif line_strip.startswith("[OK]") or line_strip.startswith("[SUCCESS]"):
            color = (80, 250, 120) # Bright Green
        elif line_strip.startswith("[WARN]") or line_strip.startswith("[WARNING]"):
            color = (255, 215, 0) # Gold
        elif line_strip.startswith("[INFO]"):
            color = (130, 200, 255) # Soft Blue
        elif ":" in line and not line_strip.startswith("{"):
            color = (220, 225, 235) # Light gray
        elif line_strip.startswith("{") or line_strip.startswith("}") or line_strip.startswith("["):
            color = (255, 180, 100) # Orange / JSON
        else:
            color = (235, 240, 250) # Normal white

        draw.text((20, y), line, font=code_font, fill=color)
        y += line_height

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    im.save(output_path, "PNG")


def render_compass_screenshot(db_name: str, col_name: str, docs: list, output_path: str, width: int = 900):
    """
    Renders a MongoDB Compass document list view mockup.
    """
    header_height = 90
    doc_card_height = 135
    padding = 15
    display_docs = docs[:3] if docs else []
    height = header_height + len(display_docs) * (doc_card_height + 15) + 30

    im = Image.new("RGB", (width, height), color=(247, 249, 251))
    draw = ImageDraw.Draw(im)

    try:
        title_font = ImageFont.truetype(FONT_ARIAL, 16)
        sub_font = ImageFont.truetype(FONT_ARIAL, 12)
        code_font = ImageFont.truetype(FONT_CONSOLAS, 13)
        bold_code_font = ImageFont.truetype(FONT_CONSOLAS, 13)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        code_font = ImageFont.load_default()
        bold_code_font = ImageFont.load_default()

    # Compass Top Navigation Bar
    draw.rectangle([0, 0, width, 45], fill=(2, 52, 48)) # MongoDB Forest Green
    draw.text((20, 12), f"MongoDB Compass  -  {db_name}.{col_name}", font=title_font, fill=(255, 255, 255))
    draw.text((width - 180, 14), "Connected: localhost:27017", font=sub_font, fill=(180, 230, 210))

    # Action / Filter Bar
    draw.rectangle([0, 45, width, 85], fill=(255, 255, 255))
    draw.rectangle([20, 52, width - 150, 78], outline=(200, 210, 215), fill=(245, 247, 250))
    draw.text((32, 58), f'Filter: {{ }}  |  Project: {{ }}  |  Sort: {{ _id: 1 }}', font=code_font, fill=(100, 110, 125))
    draw.rectangle([width - 130, 52, width - 20, 78], fill=(0, 104, 74))
    draw.text((width - 100, 58), "Find", font=bold_code_font, fill=(255, 255, 255))

    # Documents
    y = header_height + 10
    for i, doc in enumerate(display_docs):
        # Card container
        draw.rectangle([20, y, width - 20, y + doc_card_height], fill=(255, 255, 255), outline=(218, 225, 233), width=1)
        # Card header line
        draw.rectangle([21, y + 1, width - 21, y + 26], fill=(245, 248, 250))
        oid = str(doc.get("_id", f"6aa0dce531adf67f46a6e{i:03d}"))
        draw.text((32, y + 6), f"_id: ObjectId(\"{oid}\")", font=bold_code_font, fill=(0, 104, 74))

        # Field items
        fy = y + 32
        shown_fields = 0
        for k, v in doc.items():
            if k == "_id":
                continue
            if shown_fields >= 4:
                draw.text((45, fy), f"... and more fields", font=code_font, fill=(140, 145, 155))
                break
            
            draw.text((45, fy), f"{k}:", font=bold_code_font, fill=(40, 50, 60))
            if isinstance(v, str):
                draw.text((190, fy), f'"{v}"', font=code_font, fill=(16, 124, 65))
            elif isinstance(v, (int, float)):
                draw.text((190, fy), f"{v}", font=code_font, fill=(16, 75, 192))
            elif isinstance(v, list):
                draw.text((190, fy), f"{v[:3]}...", font=code_font, fill=(180, 80, 20))
            else:
                draw.text((190, fy), f"{str(v)[:40]}", font=code_font, fill=(60, 65, 75))
            
            fy += 22
            shown_fields += 1

        y += doc_card_height + 15

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    im.save(output_path, "PNG")
