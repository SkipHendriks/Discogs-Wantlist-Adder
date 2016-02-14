#!/usr/bin/env python

import pprint
import discogs_client
import argparse
import sys


DELIMITER = " || "


def readFile(filename, delimiter):
    with open(filename) as f:
        for line in f:
            album = findAlbum(line, delimiter)
            addAlbum(album)


def readSTDIN(stdin, delimiter):
    for line in stdin:
        album = findAlbum(line, delimiter)
        addAlbum(album)


def findAlbum(line, delimiter):
    artist = line[0:line.find(delimiter)]
    album = line[line.find(delimiter)+len(delimiter):]

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

    global d

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'STDIN',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    parser.add_argument(
        "-u",
        "--user-token",
        default=None,
        type=str,
        dest="USER_TOKEN",
        help="User token to connect with the Discogs API. You can obtain a token from https://www.discogs.com/settings/developers"
    )

    parser.add_argument(
        "-f",
        "--file",
        default=None,
        type=str,
        dest="FILE",
        help="File with album-titles and artists delimited by '"+DELIMITER+"' (not including quotes) or a chosen delimiter"
    )

    parser.add_argument(
        "-d",
        "--delimiter",
        default=None,
        type=str,
        dest="DELIMITER",
        help="Delimiter used in the specfied file. Defaults to '"+DELIMITER+"' (not including quotes) when not specified"
    )

    parser.add_argument(
        "-v",
        '--version',
        action='version',
        version='%(prog)s 0.1'
    )

    parser.add_argument(
        "-r",
        "--revert",
        action='store_true',
        dest="REVERT",
        help="Removes the specified files from your wantlist (not yet implemented)"
    )

    options = parser.parse_args()

    input_count = sum([bool(options.FILE), not sys.stdin.isatty()])

    if input_count is 1:
        if options.USER_TOKEN:
            d = discogs_client.Client(
                'ExampleApplication/0.1',
                user_token=options.USER_TOKEN
            )
        else:
            raise RuntimeError("Please specify a user token")
        delimiter = options.DELIMITER or " || "
        if(options.FILE):
            readFile(options.FILE, delimiter)
        else:
            readSTDIN(options.STDIN, delimiter)
    elif input_count is 0:
        raise RuntimeError("Please specify a file location")
    else:
        raise RuntimeError("Please specify only file or stdin")


if __name__ == "__main__":
    main()
