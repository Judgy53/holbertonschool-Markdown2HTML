#!/usr/bin/python3
"""This module is used to convert markdown to html.
    Usage: markdown2html.py README.md README.html
"""

import sys
import os.path
import re
import hashlib


class ParsingState():
    def __init__(self) -> None:
        self.unordered_list_started = False
        self.ordered_list_started = False
        self.paragraph_started = False


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
    if line.endswith('\n'):  # Remove trailing new line to avoid duplicates
        line = line[:-1]

    line = convert_headings(line)
    line = convert_unordered_list(line, state)
    line = convert_ordered_list(line, state)
    line = convert_paragraph(line, state)
    line = convert_emphasis(line, "**", "b")
    line = convert_emphasis(line, "__", "em")
    line = convert_md5(line)
    line = convert_remove_letter(line, 'c')

    return line + '\n'


def convert_headings(line):
    """Convert headings at the start of a markdown str"""
    match = re.match(r'^(#{1,6}) (.+)', line)
    if not match:
        return line

    heading_level = len(match.group(1))

    return f'<h{heading_level}>{match.group(2)}</h{heading_level}>'


def convert_unordered_list(line, state):
    """Convert unordered list at the start of a markdown str"""
    match = re.match(r'^- (.+)', line)
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


def convert_ordered_list(line, state):
    """Convert unordered list at the start of a markdown str"""
    match = re.match(r'^\* (.+)', line)
    if not match:
        if state.ordered_list_started:
            state.ordered_list_started = False
            return f'</ol>\n' + line
        else:
            return line

    out = ''
    if not state.ordered_list_started:
        out += '<ol>\n'
        state.ordered_list_started = True
    out += f'<li>{match.group(1)}</li>'

    return out


def convert_paragraph(line, state):
    """Convert simple text into html paragraph"""
    is_simple_text = len(line) > 0 and line[0] != '<'
    if not is_simple_text:
        if state.paragraph_started:
            state.paragraph_started = False
            return '</p>\n' + line
        else:
            return line

    out = ''
    if state.paragraph_started:
        out += '<br/>\n'
    else:
        out += '<p>\n'
        state.paragraph_started = True
    out += line

    return out


def convert_emphasis(line, markdown_tag, html_tag):
    """Convert text emphasis to html tags"""
    markdown_tag = re.escape(markdown_tag)
    pattern = re.compile(f'{markdown_tag}(.+?){markdown_tag}')

    m = re.search(pattern, line)
    while m:
        converted = '<{1}>{0}</{1}>'.format(m.group(1), html_tag)
        line = re.sub(re.escape(m.group(0)), converted, line)
        m = re.search(pattern, line)

    return line


def convert_md5(line):
    """Convert text between angled brackets to md5"""
    pattern = re.compile(r'\[\[(.+)\]\]')
    m = re.search(pattern, line)
    while m:
        converted = hashlib.md5(m.group(1).encode('utf-8')).hexdigest()
        line = re.sub(re.escape(m.group(0)), converted, line)
        m = re.search(pattern, line)

    return line


def convert_remove_letter(line, letter):
    """Remove a letter from text between parenthesis"""
    pattern = re.compile(r'\(\((.+)\)\)')
    replace_letter_pattern = re.compile(letter, re.IGNORECASE)

    m = re.search(pattern, line)
    while m:
        converted = replace_letter_pattern.sub('', m.group(1))
        line = re.sub(re.escape(m.group(0)), converted, line)
        m = re.search(pattern, line)

    return line


def check_for_missing_closures(state):
    """Closes opened tags."""
    out = ''
    if state.unordered_list_started:
        out += convert_unordered_list('', state)

    if state.ordered_list_started:
        out += convert_ordered_list('', state)

    if state.paragraph_started:
        out += convert_paragraph('', state)

    return out


if __name__ == "__main__":
    main()
