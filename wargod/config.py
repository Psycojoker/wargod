# -*- coding:Utf-8 -*-

from utils import Storage

class Config(Storage):

    def __init__(self, *args, **kwargs):
        Storage(self, *args, **kwargs)
        # default values
        self.argument = 'this is an example argument'

config = Config()
