#!/usr/bin/python3
"""This module is used to convert markdown to html.
    Usage: markdown2html.py README.md README.html
"""

import sys
import os.path


def main():
    """Entry point of the module.
        Requires 2 command line arguments.
        First argument is the name of the Markdown file
        Second argument is the output file name
    """
    args = sys.argv[1:]

    if len(args) < 2:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(args[0]):
        print(f'Missing {args[0]}',
              file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
