#!/usr/bin/python3
"""This module is used to convert markdown to html.
    Usage: markdown2html.py README.md README.html
"""

import sys
import os.path
import re

class ParsingState():
    def __init__ (self) -> None:
        self.unordered_list_started = False

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
    state = ParsingState()

    try:
        for line in markdown_file.readlines():
            output_str += convert_line(line, state)
    finally:
        markdown_file.close()

    output_str += check_for_missing_closures(state)

    with open(args[1], 'w') as out_file:
        out_file.write(output_str)


def convert_line(line, state):
    """Convert a line of markdown syntax to html syntax"""
    line = convert_headings(line)
    line = convert_unordered_list(line, state)

    return line + '\n'


def convert_headings(line):
    """Convert headings at the start of a markdown str"""
    match = re.match('^(#{1,6}) (.+)', line)
    if not match:
        return line

    heading_level = len(match.group(1))

    return f'<h{heading_level}>{match.group(2)}</h{heading_level}>'


def convert_unordered_list(line, state):
    """Convert headings at the start of a markdown str"""
    match = re.match('^- (.+)', line)
    if not match:
        if state.unordered_list_started:
            state.unordered_list_started = False
            return f'</ul>\n' + line
        else:
            return line
        
    out = ''
    if not state.unordered_list_started:
        out += '<ul>\n'
        state.unordered_list_started = True
    out += f'<li>{match.group(1)}</li>'

    return out

def check_for_missing_closures(state):
    """Closes opened lists and similar tags."""
    out = ''
    if state.unordered_list_started:
        out += convert_unordered_list('', state)

    return out

if __name__ == "__main__":
    main()
