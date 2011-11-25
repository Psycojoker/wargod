# -*- coding:Utf-8 -*-

import sys
import os
import json
#from config import config

RSS_FILE = os.path.expanduser("~/.wargodrss")
HISTORY_FILE = os.path.expanduser("~/.wargodrss.history")

def run():
    if not os.path.exists(RSS_FILE):
        sys.stderr.write("~/.wargodrss doesn't exist\nEnd\n")
        sys.exit(1)

    print get_history()
    print parse_feeds()

def parse_feeds():
    return [rss[:-1] for rss in open(RSS_FILE, "r")]

def get_history():
    try:
        return json.load(open(HISTORY_FILE, "r")) if os.path.exists(HISTORY_FILE) else {}
    except ValueError:
        return {}
