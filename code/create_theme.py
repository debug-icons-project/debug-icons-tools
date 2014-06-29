import os

import PIL

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# this is where the name lists and the icon id file is stored
ICON_DATABASE_FOLDER = "../icon-database"

# this is the subfolder inwhich the debug theme is saved
FINAL_THEME_FOLDER = "../final-themes"

# only these contexts are supported right now
supported_contexts = ["actions", 
                      "applications", 
                      "categories",
                      "devices",
                      "emblems",
                      "emotes",
                      "mimetypes",
                      "places",
                      "status"]


# this is used to print the context on the icon in a nice way
context_nice_names = {}
context_nice_names["actions"]      = "Actions"
context_nice_names["applications"] = "Applications"
context_nice_names["categories"]   = "Categories"
context_nice_names["devices"]      = "Devices"
context_nice_names["emblems"]      = "Emblems"
context_nice_names["emotes"]       = "Emotes"
context_nice_names["mimetypes"]    = "MimeTypes"
context_nice_names["places"]       = "Places"
context_nice_names["status"]       = "Status"

# this is the name of the subfolder for each supported category
context_folders = {}
context_folders["actions"]      = "actions"
context_folders["applications"] = "apps"
context_folders["categories"]   = "categories"
context_folders["devices"]      = "devices"
context_folders["emblems"]      = "emblems"
context_folders["emotes"]       = "emotes"
context_folders["mimetypes"]    = "mimetypes"
context_folders["places"]       = "places"
context_folders["status"]       = "status"

# for some icon contexts we define some nice abbreviation
context_abbrs = {}
context_abbrs["actions"]      = "AC"
context_abbrs["applications"] = "AP"
context_abbrs["categories"]   = "CA"
context_abbrs["devices"]      = "DE"
context_abbrs["emblems"]      = "EM"
context_abbrs["emotes"]       = "EO"
context_abbrs["mimetypes"]    = "MI"
context_abbrs["places"]       = "PL"
context_abbrs["status"]       = "ST"

# creates a string similar to "16x16/apps"
# this is used several times in the theme file
def generate_subfolder_name(size, name):
    return os.path.join("%dx%d" % (size, size), name) # this is done in this specific way because otherwise KDE will not find some theme icons

# this writes the theme file for all supported contexts and the user defined sizes
def write_theme_ini(output, sizes):
    """this creates an inifile with all paths"""
    
    # this is the header of the theme file
    ini_header = """[Icon Theme]
                 Name=%s
                 Comment=A theme which can be used for debugging or creating new icon themes
                 """ % output

    #####################
    # write the Directories string to the theme file which contains a comma separated list of all icon subdirectories

    contexts = supported_contexts[:]
    contexts.sort()
   
    folders_temp = []

    for c in contexts:

        for size in sizes:
        
            subfolder = generate_subfolder_name(size, context_folders[c])
            
            folders_temp.append(subfolder)

    folders_as_string = ",".join(folders_temp)

    ini_dir_string = """
                     Directories=%s
                     """ % folders_as_string

    
    ini_dir_sections = ""
    #####################
    # for each icon subdirectory create an entry to the ini file
    for c in contexts:

        for size in sizes:
            
            subfolder = generate_subfolder_name(size, context_folders[c])
            
            ini_dir_sections += """
                                [%s]
                                Size=%d
                                Context=%s
                                Type=Fixed
                                """ % (subfolder, size, context_nice_names[c])

    # these 4 lines remove all trailing whitespace which resulted from the indention above... 
    # this is just done that the source file looks nicer...
    file_content = ini_header + ini_dir_string + ini_dir_sections
    file_content = file_content.splitlines()
    file_content = [l.strip() for l in file_content]
    file_content = "\n".join(file_content)

    #####################
    # write the ini text to the theme file

    complete_path = os.path.join(FINAL_THEME_FOLDER, output)
    if not os.path.exists(complete_path):
        os.makedirs(complete_path)

    with open(os.path.join(complete_path, "index.theme"), "w") as f:

        f.write(file_content)


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
        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))

        draw.text((1, 1), iid[0:3], font_color)
        draw.text((1, 8), iid[3:], font_color)

    elif (size >= 22) and (size < 24):
        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))

        draw.text((4,  0), iid[0:3], font_color)
        draw.text((4,  7), iid[3:], font_color)      
        
        draw.text((1, 22-7), str(size), font_color)      
        draw.text((12, 22-7), context_abbr, font_color)      

    elif (size >= 24) and (size < 32): # oben links
        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))

        draw.text((5,  1), iid[0:3], font_color)
        draw.text((5,  8), iid[3:], font_color)      
        
        draw.text((1, size-7), str(size), font_color)      
        draw.text((14, size-7), context_abbr, font_color)      

    elif (size >= 32) and (size < 64):
        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))

        draw.text((1, 0), iid, font_color)
        draw.text((1, 8), context, font_color)
        draw.text((1, 16), filename, font_color)


        draw.text((1, size-7), str(size), font_color)        

        draw.line([size-1, 0, size-1, size-1], bg_color)

    elif size >= 64:

        # this is a larger font which makes it more readable
        
        # draw.setfont(ImageFont.truetype("fonts/LiberationMono-Regular.ttf", 11))

        # draw.text((1, 0),  iid, font_color)
        # draw.text((1, 11), context, font_color)
        # draw.text((1, 22), filename, font_color)

        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))

        draw.text((1, 0), iid, font_color)
        draw.text((1, 8), context, font_color)
        draw.text((1, 16), filename, font_color)


        draw.setfont(ImageFont.truetype("fonts/04B_03.ttf", 8))
        
        draw.text((1, size-7), str(size), font_color)              

        draw.line([size-1, 0, size-1, size-1], bg_color)

    return img


