import logging

from lunr.__main__ import lunr, get_default_builder

__all__ = ("lunr", "get_default_builder")

logging.basicConfig(format="%(levelname)-7s -  %(message)s")

__VERSION__ = "0.6.0"
__TARGET_JS_VERSION__ = "2.3.9"
