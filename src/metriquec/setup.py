#!/usr/bin/python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward <cward@redhat.com>

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from setuptools import setup

__pkg__ = 'metriquec'
__version__ = '0.2.0'
__release__ = 4
__nvr__ = '%s-%s' % (__version__, __release__)
__pkgs__ = [
    'metriquec',
    'metriquec.sql',
]
__provides__ = ['metriquec']
__datafiles__ = []
__desc__ = 'Metrique - Cubes'
__scripts__ = []
__requires__ = [
    'metrique (>=%s)' % __version__,
    'celery (>=3.0)',
    'gittle (>=0.2.1)',
    'psycopg2 (>=2.5.1)',
]
__irequires__ = [
    'metrique>=%s' % __version__,
    'celery>=3.0',
    'gittle>=0.2.1',
    'psycopg2>=2.5.1',
]
pip_src = 'https://pypi.python.org/packages/source'
__deplinks__ = []

try:
    with open('README.rst') as _file:
        readme = _file.read()
except IOError:
    readme = __desc__


github = 'https://github.com/drpoovilleorg/metrique'
download_url = '%s/archive/master.zip' % github


default_setup = dict(
    url=github,
    license='GPLv3',
    author='Chris Ward',
    author_email='cward@redhat.com',
    download_url=download_url,
    long_description=readme,
    data_files=__datafiles__,
    dependency_links=__deplinks__,
    description=__desc__,
    install_requires=__irequires__,
    name=__pkg__,
    packages=__pkgs__,
    provides=__provides__,
    requires=__requires__,
    scripts=__scripts__,
    version=__nvr__,
)


setup(**default_setup)