# this loads the abbreviation file and returns a dict with all valid entries
def load_abbrs():
    
    abbrs = {}

    temp_unique = []

    with open(os.path.join(ICON_DATABASE_FOLDER, "icon.ids"), "r") as f:

        temp = f.read().splitlines()

        for line in temp:

            # remove comments           
            line = line.split("#")[0] 

            # split at the "=". if not "=" is present then just read the next line
            t = line.split("=")

            if len(t) != 2:
                continue

            # this part is a bit stupid: alle the line contain an entry like context/iconname
            # while the context should be lower case, the case of the icon name should be preserved

            Context_slash_name    = t[0].strip()
            icon_id               = t[1].strip()

            t = Context_slash_name.split("/")

            if len(t) != 2:
                continue

            Context, name = t

            context_slash_name = Context.lower() + "/" + name # convert context to lowercase but leave icon name

            if icon_id in temp_unique:
                print "warning, the icon id", icon_id, "appears at least to times in icon_ids.txt"
            
            temp_unique.append(icon_id)

            abbrs[context_slash_name] = icon_id

    return abbrs

def create_theme(base_themes, output, sizes):
    
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


    ##############
    # here we load the abbreveation file
    icon_abbrs = load_abbrs()

    write_theme_ini(output, sizes)

    ###
    # load icons
    temp_icons = []
    
    icons = {}

    # load all icon names from all files and populate a dict which contains a list of 
    # all icon names for all supported contexts
    for theme in base_themes:
    
        with open(os.path.join(ICON_DATABASE_FOLDER, theme + ".txt"), "r") as f:
            lines = f.read().splitlines()    
        
        for line in lines:
            t = line.split("/")

            if len(t) != 2:
                continue

            context = t[0].strip().lower()

            if not context in supported_contexts:
                continue

            n = t[1].strip()

            if len(n) == 0:
                continue

            if not icons.has_key(context):
                icons[context] = []

            if not n in icons[context]: # prevent double entries
                icons[context].append(n) 
    
    icon_list = []

    for c in icons.iterkeys():
        icons[c].sort()

    # now run through all the icons and create 
    for current_context in icons.iterkeys():

        print current_context

        # enumerate is used here because thenthe idx can be used as an icon ID
        for idx, name in enumerate(icons[current_context]): 

            temp = current_context.lower() + "/" + name.lower()

            # remember: the icon id will be limited to 6 chars inside the icon creation routine
            if icon_abbrs.has_key(temp):
                icon_id = icon_abbrs[temp]
            else:
                icon_id = context_abbrs[current_context] + "%04d" % idx

            for size in sizes:
                
                icon = create_icon(size, icon_id, context=current_context, filename=name, bg_color=bg_colors[current_context], font_color=font_colors[current_context])
                
                # save icon
                sub_dir = generate_subfolder_name(size, context_folders[current_context])
                
                full_path = os.path.join(FINAL_THEME_FOLDER, output, sub_dir)
                
                if not os.path.exists(full_path):
                    os.makedirs(full_path)

                icon.save(os.path.join(full_path, name + ".png"))

            # this is used for the look up file for icon ids and filenames
            icon_list.append("%-6s = %s/%s" % (icon_id, current_context, name))
    
    # create the list of all icon ids and the coresponding file names
    icon_list.sort()
    icon_list = "\n".join(icon_list)

    with open(os.path.join(FINAL_THEME_FOLDER, output, "lookup_icons.txt"), "w") as f:
        f.write(icon_list)
    

##############
##############
# here starts the real program

sizes = [16, 22, 24, 32, 48, 64, 96, 128]

print
print "creating standard icons"
create_theme(base_themes=["standard-icons-0.8.90"], output="debug-icons-standard-0.8.90", sizes=sizes)

print
print "creating oxygen icon"
create_theme(base_themes=["Oxygen-4"], output="debug-icons-oxygen-4", sizes=sizes)
