#!/bin/env python3
# coding: utf-8

import sys
import logging
import multiprocessing

from prettyconf import config

from curytybainbox import web


debug = config('CURYTYBAINBOX_DEBUG', default=False, cast=config.boolean)
log = logging.getLogger('curytybainbox')
if debug:
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.INFO)
    multiprocessing.log_to_stderr(logging.DEBUG)

host = config('CURYTYBAINBOX_WEB_HOST', default='127.0.0.1')
port = int(config('CURYTYBAINBOX_WEB_PORT', default=9876))
secret_key = config('CURYTYBAINBOX_SECRETY_KEY', default='super_secret_key')


def main():

    web.app.config['DEBUG'] = debug
    web.app.config['SECRET_KEY'] = secret_key
    web.app.run(host=host, port=port, processes=5)  # threaded=True
    sys.exit(0)


if __name__ == '__main__':
    main()
