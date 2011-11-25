# -*- coding:Utf-8 -*-

import sys
import os
#from config import config

def run():
    if not os.path.exists(os.path.expanduser("~/.wardogrss")):
        sys.stderr.write("~/.wardogrss doesn't exist\nEnd\n")
        sys.exit(1)
