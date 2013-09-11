#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward <cward@redhat.com>

import logging
logger = logging.getLogger(__name__)

import os
from tornado.ioloop import IOLoop
from tornado.web import Application

from metriqued.metriqueserver import MetriqueServer

from handlers import PingHandler
from handlers import QueryAggregateHandler, QueryFindHandler
from handlers import QueryDeptreeHandler
from handlers import QueryFetchHandler, QueryCountHandler
from handlers import QueryDistinctHandler, QuerySampleHandler
from handlers import ETLIndexHandler
from handlers import ETLActivityImportHandler
from handlers import ETLSaveObjectsHandler, ETLRemoveObjectsHandler
from handlers import CubeListHandler
from handlers import UserUpdateProfileHandler, UserUpdatePropertiesHandler
from handlers import LoginHandler, LogoutHandler
from handlers import RegisterHandler, UserUpdatePasswordHandler
from handlers import CubeRegisterHandler, CubeDropHandler
from handlers import CubeUpdateRoleHandler

# FIXME: add this to config and generate with metriqued-setup
# DEFAULT should be just a bunch of 0000000's
# generate a new one with
# import base64
# import uuid
# base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
COOKIE_SECRET = 'kmBe2OApQW+d4hjsUPjWcY5cYQyBh0CLnBo9KyikyRI='
API_VERSION = r'/api/v2'
USER_CUBE = r'(\w+)/(\w+)'


def user_cube(value):
    value = str(value)
    path = os.path.join(USER_CUBE, value)
    return path


def api_v2(value):
    value = str(value)
    path = os.path.join(API_VERSION, value)
    return path


def ucv2(value):
    uc = user_cube(value)
    a2 = api_v2(uc)
    return a2


base_handlers = [
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),

    (r"/(\w+)/passwd", UserUpdatePasswordHandler),
    (r"/(\w+)/update_profile", UserUpdateProfileHandler),
    (r"/(\w+)/update_properties", UserUpdatePropertiesHandler),

    (api_v2(r"ping"), PingHandler),

    (api_v2(r"(\w+)?/?(\w+)?"), CubeListHandler),
]

user_cube_handlers = [
    (ucv2(r"find"), QueryFindHandler),
    (ucv2(r"deptree"), QueryDeptreeHandler),
    (ucv2(r"count"), QueryCountHandler),
    (ucv2(r"aggregate"), QueryAggregateHandler),
    (ucv2(r"fetch"), QueryFetchHandler),
    (ucv2(r"distinct"), QueryDistinctHandler),
    (ucv2(r"sample"), QuerySampleHandler),
    (ucv2(r"index"), ETLIndexHandler),
    (ucv2(r"save_objects"), ETLSaveObjectsHandler),
    (ucv2(r"remove_objects"), ETLRemoveObjectsHandler),
    (ucv2(r"activity_import"), ETLActivityImportHandler),
    (ucv2(r"update_cube_role"), CubeUpdateRoleHandler),
    (ucv2(r"drop_cube"), CubeDropHandler),
    (ucv2(r"register"), CubeRegisterHandler),
]

api_v2_handlers = base_handlers + user_cube_handlers


class HTTPServer(MetriqueServer):
    ''' HTTP (Tornado >=3.0) implemntation of MetriqueServer '''
    def __init__(self, host=None, port=None, **kwargs):
        super(HTTPServer, self).__init__(**kwargs)
        if host:
            self.metrique_config.http_host = host
        if port:
            self.metrique_config.http_port = port

    def _setup_webapp(self):
        ''' Config and Views'''
        logger.debug("Tornado: Web App setup")
        debug = self.metrique_config.debug == 2
        gzip = self.metrique_config.gzip

        login_url = self.metrique_config.login_url
        static_path = self.metrique_config.static_path

        init = dict(metrique_config=self.metrique_config,
                    mongodb_config=self.mongodb_config)
        handlers = [(h[0], h[1], init) for h in api_v2_handlers]

        self._web_app = Application(
            gzip=gzip,
            debug=debug,
            static_path=static_path,
            handlers=handlers,
            cookie_secret=COOKIE_SECRET,
            login_url=login_url,
            #xsrf_cookies=True,
        )

        if debug:
            # FIXME hack to disable autoreload when debug is True
            from tornado import autoreload
            autoreload._reload_attempted = True
            autoreload._reload = lambda: None

        port = self.metrique_config.http_port
        address = self.metrique_config.http_host
        if self.metrique_config.ssl:
            ssl_options = dict(
                certfile=self.metrique_config.ssl_certificate,
                keyfile=self.metrique_config.ssl_certificate_key)
            try:
                self._web_app.listen(port=port, address=address,
                                     ssl_options=ssl_options)
            except ValueError:
                raise ValueError(
                    "SSL Cert missing, perhaps? (%s)." % ssl_options)
        else:
            self._web_app.listen(port=port, address=address)

        logger.debug("Tornado: listening on %s:%s" % (port, address))

    def start(self):
        ''' Start a new tornado web app '''
        pid = os.fork()
        if pid == 0:
            logger.debug("Tornado: Start")
            super(HTTPServer, self).start()
            self._setup_webapp()
            ioloop = IOLoop.instance()
            ioloop.start()

    def stop(self):
        ''' Stop a run tornado web app '''
        # FIXME: THIS ISN"T WORKING!
        # should catch sigkill/sigterm and shutdown properly
        super(HTTPServer, self).stop()
        logger.debug("Tornado: Stop")
        ioloop = IOLoop.instance()
        ioloop.stop()
        if hasattr(self, '_web_app'):
            del self._web_app
