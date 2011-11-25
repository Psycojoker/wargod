# -*- coding:Utf-8 -*-

import sys
import os
#from config import config

RSS_FILE = os.path.expanduser("~/.wargodrss")

def run():
    if not os.path.exists(RSS_FILE):
        sys.stderr.write("~/.wargodrss doesn't exist\nEnd\n")
        sys.exit(1)

    print parse_feeds()

def parse_feeds():
    return [rss[:-1] for rss in open(RSS_FILE, "r")]
