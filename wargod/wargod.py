# -*- coding:Utf-8 -*-

import sys
import os
import json
from feedparser import parse
#from config import config

RSS_FILE = os.path.expanduser("~/.wargodrss")
HISTORY_FILE = os.path.expanduser("~/.wargodrss.history")

def run():
    if not os.path.exists(RSS_FILE):
        sys.stderr.write("~/.wargodrss doesn't exist\nEnd\n")
        sys.exit(1)

    history = get_history()
    for feed in parse_feeds():
        if not history["rss"].get(feed):
            history[feed] = []

        for entry in parse(feed).entries:
            print entry.title

    save_history(history)

def parse_feeds():
    return [rss[:-1] for rss in open(RSS_FILE, "r")]

def get_history():
    default = {"rss" : {}}
    try:
        return json.load(open(HISTORY_FILE, "r")) if os.path.exists(HISTORY_FILE) else default
    except ValueError:
        return default

def save_history(history):
    json.dump(history, open(HISTORY_FILE, "w"))
