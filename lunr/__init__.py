from __future__ import unicode_literals

import logging

from lunr.__main__ import lunr

__all__ = (lunr,)

logging.basicConfig(format="%(levelname)-7s -  %(message)s")

__VERSION__ = '0.2.0'
__TARGET_JS_VERSION__ = '2.1.5'
