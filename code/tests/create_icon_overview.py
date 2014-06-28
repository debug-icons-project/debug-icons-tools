import os

import PIL

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def create_icon(size, iid, context=None, filename=None, bg_color=(255, 255, 255), font_color=(0, 0, 0)):

    if size < 16:
        raise ValueError("'size' must be >= 16!")

    # for some icon contexts we define some nice abbreviation
    context_abbrs = {}
    context_abbrs["actions"]      = "AC"
    context_abbrs["applications"] = "AP"
    context_abbrs["categories"]   = "CA"
    context_abbrs["devices"]      = "DV"
    context_abbrs["emblems"]      = "EB"
    context_abbrs["emotes"]       = "EO"
    context_abbrs["mimetypes"]    = "MI"
    context_abbrs["places"]       = "PL"
    context_abbrs["status"]       = "ST"

    # this is used to print the context on the icon in a nice way
    context_nice_formats = {}
    context_nice_formats["actions"]      = "Actions"
    context_nice_formats["applications"] = "Applications"
    context_nice_formats["categories"]   = "Categories"
    context_nice_formats["devices"]      = "Devices"
    context_nice_formats["emblems"]      = "Emblems"
    context_nice_formats["emotes"]       = "Emotes"
    context_nice_formats["mimetypes"]    = "MimeTypes"
    context_nice_formats["places"]       = "Places"
    context_nice_formats["status"]       = "Status"
    
    # check if a context is given
    if context is None:
        context      = "Undefined"
        context_abbr = "??"
    # check if the context is "supported" but the above dict...
    else:
        # if it is a supported, then read the abbreviation and make the 
        # context name in nice upper/lower case regardless how the input string looks like
        if context_abbrs.has_key(context.lower()):
            context_abbr = context_abbrs[context.lower()]
            context = context_nice_formats[context.lower()]
        # if no supported contest is found then take the first two letters and amke them 
        # uppercase
        else:
            context_abbr = context[0:2].upper()

    # turn the icon id into a 6 letter string. this makes it easier later on
    iid = "%-6.6s" % iid

    # create new image and a draw object
    img  = Image.new("RGBA", (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # this disables antialiasing
    draw.fontmode = "1"
        
    if (size >= 16) and (size < 22):
        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))

        draw.text((1, 1), iid[0:3], font_color)
        draw.text((1, 8), iid[3:], font_color)

    elif (size >= 22) and (size < 24):
        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))

        draw.text((4,  0), iid[0:3], font_color)
        draw.text((4,  7), iid[3:], font_color)      
        
        draw.text((1, 22-7), str(size), font_color)      
        draw.text((12, 22-7), context_abbr, font_color)      

    elif (size >= 24) and (size < 32): # oben links
        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))

        draw.text((5,  1), iid[0:3], font_color)
        draw.text((5,  8), iid[3:], font_color)      
        
        draw.text((1, size-7), str(size), font_color)      
        draw.text((14, size-7), context_abbr, font_color)      

    elif (size >= 32) and (size < 64):
        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))

        draw.text((1, 0), iid, font_color)
        draw.text((1, 8), context, font_color)
        draw.text((1, 16), filename, font_color)


        draw.text((1, size-7), str(size), font_color)        

        draw.line([size-1, 0, size-1, size-1], bg_color)

    elif size >= 64:

        # this is a larger font which makes it more readable
        # draw.setfont(ImageFont.truetype("../fonts/LiberationMono-Regular.ttf", 11))
        # draw.text((1, 0),  iid, font_color)
        # draw.text((1, 11), context, font_color)
        # draw.text((1, 22), filename, font_color)

        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))

        draw.text((1, 0), iid, font_color)
        draw.text((1, 8), context, font_color)
        draw.text((1, 16), filename, font_color)


        draw.setfont(ImageFont.truetype("../fonts/04B_03.ttf", 8))
        
        draw.text((1, size-7), str(size), font_color)              

        draw.line([size-1, 0, size-1, size-1], bg_color)

    return img

##############
##############
# sets some default values


bg_colors = {}
bg_colors["actions"]      = (255,   0,   0) # red
bg_colors["applications"] = (255,   0, 255) # pink
bg_colors["categories"]   = (  0,   0, 255) # blau
bg_colors["devices"]      = (  0, 255, 255) # hellblau
bg_colors["emblems"]      = (255, 255, 255) # white
bg_colors["emotes"]       = (133, 133, 133) # grau
bg_colors["mimetypes"]    = (  0, 255,   0) # green
bg_colors["places"]       = (255, 255,   0) # yellow
bg_colors["status"]       = (255, 128,   0) # orange

font_colors = {}
font_colors["actions"]      = (255, 255, 255) # red
font_colors["applications"] = (255, 255, 255) # pink
font_colors["categories"]   = (255, 255, 255) # blau
font_colors["devices"]      = (  0,   0,   0) # hellblau
font_colors["emblems"]      = (  0,   0,   0) # white
font_colors["emotes"]       = (  0,   0,   0) # grau
font_colors["mimetypes"]    = (  0,   0,   0) # green
font_colors["places"]       = (  0,   0,   0) # yellow
font_colors["status"]       = (  0,   0,   0) # orange




sizes = [16, 22, 24, 32, 48, 64, 96, 128]
# sizes = [96]
sizes.sort()

gap = 5

s = 0
for size in sizes:
    s+= size
s = s + len(sizes)*gap + gap


img = Image.new("RGBA", (s, sizes[-1] + 2*gap ), (128, 128, 128))

draw = ImageDraw.Draw(img)

t = gap
for size in sizes:

    iid = "starth"
    iid = "zooin"
    filename = "start-here-kde"
    context = "Places"

    # context = "Applications"
    context = "mimeTypes"

    context = "MimeTypes"
    filename = "inode-directory"
    iid = "inodir"
            
            
    icon = create_icon(size, iid=iid, context=context, filename=filename, bg_color=bg_colors[context.lower()], font_color=font_colors[context.lower()])

    img.paste(icon, (t, gap))

    t = t + size + gap
    

    # icon.save(os.path.join(full_path, name + ".png"))

img.save("icon_overview.png")




