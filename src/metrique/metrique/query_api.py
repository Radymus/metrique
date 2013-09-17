#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
This module contains all the query and aggregation
related api functionality.
'''

import logging
logger = logging.getLogger(__name__)
import os

from metrique.result import Result
from metriqueu.utils import set_default

DEFAULT_SAMPLE_SIZE = 1


def aggregate(self, pipeline, cube=None, owner=None):
    '''
    Proxy for pymongodb's .aggregate framework call
    on a given cube

    :param list pipeline: The aggregation pipeline. $match, $project, etc.
    :param string cube: name of cube to work with
    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name, err_msg="cube required")
    cmd = os.path.join(owner, cube, 'aggregate')
    result = self._get(cmd, pipeline=pipeline)
    try:
        return result['result']
    except Exception:
        raise RuntimeError(result)


def count(self, query=None, cube=None, date=None, owner=None):
    '''
    Run a `pql` based query on the given cube, but
    only return back the count (Integer)

    :param string query: The query in pql
    :param string date: Date (date range) that should be queried
    :param bool most_recent:
        If true and there are multiple historical version of a single
        object matching the query then only the most recent one will
        be returned
    :param string cube: name of cube to work with
    '''
    if not query:
        query = '_oid == exists(True)'
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name)
    cmd = os.path.join(owner, cube, 'count')
    return self._get(cmd, query=query, date=date)


def find(self, query, fields=None, date=None, sort=None, one=False,
         raw=False, explain=False, cube=None, merge_versions=True,
         owner=None, **kwargs):
    '''
    Run a `pql` based query on the given cube. Optionally:

    :param string query: The query in pql
    :param list/string fields: Fields that should be returned
    :type fields: str, or list of str, or str of comma-separated values
    :param string date: Date (date range) that should be queried
    :param bool explain: return execution plan instead of results
    :param string cube: name of cube to work with
    :param boolean merge_versions:
        merge versions with unchanging fields od interest
    :param string owner: owner of cube

    .. note::
        - if date==None then the most recent versions of the objects
          will be queried.

    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name)
    cmd = os.path.join(owner, cube, 'find')
    result = self._get(cmd, query=query, fields=fields,
                       date=date, sort=sort, one=one,
                       explain=explain,
                       merge_versions=merge_versions)
    return result if raw or explain else Result(result, date)


def deptree(self, field, oids, date=None, level=None,
            owner=None, cube=None):
    '''
    Dependency tree builder recursively fetchs objects that
    are children of the initial set of objects provided.

    :param string field: Field that contains the 'parent of' data
    :param list oids: Object oids to build depedency tree for
    :param string date: Date in time when the deptree should be generated for
    :param integer level: limit depth of recursion
    :param string cube: name of cube to work with
    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name)
    cmd = os.path.join(owner, cube, 'deptree')
    result = self._get(cmd, field=field,
                       oids=oids, date=date,
                       level=level)
    return sorted(result)


def fetch(self, fields=None, date=None, sort=None, skip=0, limit=0,
          oids=None, raw=False, cube=None, owner=None):
    '''
    Fetch field values for (potentially) all objects
    of a given, with skip, limit, id "filter" arguments

    :param fields: Fields that should be returned
    :type fields: str, or list of str, or str of comma-separated values
    :param string date: Date (date range) that should be queried
    :param tuple sort: pymongo formated sort tuple
    :param Integer skip:
        number of items (sorted ASC) to skip
    :param Integer limit:
        number of items total to return, given skip
    :param List oids:
        specific list of oids we should fetch
    :param boolean raw: return the documents in their (dict) form
    :param string cube: name of cube to work with
    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name, err_msg="cube required")
    cmd = os.path.join(owner, cube, 'fetch')
    result = self._get(cmd, fields=fields,
                       date=date, sort=sort,
                       skip=skip, limit=limit,
                       oids=oids)
    return result if raw else Result(result, date)


def distinct(self, field, cube=None, owner=None):
    '''
    Return back all distinct token values of a given field

    :param string field:
        Field to get distinct token values from
    :param string cube: name of cube to work with
    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name, err_msg="cube required")
    cmd = os.path.join(owner, cube, 'distinct')
    result = self._get(cmd, field=field)
    return sorted(result)


def sample(self, sample_size=DEFAULT_SAMPLE_SIZE, fields=None,
           date=None, raw=False, query=None, cube=None, owner=None):
    '''
    Draws a sample of objects at random.

    :param integer sample_size: Size of the sample.
    :param fields: Fields that should be returned
    :param string date: Date (date range) that should be queried
    :param boolean raw: if True, then return result as a dictionary
    :param string cube: name of cube to work with

    .. note::
        - if date==None then the most recent versions of the objects
          will be queried.
    '''
    owner = set_default(owner, self.config.api_username)
    cube = set_default(cube, self.name, err_msg="cube required")
    cmd = os.path.join(owner, cube, 'sample')
    result = self._get(cmd, sample_size=sample_size, fields=fields,
                       query=query, date=date)
    return result if raw else Result(result, date)
