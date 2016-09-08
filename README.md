# odin-wordlister
Quick functional demo for how to use Xigt code on ODIN data.

## Usage
To run the script, simply do:

    ./wordlist.py <ODIN_XIGTXML_FILE[S]> -g <GLOSS_WORDLIST_OUTPUT> -m <META_WORDLIST_OUTPUT>
    
This will generate a wordlist of gloss and/or meta lines from the given ODIN files in Xigt-XML format.

Wildcards are accepted for the input files. (e.g. `odin-2.1/*.xml`)