#!/bin/env python3
# coding: utf-8

import sys
import logging
import multiprocessing

from prettyconf import config

from curytybainbox import box


debug = config('CURYTYBAINBOX_DEBUG', default=False, cast=config.boolean)
log = logging.getLogger('curytybainbox')
if debug:
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.INFO)
    multiprocessing.log_to_stderr(logging.DEBUG)


def main():

    unix_path = config('CURYTYBAINBOX_UNIX_PATH', default='/var/run/curytybainbox')
    b = box.BoxProcess(unix_path)
    b.start()
    try:
        b.join()
    except KeyboardInterrupt:
        pass
    finally:
        b.stop()
        b.terminate()

    sys.exit(0)


if __name__ == '__main__':
    main()
