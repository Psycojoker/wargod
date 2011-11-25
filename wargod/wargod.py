# -*- coding:Utf-8 -*-

import sys
import os
import json
from feedparser import parse
#from config import config

MAX_ENTRIES = 10
RSS_FILE = os.path.expanduser("~/.wargodrss")
HISTORY_FILE = os.path.expanduser("~/.wargodrss.history")

def run():
    if not os.path.exists(RSS_FILE):
        sys.stderr.write("~/.wargodrss doesn't exist\nEnd\n")
        sys.exit(1)

    history = get_history()
    for feed in parse_feeds():
        if not history["rss"].get(feed):
            history["rss"][feed] = []

        for entry in parse(feed).entries[::-1]:
            if entry_key(entry) not in history["rss"][feed]:
                history["current"].append({"title": entry.title, "link":
                                           entry.link, "description":
                                           entry.description, "updated":
                                           entry.updated})
                history["rss"][feed].append(entry_key(entry))

    history["current"] = history["current"][-MAX_ENTRIES:]
    for i in history["current"]:
        print i["title"]
    save_history(history)

def entry_key(entry):
    return entry.get("id", entry.get("updated", entry.link))

def parse_feeds():
    return [rss[:-1] for rss in open(RSS_FILE, "r")]

def get_history():
    default = {"rss": {}, "current": []}
    try:
        return json.load(open(HISTORY_FILE, "r")) if os.path.exists(HISTORY_FILE) else default
    except ValueError:
        return default

def save_history(history):
    json.dump(history, open(HISTORY_FILE, "w"))
