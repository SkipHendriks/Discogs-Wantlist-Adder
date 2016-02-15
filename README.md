
<h1>Discogs Wantlist Adder</h1>

<h4>Adds albums from specified file to your Discogs wantlist.</h4>

I build this script to add my entire digital music library to my discogs wantlist in vinyl format. This is standard behavior, but this can be changed to a different format with the `--format` option.

<br />

<h3>Installation</h3>

1. Install Discogs API Client from your terminal using `pip3 install discogs_client`
2. Download and unzip.

If you don't have python 3 installed, download a recent version (at least 3.x) from their [website](https://www.python.org/downloads/ "Python's Homepage").

<h3>How to</h3>

1. Make a file with a list of Artists and Albums. Each line should first specify the artist, then have a common delimiter and specify the album after. Have a look at example.list for an example on how to do this.
2. Specify this file with `-f` or `--file`
3. If you did not use the standard delimiter specify your used delimiter with `-d` or `--delimiter`.
4. Obtain a Consumer Token from Discogs.com
5. Specify the obtained token with `-u` or `--user-token`.

If this doesn't help you at all open up a command-line terminal like PowerShell (Windows) or Terminal (Linux / OSX), navigate to the folder you dowloaded the file to using the `cd` command. Type `man cd` and press enter if you're at a loss here too. Then use the script by typing ./wantlist.py and adding the required parameters.

Your final command could look like this:
```bash
./wantlist.py --file yourfile.list --user-token your-token-here --delimiter 'your-delimiter'
```