# -*- coding:Utf-8 -*-

from utils import Storage

class Config(Storage):

    def __init__(self, *args, **kwargs):
        Storage(self, *args, **kwargs)
        self.update_feeds = True
        self.regrab_content = False

config = Config()
