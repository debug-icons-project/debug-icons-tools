import PIL

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import os

size = 512

img = Image.new("RGBA", (600, 600), (255, 255, 255))

font_color = (0, 0, 0)

draw = ImageDraw.Draw(img)

draw.fontmode = "1" # this disables antialiasing

fonts = ["04B_03", "04B_03B", "04B_08", "04B_24", "LiberationMono-Regular"]

position = 5

sizes = (8, 9, 10, 11, 12, 13)

for fontname in fonts:
    print fontname
    for size in sizes:
        fontfilenname = os.path.join("..", "fonts", fontname + ".ttf")
        font = ImageFont.truetype(fontfilenname, size)
        draw.setfont(font)

        text = str(size) + ":  "
        draw.text((5, position), text, font_color)

        text = "ABC GQ abc gq MI mi 0O 0123456789 AC0145 " + fontname
        draw.text((35, position), text, font_color)

        position += size + 3
    position += 10


img.save("test_fonts.png")




