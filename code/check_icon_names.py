import os

ICON_DATABASE_FOLDER = "../icon-database"

def check_for_context_problems(themes):

    print "Checking the following themes for icons in multiple contexts:"
    print ", ".join(themes)
    print



    Icons = {}

    for theme in themes:

        with open(os.path.join(ICON_DATABASE_FOLDER, theme + ".txt"), "r") as f:
            icons = f.read().splitlines()

        for icon in icons:

            context, name = icon.split("/")

            if not Icons.has_key(name):
                Icons[name] = {}

            if not Icons[name].has_key(context):
                Icons[name][context] = []

            Icons[name][context].append(theme)

    names = Icons.keys()
    names.sort()

    for name in names:

        data = Icons[name]

        number_of_contexts_for_current_icon = len(data.keys())

        if number_of_contexts_for_current_icon == 1:

            # everything is fine, the icon has the same context in all themes
                # themes = data[data.keys()[0]]

                # number_of_themes = len(themes)

                # if number_of_themes != 1:
                #     print name, themes

                # print name, data
                # print 
                # print
            pass
        else:    
            print name
            for category in data.keys():
                # print category,  data[category]

                for theme in data[category]:
                    print " %-13s:" %category, theme

            print
        #     print

    correct_icons = 0
    incorrect_icons = 0

    for name, data in Icons.iteritems():

        number_of_contexts_for_current_icon = len(data.keys())

        if number_of_contexts_for_current_icon == 1:

            correct_icons += 1
        else:
            incorrect_icons += 1
    
    print "Icons with unique contexts:  ", correct_icons
    print "Icons with multiple contexts:", incorrect_icons    


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

    # ... otherwise use all the available theme folders
    else:

        # get all files inthe base theme folder
        themes = os.listdir(ICON_DATABASE_FOLDER)

        # remove all folder in which 'index.theme' does not exist
        themes = [f for f in themes if os.path.isfile(os.path.join(ICON_DATABASE_FOLDER, f))]

        # take only file with the ending 'txt' strip the ending
        themes = [f[:-4] for f in themes if f.endswith(".txt")]

    check_for_context_problems(themes)

