#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" Utils to support python 2.6 compatibility """

try:
    import simplejson as json
except ImportError:
    import json

from collections import MutableMapping


def _import_module(module_uri):
    return __import__(module_uri, {}, {}, [''])


def import_module(module_uri):
    """ Import module by string 'from.path.module'

    To support python 2.6
    """
    try:
        from importlib import import_module
        callback = import_module
    except ImportError:
        callback = _import_module

    return callback(module_uri)


class _OrderedDict(dict, MutableMapping):
    """
    Src: http://code.activestate.com/recipes/576669/
    Author: Raymond Hettinger (Promoter of PEP which introduces OrderDict into
    colletions module in python >2.7)
    """

    # Methods with direct access to underlying attributes

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at 1 argument, got %d', len(args))
        if not hasattr(self, '_keys'):
            self._keys = []
        self.update(*args, **kwds)

    def clear(self):
        del self._keys[:]
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            self._keys.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __iter__(self):
        return iter(self._keys)

    def __reversed__(self):
        return reversed(self._keys)

    def popitem(self):
        if not self:
            raise KeyError
        key = self._keys.pop()
        value = dict.pop(self, key)
        return key, value

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        inst_dict.pop('_keys', None)
        return (self.__class__, (items,), inst_dict)

    # Methods with indirect access via the above methods

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items

    def __repr__(self):
        pairs = ', '.join(map('%r: %r'.__mod__, self.items()))
        return '%s({%s})' % (self.__class__.__name__, pairs)

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = _OrderedDict
