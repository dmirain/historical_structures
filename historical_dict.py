# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class HistoricalDict(dict):

    def __init__(self, iterable, parent=None):
        dict.__init__(self, iterable)
        self._added = {}
        self._removed = {}
        self._changed = {}

    def __setitem__(self, key, value):
        if key in self:
            if key in self._added:
                self._added[key] = value
            elif key in self._removed:
                if value != self._removed[key]:
                    self._changed[key] = self._removed[key]
                del self._removed[key]
            else:
                if key in self._changed:
                    if value == self._changed[key]:
                        del self._changed[key]
                else:
                    self._changed[key] = self[key]
        else:
            self._added[key] = value

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if key in self._added:
            del self._added[key]
        elif key in self._changed:
            self._removed[key] = self._changed[key]
        elif key in self:
            self._removed[key] = self[key]

        dict.__delitem__(self, key)

    def update(self, iterable):
        if isinstance(iterable, dict):
            iterable = iterable.iteritems()
        for num, kv in enumerate(iterable):
            try:
                k,v = kv
            except TypeError:
                msg = ('cannot convert dictionary update'
                        ' sequence element #{num} to a sequence')
                raise TypeError(msg.format(num=num))

            self[k] = v

    def commit(self):
        self._added = {}
        self._removed = {}
        self._changed = {}

    def reset(self):
        if self._added:
            for key in self._added:
                dict.__delitem__(self, key)
        if self._removed:
            dict.update(self, self._removed)
        if self._changed:
            dict.update(self, self._changed)

        self.commit()

    def history(self):
        return {
            'added': self._added.copy(),
            'changed': self._changed.copy(),
            'removed': self._removed.copy(),
        }

    added = property(lambda self: self._added.copy())
    removed = property(lambda self: self._removed.copy())
    changed = property(lambda self: self._changed.copy())
