HEADER = """\
<html>
<head>
    <title>WarGod - %s</title>
    <style>
    #title
    {
        margin-left: 8%;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    #content
    {
        margin-left: 12%;
        margin-right: 12%;
    }
    .item
    {
        margin-bottom: 25px;
        padding: 4px;
    }
    .item-title
    {
        padding: 4px;
        padding-left: 6px;
        margin-top: 0px;
        margin-bottom: 0px;
        /* border: 1px solid; */
        background-color: #9D4DC9;
    }
    .item-description
    {
        background-color: #DDDDDD;
        padding: 4px;
        padding-left: 6px;
        margin-top: 0px;
        margin-bottom: 0px;
        /*
        border-left:   1px solid;
        border-right:  1px solid;
        border-bottom: 1px solid;
        */
    }
    .item-title a
    {
        color: #EEEEEE;
        text-decoration: none;
    }
    p
    {
        font-size: 20px;
    }
    </style>
</head>
<body>
    <h1 id="title">WarGod</h1>
    <div id="content">
"""

FOOTER = """\
    </div>
</body>
</html>"""


def generate_html(entries):
    content = HEADER

    for entry in entries:
        content += """\
        <div class="item">
        <p class="item-title"><a href="%s">%s</a> - <a href="%s">%s</a></p>
        <p class="item-description">
        %s
        </p>
        </div>

""" % (entry["link"], entry["title"], entry["site"]["link"], entry["site"]["title"], entry["description"])

    content += FOOTER

    return content
