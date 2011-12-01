# -*- coding:Utf-8 -*-

import logging

HEADER = """\
<html>
<head>
    <title>WarGod - %s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style>
    #title
    {
        margin-left: 8%;
        margin-top: 40px;
        margin-bottom: 40px;
        font-size: 42px;
    }
    #content
    {
        margin-left: 12%;
        margin-right: 12%;
    }
    .item
    {
        margin-bottom: 55px;
        padding: 4px;
    }
    .item-title
    {
        padding: 4px;
        padding-left: 15px;
        padding-right: 15px;
        margin-top: 0px;
        margin-bottom: 0px;
        border-bottom: 3px solid;
    }
    .item-description
    {
        padding: 4px;
        margin-left: 35px;
        margin-right: 35px;
        margin-top: 3px;
        margin-bottom: 0px;
    }
    .separator
    {
        text-align: center;
        margin-bottom: 74px;
        border-top: 1px solid #DDDDDD;
        margin-left: 38%;
        margin-right: 38%;
    }
    .item-title a
    {
        color: #555555;
        text-decoration: none;
    }
    p
    {
        font-size: 20px;
    }
    .inner-description
    {
        padding: 0px;
        margin: 0px;
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
    logging.debug("starting html generation")
    content = HEADER

    for entry in entries[::-1]:
        logging.debug("handling an entry %s" % entry["site"]["link"])
        logging.debug("adding link: %s" % entry["link"])
        content += """\
        <div class="item">
        <p class="item-title"><a href="%s">
        """ % entry["link"]
        logging.debug("adding title: %s" % entry["title"])
        content += '%s</a> - ' % entry["title"]
        logging.debug("adding site link: %s" % entry["site"]["link"])
        content += '<a href="%s">' % entry["site"]["link"]
        logging.debug("adding site title: %s" % entry["site"]["title"])
        content += """%s</a></p>
        <div class="item-description"><p class="inner-description">
        """ % entry["site"]["title"]
        logging.debug("adding description: %s..." % entry["description"][50:])
        content += """%s
        </p>
        </div>
        </div>

        <p class="separator"> </p>

""" % entry["description"]

    logging.debug("adding FOOTER")
    content += FOOTER

    logging.debug("end of html generation")
    return content
