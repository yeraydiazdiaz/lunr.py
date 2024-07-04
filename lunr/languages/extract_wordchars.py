#!/usr/bin/env python

"""
Since lunr-languages has a horrid API that makes it
impossible to access the actual language support objects, it is easier
to simply extract the definitions of wordCharacters from the
JavaScript source code.  This does that.
"""

import argparse
import re
from pathlib import Path
from typing import Dict


def parse_lang(langfile: Path) -> str:
    """
    Find the wordChars pattern in a lunr language model.
    """
    # Not a very good parser, but that is unnecessary
    wcre = re.compile(r".*\.wordCharacters = (.*?);", re.DOTALL)
    plusre = re.compile(r'"\s+\+\s+"')
    comre = re.compile(r"//.*\n", re.MULTILINE)
    with open(langfile, "rt", encoding="utf-8") as infh:
        txt = infh.read()
        m = wcre.search(txt)
        if m is not None:
            # Remove various unnecessary junk
            jsstr = comre.sub("", m.group(1))
            jsstr = plusre.sub("", jsstr)
            jsstr = jsstr.strip('[]";')
            assert re.compile(f"[{jsstr}]")
            return jsstr


def extract_wordchars(langdir: Path) -> Dict:
    langre = re.compile(r".*/lunr\.(..)\.js")
    wordchars = {}
    for path in langdir.iterdir():
        m = langre.match(str(path))
        if m is None:
            continue
        wordchars[m.group(1)] = parse_lang(path)
    return wordchars


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--langdir",
        help="Path to lunr-languages as installed by npm",
        default="node_modules/lunr-languages",
        type=Path,
    )
    args = parser.parse_args()
    if not args.langdir.is_dir():
        parser.error(
            f"""Could not find lunr-languages in {args.langdir}.
You can install it with `npm install lunr-languages` and it should
magically appear in node_modules/lunr-languages."""
        )
    wordchars = extract_wordchars(args.langdir)
    print("WORDCHARS = ", wordchars)


if __name__ == "__main__":
    main()
