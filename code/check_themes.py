import os


themes = ["Faba", "hicolor_local", "Moka", "oxygen", "standard_icons"]
# themes = ["Faba", "Moka", "standard_icons"]

Icons = {}

for theme in themes:

    with open(os.path.join("base_themes", theme + ".txt"), "r") as f:
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
print
print "correct items", correct_icons
print "incorrect items", incorrect_icons    