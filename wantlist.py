#!/usr/bin/env python3

import pprint
import discogs_client
import argparse
import sys

# Todo:
# 1. Implement OAuth
# 2. Refactoring:
#    1. reading in main() ( will become handleUserInput())
#    2. findAlbum() called from addAlbum()
#    3. Add handleUserInput()
# 3. Add Progress bar


def readFile(filename, delimiter, revert, album_format):
    with open(filename) as f:
        for line in f:
            album = findAlbum(line, delimiter, album_format)
            if album:
                if revert is True:
                    removeAlbum(album)
                else:
                    addAlbum(album)


def readSTDIN(stdin, delimiter, revert, album_format):
    for line in stdin:
        album = findAlbum(line, delimiter, album_format)
        if album:
            if revert is True:
                removeAlbum(album)
            else:
                addAlbum(album)


def findAlbum(line, delimiter, album_format):
    artist = line[0:line.find(delimiter)]
    album = line[line.find(delimiter)+len(delimiter):]

    results = d.search(
        artist=artist,
        release_title=album,
        format=album_format,
        type="release"
    )

    if len(results) > 0:
        return results
    else:
        print(album + ' by ' + artist + ' was not found as ' + album_format)
        return None


def addAlbum(albums):
    me = d.identity()
    for album in albums:
        pprint.pprint(album)
        me.wantlist.add(album)


def removeAlbum(albums):
    me = d.identity()
    for album in albums:
        pprint.pprint(album)
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

    parser.add_argument(
        "--format",
        type=str,
        dest="FORMAT",
        help="Album format you want in your wantlist (eg. Vinyl, CD, 12\", Cassette...)"
    )

    options = parser.parse_args()

    input_count = sum([bool(options.FILE), not sys.stdin.isatty()])

    if input_count is 0:
        options.FILE = input("Please enter the location of your list file: ")
    elif input_count > 1:
        raise RuntimeError("Please specify only file or stdin")
    if not options.USER_TOKEN:
        options.USER_TOKEN = input("Please enter your Discogs Consumer Token: ")

    global d
    d = discogs_client.Client(
        'Discogs-Wantlist-Adder/0.1',
        user_token=options.USER_TOKEN
    )

    album_format = "Vinyl"

    if options.FORMAT:
        album_format = options.FORMAT

    if options.DELIMITER:
        delimiter = options.DELIMITER
    if(options.FILE):
        readFile(options.FILE, delimiter, options.REVERT, album_format)
    else:
        readSTDIN(options.STDIN, delimiter, options.REVERT, album_format)

if __name__ == "__main__":
    main()
