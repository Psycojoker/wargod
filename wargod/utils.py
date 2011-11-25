# -*- coding:Utf-8 -*-

# The following class is part of the web.py project. So it is in the Public
# Domain. For more informations, please see the following URLs :
#
#   https://github.com/webpy/webpy/blob/master/LICENSE.txt
#   https://github.com/webpy/webpy/blob/master/web/utils.py
#
class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.

        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
        ...
        AttributeError: 'a'

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k


    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'
