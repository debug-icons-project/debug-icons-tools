import os


header = """<html>
<head>
    <title>Icon Theme</title>
</head>   
<body>
<table border=1>
"""

footer = """
</table>
        
</body>
</html>
"""

themes = ["Faba", "hicolor_local", "Moka", "oxygen", "standard_icons"]
themes = ["Faba", "Moka", "standard_icons"]

Icons_with_themes = {}

for theme in themes:

    with open(os.path.join("base_themes", theme + ".txt"), "r") as f:
        icons = f.read().splitlines()

    for icon in icons:
        if not Icons_with_themes.has_key(icon):
            Icons_with_themes[icon] = []

        Icons_with_themes[icon].append(theme)

### make table header
table = "<th>Icon name</th>"

for theme in themes:
    table = table + "<th>" + theme +"</th>"

### make the table itself
icons = Icons_with_themes.keys()
icons.sort()

for icon in icons:

    if "standard_icons" in Icons_with_themes[icon]:
        line = "<tr><td><b>" + icon + "</b></td>"
    else:
        line = "<tr><td>" + icon + "</td>"
    for theme in themes:
        if theme in Icons_with_themes[icon]:
            line = line + "<td>*</td>"
        else:
            line = line + "<td>&nbsp;</td>"
    line = line + "</tr>"
    table = table + line + "\n"

    # use this if you want to see only the standard icons
    # if "standard_icons" in Icons_with_themes[icon]:
    #     line = "<tr><td>" + icon + "</td>"
    #     for theme in themes:
    #         if theme in Icons_with_themes[icon]:
    #             line = line + "<td>*</td>"
    #         else:
    #             line = line + "<td>&nbsp;</td>"
    #     line = line + "</tr>"
    #     table = table + line + "\n"

with open("comparison.html", "w") as f:
    f.write(header + table + footer)
