#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob

path = os.path.abspath(os.path.dirname(__file__))


def install(req):
    if not os.path.isfile(req):
        raise RuntimeError('Could not find requirements file at %s' % req)

    if sys.platform == 'darwin':
        prefix = 'env ARCHFLAGS="-arch i386 -arch x86_64" '
    else:
        prefix = ''

    return os.system(prefix + 'pip install -r %s %s' % (req, ' '.join(sys.argv[1:])))


def main():
    for req in glob.glob(os.path.join(path, 'requirements*.txt')):
        ret = install(req)
        if ret != 0:
            return ret

    return 0


if __name__ == '__main__':
    sys.exit(main())
