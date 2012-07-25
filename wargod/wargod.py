# -*- coding:Utf-8 -*-

import re
import sys
import json
import logging
from os import makedirs
from os.path import expanduser, exists
from feedparser import parse
from urllib2 import urlopen
from readability.readability import Document, Unparseable
from lxml import etree
from lxml.html import ElementSoup
from lxml.html import parse as lxml_parse
from StringIO import StringIO
from yaml import load

from html import generate_html
from config import config


MAX_ENTRIES = 80
WARDOG_DIR = expanduser("~/.config/wargod/")
RSS_FILE = WARDOG_DIR + "rss"
HISTORY_FILE = WARDOG_DIR + "history"


if exists(WARDOG_DIR + "xpath"):
    logging.debug("opening xpath file")
    grabber_list = load(open(WARDOG_DIR + "xpath", "r").read())
else:
    logging.debug("doesn't have a xpath file")
    grabber_list = []

def run():
    if not exists(expanduser(WARDOG_DIR)):
        makedirs(WARDOG_DIR)
    if not exists(RSS_FILE):
        sys.stderr.write("Error: %s doesn't exist\n" % RSS_FILE)
        sys.exit(1)

    logging.debug("parsing feeds")
    logging.debug("getting history")
    history = get_history()
    if config.update_feeds:
        update_feeds(history)

    logging.debug("cutting the size of the 'current' list to MAX_ENTRIES")
    for name in history["output"]:
        history["output"][name] = history["output"][name][-MAX_ENTRIES:]
        if config.regrab_content:
            logging.debug("regrabing content of outputed links")
            for i in history["output"][name]:
                try:
                    logging.debug("trying to get the real url of %s" % i["title"])
                    real_url = urlopen(i["link"]).geturl()
                    i["link"] = real_url
                except Exception as e:
                    logging.debug("Error: %s" % e)
                    continue
                if get_grabber(i["link"]):
                    logging.debug("%s has a grabber" % i["link"])
                    i["description"] = grab_content(i["link"], i["description"])
        open(expanduser("~/%s" % name), "w").write(generate_html(history["output"][name], name).encode("Utf-8"))
        logging.debug("%s written" % name)
    logging.debug("saging history")
    save_history(history)
    logging.debug("end")


def update_feeds(history):
    a = len(parse_feeds())
    for feed, file_names, extend in parse_feeds():
        logging.debug("%s feeds left to handle" % a)
        a -= 1

        logging.debug("current feed: %s" % feed)
        try:
            parsed_feed = parse(feed)
        except Exception, e:
            print >>sys.stderr, "Error: can't read %s: %s" % (feed, e)
            continue

        if not history["rss"].get(feed):
            # if the feed is new, only display the newest entry
            # so put all other entries in the history of this feed
            logging.debug("feed not in history, adding it and pushing all it's items execpt the newest one in the history")
            history["rss"][feed] = [entry_key(entry) for entry in parsed_feed.entries[1:]]

        if not parsed_feed.entries:
            print >>sys.stderr, "Error: %s has not entries" % feed

        for entry in parsed_feed.entries[::-1]:
            logging.debug("handling entry: %s" % entry["title"] if entry.get("title") else "")
            if entry_key(entry) not in history["rss"][feed]:
                for fileu in (file_names if file_names else ["output.html"]):
                    if entry.get("link") is None:
                        continue

                    try:
                        logging.debug("trying to get the real url of %s" % entry["title"])
                        real_url = urlopen(entry["link"]).geturl()
                        entry["link"] = real_url
                    except Exception as e:
                        logging.debug("Error: %s" % e)
                        pass

                    if not history["output"].get(fileu):
                        history["output"][fileu] = []

                    if extend:
                        description = get_link_content(entry.link, entry.get("description", "<p><b>WarGod</b>: this item doesn't have any description"))
                    elif get_grabber(entry.link):
                        description = grab_content(entry.link, entry.get("description", "<p><b>WarGod</b>: this item doesn't have any description"))
                    elif not entry.get("description"):
                        description = "<p><b>WarGod</b>: this item doesn't have any description"
                    else:
                        description = entry.description

                    history["output"][fileu].append({"title": entry.get("title", "No title"),
                                               "link": entry.link,
                                               "description": description,
                                               "updated": entry.get("updated"),
                                               "site": {"title": parsed_feed.feed.get("title", feed),
                                                        "link": parsed_feed.feed.link if parsed_feed.feed.get("link") else feed,
                                                       }
                                              })
                logging.debug("entry not in history, adding it")
                history["rss"][feed].append(entry_key(entry))


def get_grabber(url):
    for i, path in grabber_list:
        if i.startswith("r:") and re.findall(i[2:], url):
            return path
        elif i in url:
            return path
    return None


def grab_content(url, original_description):
    logging.debug("grabbing the content of %s" % url)
    try:
        site = urlopen(url)
    except Exception as e:
        logging.debug("Error: can't access %s for grabbing: %s" % (url, e))
        return original_description + "\n<p><b>WarGod error</b>: I could not access this url</p>"
    site_url = "/".join(site.geturl().split("/")[:3]) + "/"
    path = get_grabber(url)
    logging.debug("xpath query is %s" % path)
    try:
        xml = lxml_parse(site)
        content = xml.xpath(path)[0]
    except Unparseable:
        logging.debug("Error: can't parse %s using %s" % (url, path))
        return original_description + "\n<p><b>WarGod error</b>: I could not parse this url</p>"
    except IndexError:
        logging.debug("Error: can't get content of %s using %s" % (url, path))
        return original_description + "\n<p><b>WarGod error</b>: I could not parse this url</p>"
    except Exception as e:
        sys.stderr.write("Unpredicted Error: can't get content of %s using %s" % (url, path))
        return original_description + "\n<p><b>WarGod error</b>: I could not parse this url</p>"
    content.make_links_absolute(site_url)
    return etree.tostring(content, encoding="Utf-8").decode("Utf-8")


def get_link_content(url, original_description):
    try:
        site = urlopen(url)
    except Exception:
        return original_description + "\n<p><b>WarGod error</b>: I could not access this url</p>"
    site_url = "/".join(site.geturl().split("/")[:3]) + "/"
    content = site.read()
    try:
        xml = ElementSoup.parse(StringIO(Document(content).summary()))
    except Unparseable:
        return original_description + "\n<p><b>WarGod error</b>: I could not parse this url</p>"
    xml.make_links_absolute(site_url)
    return etree.tostring(xml.find("body"), encoding="Utf-8")[6:-7].decode("Utf-8")


def entry_key(entry):
    if "deviantart.com" in entry.link:
        return entry.link
    return entry.get("id", entry.get("updated", entry.link))


def parse_feeds():
    def manage_arguments(args):
        if "extend" in args:
            args.remove("extend")
            return args, True
        return args, False
    return [(rss[:-1].split(" ")[0],) + manage_arguments(rss[:-1].split(" ")[1:]) for rss in open(RSS_FILE, "r") if not re.match("^ *#.*$", rss)]


def get_history():
    default = {"rss": {}, "output": {"output.html": []}}
    try:
        return json.load(open(HISTORY_FILE, "r")) if exists(HISTORY_FILE) else default
    except ValueError:
        return default


def save_history(history):
    json.dump(history, open(HISTORY_FILE, "w"), indent=4)
