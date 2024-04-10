#!/usr/bin/python3
"""This module is used to convert markdown to html.
    Usage: markdown2html.py README.md README.html
"""

import sys
import os.path
import re


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

    markdown_file = open(args[0], 'r')
    output_str = ''

    try:
        for line in markdown_file.readlines():
            output_str += convert_line(line)
    finally:
        markdown_file.close()

    with open(args[1], 'w') as out_file:
        out_file.write(output_str)


def convert_line(line):
    """Convert a line of markdown syntax to html syntax"""
    line = convert_headings(line)

    return line


def convert_headings(line):
    """Convert headings at the start of a markdown str"""
    match = re.match('^(#{1,6}) (.+)', line)
    if not match:
        return line

    heading_level = len(match.group(1))

    return f'<h{heading_level}>{match.group(2)}</h{heading_level}>'


if __name__ == "__main__":
    main()
