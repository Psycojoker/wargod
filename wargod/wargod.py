# -*- coding:Utf-8 -*-

import re
import sys
import json
import logging
from os import makedirs
from os.path import expanduser, exists
from feedparser import parse

from html import generate_html
#from config import config

MAX_ENTRIES = 20
WARDOG_DIR = expanduser("~/.config/wargod/")
RSS_FILE = WARDOG_DIR + "rss"
HISTORY_FILE = WARDOG_DIR + "history"

def run():
    if not exists(expanduser(WARDOG_DIR)):
        makedirs(WARDOG_DIR)
    if not exists(RSS_FILE):
        sys.stderr.write("Error: %s doesn't exist\n" % RSS_FILE)
        sys.exit(1)

    logging.debug("parsing feeds")
    a = len(parse_feeds())
    logging.debug("getting history")
    history = get_history()
    for feed in parse_feeds():
        logging.debug("%s feeds left to handle" % a)
        a -= 1

        logging.debug("current feed: %s" % feed)
        parsed_feed = parse(feed)

        if not history["rss"].get(feed):
            # if the feed is new, only display the newest entry
            # so put all other entries in the history of this feed
            logging.debug("feed not in history, adding it and pushing all it's items execpt the newest one in the history")
            history["rss"][feed] = [entry_key(entry) for entry in parsed_feed.entries[1:]]

        for entry in parsed_feed.entries[::-1]:
            logging.debug("handling entry: %s" % entry["title"])
            if entry_key(entry) not in history["rss"][feed]:
                history["current"].append({"title": entry.title,
                                           "link": entry.link,
                                           "description": entry.description,
                                           "updated": entry.get("updated"),
                                           "site": {"title": parsed_feed.feed.title,
                                                    "link": parsed_feed.feed.link,
                                                   }
                                          })
                logging.debug("entry not in history, adding it")
                history["rss"][feed].append(entry_key(entry))

    logging.debug("cutting the size of the 'current' list to MAX_ENTRIES")
    history["current"] = history["current"][-MAX_ENTRIES:]
    open(expanduser("~/output.html"), "w").write(generate_html(history["current"]).encode("Utf-8"))
    logging.debug("output.html written")
    logging.debug("saging history")
    save_history(history)
    logging.debug("end")

def entry_key(entry):
    return entry.get("id", entry.get("updated", entry.link))

def parse_feeds():
    return [rss[:-1] for rss in open(RSS_FILE, "r") if not re.match("^ *#.*$", rss)]

def get_history():
    default = {"rss": {}, "current": []}
    try:
        return json.load(open(HISTORY_FILE, "r")) if exists(HISTORY_FILE) else default
    except ValueError:
        return default

def save_history(history):
    json.dump(history, open(HISTORY_FILE, "w"))
