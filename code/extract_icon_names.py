import os
import ConfigParser

def get_list_of_icon_names_from_theme(theme):

    # create some paths
    theme_folder = os.path.join("../base-themes/", theme)

    if not os.path.exists(theme_folder):
        raise ValueError("Error: this folder does not exist!")

    if not os.path.isdir(theme_folder):
        raise ValueError("Error: this is not a folder!")

    theme_index_filename = os.path.join(theme_folder, "index.theme")
       
    # read the ini file
    ini = ConfigParser.ConfigParser()
    a = ini.read(theme_index_filename)

    if not a:
        raise ValueError("Error: There is no 'index.theme' file!")
    
    theme_name = ini.get("Icon Theme", "Name")
    
    all_folders = ini.get("Icon Theme", "Directories")
       
    all_folders = all_folders.split(",")

    # remove whitespace around foldernames
    all_folders = [folder.strip() for folder in all_folders ]

    # sometimes people put ",,,,,". therefore emtpy folder names have to be removed
    all_folders = [folder for folder in all_folders if len(folder) != 0]
    
    # this is where the icon names are stored
    icons = []

    # try to list all icons in each subfolder of the theme
    for current_folder in all_folders:
        
        
        if not ini.has_option(current_folder, "context"):
            raise ValueError("the theme " + theme_path + " in the icon directory " + current_folder + " does not have a 'context' entry")

        if not ini.has_option(current_folder, "size"):
            raise ValueError("the theme " + theme_path + " in the icon directory " + current_folder + " does not have a 'size' entry")

        if not ini.has_option(current_folder, "type"):
            raise ValueError("the theme " + theme_path + " in the icon directory " + current_folder + " does not have a 'type' entry")

        context = ini.get(current_folder, "context").lower()  # we use the lower case version 
        size    = ini.get(current_folder, "size")
        typ     = ini.get(current_folder, "type")
               
        # try to read the subdirectories from the current icon directory
        path = os.path.join(theme_folder, current_folder)

        # if the path does not exist just continue. initially I tought I should print a
        # warning, but it is quite common that icons of a certain size do not exist altough
        # their folder is present so all these errors are just skipped. a check for this would 
        # be better suited in a theme checker script
        if not os.path.isdir(path):
            # print "could not read", path
            continue

        # get all files in the current directory
        icon_names = os.listdir(path)
        
        for icon_name in icon_names:

            # skip hiden files
            if icon_name[0] == ".":
                continue

            file_name = os.path.basename(icon_name)
            
            icon_name, extension = os.path.splitext(file_name)

            # right now only .png and .svg are included in the icon list.
            if not extension in (".png", ".svg"):
                continue
           
            # the name in the icon list consists of the context followed by the icon name. this
            # is done because sometimes the same icon name turns up in more than one context...
            icons.append(context + "/" + icon_name)

    # remove double entries from the different icon sizes and sort the list alphabetically
    icons = list(set(icons))
    icons.sort()

    return icons


if __name__ == "__main__":

    import sys

    nparams = len(sys.argv) - 1

    # Please note: 
    # - all themes must be in the "../base_themes/" subfolder!
    # - the themename is the folder of the theme, notthe one given in the index.theme file
    # - one could implement direct support of locally installed theme files in /usr/share/icons
    #   but creating symlinks in the ".../base_themes/" folder might be easier

    # if there are parameters passed via command line then these are treated as theme names...
    if nparams >= 1: 
        themes = sys.argv[1:]

    # ... otherwise just use these themes:
    else:

        # get all files inthe base theme folder
        themes = os.listdir("../base-themes/")

        # remove all folder in which 'index.theme' does not exist
        themes = [f for f in themes if os.path.isfile(os.path.join("../base-themes/",f, "index.theme"))]

    print "Extracting icon names..."
    print

    # now try to read the theme from each folder...
    # it does not matter if there are wrong entries in 'themes' because they will be fitlered
    # out automatically
    for theme in themes:

        print "-", theme
        
        # get a list of icons names of the format "context/filename_without_ending", e.g. "actions/edit-copy"
        try:
            icons = get_list_of_icon_names_from_theme(theme) 

        # ... if there is an error (corrupt files, ...) then print the error message and continue with next theme
        except ValueError, e:
            print "  -> ", e
            continue

        # create a large string from the list...
        icons_string = "\n".join(icons)

        # ... and write it to a .txt file
        with open(os.path.join("..", "icon-database", theme + ".txt"), "w") as f:
            f.write(icons_string)  
