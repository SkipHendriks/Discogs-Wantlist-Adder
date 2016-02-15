#!/usr/bin/env python3

import pprint
import discogs_client
import argparse
import sys

# Todo:
# 1. Implement OAuth
# 2. Add format option
# 3. Refactoring:
#    1. reading in main() ( will become handleUserInput())
#    2. findAlbum() called from addAlbum()
#    3. Add handleUserInput()


def readFile(filename, delimiter, revert):
    with open(filename) as f:
        for line in f:
            album = findAlbum(line, delimiter)
            if revert is True:
                removeAlbum(album)
            else:
                addAlbum(album)


def readSTDIN(stdin, delimiter, *revert):
    for line in stdin:
        album = findAlbum(line, delimiter)
        if revert is True:
            removeAlbum(album)
        else:
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


def removeAlbum(album):
    pprint.pprint(vars(album))
    me = d.identity()
    me.wantlist.remove(album)


def main():

    delimiter = ' || '

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
        help="File with album-titles and artists delimited by '"+delimiter+"' (not including quotes) or a chosen delimiter"
    )

    parser.add_argument(
        "-d",
        "--delimiter",
        default=None,
        type=str,
        dest="DELIMITER",
        help="Delimiter used in the specfied file. Defaults to '"+delimiter+"' (not including quotes) when not specified"
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
        help="Removes the specified files from your wantlist"
    )

    options = parser.parse_args()

    print(options.REVERT)

    input_count = sum([bool(options.FILE), not sys.stdin.isatty()])

    if input_count is 0:
        options.FILE = str(input("Please enter the location of your list file: "))
    elif input_count > 1:
        raise RuntimeError("Please specify only file or stdin")
    if not options.USER_TOKEN:
        options.USER_TOKEN = input("Please enter your Discogs Consumer Token: ")

    global d
    d = discogs_client.Client(
        'Discogs-Wantlist-Adder/0.1',
        user_token=options.USER_TOKEN
    )

    if options.DELIMITER:
        delimiter = options.DELIMITER
    if(options.FILE):
        readFile(options.FILE, delimiter, options.REVERT)
    else:
        readSTDIN(options.STDIN, delimiter, options.REVERT)

if __name__ == "__main__":
    main()
