#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from decorator import decorator


def _memo(func, *args, **kw):
    # sort and convert list items to tuple for hashability
    if type(kw) is list:
        kw = tuple(sorted(kw))
    # frozenset is used to ensure hashability
    key = args, frozenset(kw.iteritems())
    cache = func.cache  # attributed added by memoize
    if key in cache:
        return cache[key]
    else:
        cache[key] = result = func(*args, **kw)
    return result


def memo(f):
    ''' memoize function output '''
    f.cache = {}
    return decorator(_memo, f)
