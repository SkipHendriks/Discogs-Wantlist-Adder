
<h1>Discogs Wantlist Adder</h1>

<h4>Adds albums from specified file to your Discogs wantlist.</h4>


<h3>How to</h3>

1. Make a file with a list of Artists and Albums. Each line should first specify the artist, then have a common delimiter and specify the album after. Have a look at example.list for an example on how to do this.
2. Specify this file with -f or --file
3. If you did not use the standard delimiter specify your used delimiter with -d or --delimiter.
4. Obtain a Consumer Token from Discogs.com
5. Specify the obtained token with -u or --user-token.

If this doesn't help you at all open up your a comand-line terminal like PowerShell (Windows) or Terminal (Linux / OSX), navigate to the folder using the cd command. Type 'man cd' and press enter if you're at a loss here to. Then use the script by typing ./wantlist.py and adding the required parameters.

Your final command could look like this: ./wantlist.py -f yourfile.list -u your-toke-here -d 'your-delimiter'