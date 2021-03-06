#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
config.py contains the main configuration object for
metrique client applications, which includes built-in
defaults.

Pure defaults assume local, insecure 'test', 'development'
or 'personal' environment. The defaults are not meant for
production use.

To customize local client configuration, add/update
`~/.metrique/http_api.json` (default).

Paths are UNIX compatible only.
'''

import multiprocessing
import os
import re

from metriqueu.jsonconf import JSONConf


class Config(JSONConf):
    ''' Client config (property) class

    DEFAULTS::
        api_verison: Current api version in use
        async: Turn on/off async (parallel) multiprocessing (where supported)
        auto_login: ...
        batch_size: The number of objs to push save_objects at a time
        cubes_path: Path to client modules
        host: Metrique Server host
        username: The username to connect to metrique api with (OPTIONAL)
        password: The password to connect to metrique api with (OPTIONAL)
        port: Metrique server port
        ssl: Connect with SSL (https)
        ssl_verify: ...
    '''
    def __init__(self, config_file=None, *args, **kwargs):
        self.default_config = '~/.metrique/http_api'
        self.defaults = {
            'api_version': 'v2',
            'api_rel_path': 'api/v2',
            'async': True,
            'auto_login': True,
            'batch_size': 1000,
            'cubes_path': '~/.metrique/cubes',
            'debug': None,
            'host': '127.0.0.1',
            'journal': False,
            'logfile': '',
            'logstdout': True,
            'max_workers': multiprocessing.cpu_count(),
            'password': None,
            'port': 5420,
            'retries': 1,
            'sort': -1,
            'ssl': False,
            'ssl_verify': True,
            'username': os.getenv('USER'),
        }
        super(Config, self).__init__(config_file=config_file, *args, **kwargs)

    @property
    def api_url(self):
        ''' Url and schema - http(s)? needed to call metrique api '''
        return os.path.join(self.host_port, self.api_rel_path)

    @property
    def host_port(self):
        ''' Url and schema - http(s)? needed to call metrique api '''
        protocol = 'https://' if self.ssl else 'http://'

        if not re.match('https?://', self.host):
            host = '%s%s' % (protocol, self.host)
        else:
            host = self.host

        host_port = '%s:%s' % (host, self.port)
        return host_port
