#!/usr/bin/python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward <cward@redhat.com>

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from setuptools import setup

__pkg__ = 'metriqued'
__version__ = '0.2.0'
__release__ = 4
__nvr__ = '%s-%s' % (__version__, __release__)
__pkgs__ = ['metriqued']
__provides__ = ['metriqued']
__datafiles__ = []
__desc__ = 'Python/MongoDB Information Platform - Server'
__scripts__ = [
    'bin/metriqued-setup',
    'bin/metriqued'
]
__requires__ = [
    'kerberos (>=1.1.1)',
    'metriqueu (>=%s)' % __version__,
    'passlib (>=1.6.1)',
    'pymongo (>=2.6.1)',
    'tornado (>=3.0)',
]
__irequires__ = [
    'kerberos>=1.1.1',
    'metriqueu>=%s' % __version__,
    'passlib>=1.6.1',
    'pymongo>=2.6.1',
    'tornado>=3.0',
    'argparse',
]
pip_src = 'https://pypi.python.org/packages/source'
__deplinks__ = []

with open('README.rst') as _file:
    readme = _file.read()

github = 'https://github.com/drpoovilleorg/metrique'
download_url = '%s/archive/master.zip' % github

default_setup = dict(
    url='https://github.com/drpoovilleorg/metrique',
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
