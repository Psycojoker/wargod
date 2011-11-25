HEADER = """\
<html>
<head>
    <title>WarGod</title>
</head>
<body>
    <h1>WarGod</h1>
    <div style="">
"""

FOOTER = """\
    </div>
</body>
</html>"""


def generate_html(entries):
    content = HEADER

    for entry in entries:
        content += """\
        <h2><a href="%s">%s</a></h2>
        <p>
        %s
        </p>
""" % (entry["link"], entry["title"], entry["description"])

    content += FOOTER

    return content
