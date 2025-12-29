from PIL import Image, ImageDraw, ImageFont
import textwrap
import cv2
import numpy as np

def make_thumbnail(img_path, text, out_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    base = Image.fromarray(img).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rect_h = int(h * 0.35)
    rect_top = h - rect_h
    rect_alpha = int(255 * 0.7)
    draw.rectangle(
        [(0, rect_top), (w, h)],
        fill=(0, 0, 0, rect_alpha)
    )
    img_combined = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(img_combined)
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_size = 64
    font = ImageFont.truetype(font_path, font_size)
    lines = textwrap.wrap(text.upper(), width=16)
    lines = lines[:3]
    line_heights = []
    max_line_width = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=4)
        w_line = bbox[2] - bbox[0]
        h_line = bbox[3] - bbox[1]
        line_heights.append(h_line)
        max_line_width = max(max_line_width, w_line)
    total_text_h = sum(line_heights) + (len(lines) - 1) * 10
    y = rect_top + (rect_h - total_text_h) // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=4)
        line_w = bbox[2] - bbox[0]
        x = (w - line_w) // 2
        draw.text(
            (x, y),
            line,
            font=font,
            fill="white",
            stroke_width=4,
            stroke_fill="black"
        )
        y += line_heights[i] + 10
    out = img_combined.convert("RGB")
    cv2.imwrite(out_path, cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR))
