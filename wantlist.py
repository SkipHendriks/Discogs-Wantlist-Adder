#!/usr/bin/env python

import pprint
import discogs_client
import argparse
import sys


DELIMITER = " || "

d = discogs_client.Client(
    'ExampleApplication/0.1',
    user_token="zBgDuMUoWCUtzYVtmKiTykvGMTXwKfdDlSisujtt"
)


def readFile(filename):
    with open(filename) as f:
        for line in f:
            album = findAlbum(line)
            addAlbum(album)


def readSTDIN(stdin):
    for line in stdin:
        album = findAlbum(line)
        addAlbum(album)


def findAlbum(line):
    artist = line[0:line.find(DELIMITER)]
    album = line[line.find(DELIMITER)+len(DELIMITER):]

    return d.search(
        artist=artist,
        release_title=album,
        format="Vinyl",
        type="release"
    )[0]


def addAlbum(album):
    pprint.pprint(vars(album))
    me = d.identity()
    me.wantlist.add(album)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "positional_file",
        type=str,
        nargs='?'
    )

    parser.add_argument(
        'pipe_input_file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    parser.add_argument(
        "-f",
        "--file",
        default=None,
        type=str,
        dest="optional_file",
        help="File with album-titles and artists delimited by '"+DELIMITER+"' (not including quotes)"
    )

    parser.add_argument(
        "-v",
        '--version',
        action='version',
        version='%(prog)s 0.1'
    )

    options = parser.parse_args()

    input_count = sum([bool(options.positional_file), bool(options.optional_file), not sys.stdin.isatty()])

    if input_count is 1:
        if(options.positional_file or options.optional_file):
            readFile(options.positional_file or options.optional_file)
        else:
            readSTDIN(options.pipe_input_file)
    elif input_count is 0:
        raise RuntimeError("Please specify a file location")
    else:
        raise RuntimeError("Please specify only one file")

if __name__ == "__main__":
    main()
