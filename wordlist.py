#!/usr/bin/env python3
"""
This script is meant to serve as a functional example of how the xigt library can be used
to process xigt files.

 :author: Ryan Georgi <rgeorgi@uw.edu>
"""

import glob
import re
from argparse import ArgumentParser

from collections import defaultdict

from xigt import xigtpath
from xigt.codecs import xigtxml


def wordlist(filelist, gloss=None, meta=None):
    """
    This function takes a list of Xigt-XML ODIN files, looks for the
    'normalized' ODIN tier, and grabs the contents of all gloss and
    meta lines. It tokenizes simply by matching all word characters
    (using regex's `\w` escape) so as to pull out hyphenated and dotted
    gloss line tokens.

    The output is returned as a wordlist reverse sorted by count.

    :param filelist: List of input files to process.
    :type filelist: list[str]
    :param gloss: Path to use for the output gloss wordlist.
    :type gloss: str
    :param meta: Path to use for the output meta wordlist.
    :type meta: str
    """
    gloss_words = defaultdict(int)
    meta_words  = defaultdict(int)

    # -------------------------------------------
    # Iterate over all the paths in the list of files.
    # -------------------------------------------
    for path in filelist:
        with open(path, 'r', encoding='utf-8') as f:
            # Load the XigtCorpus, using the transient mode (most memory efficient)
            xc = xigtxml.load(f, mode='transient')

            # Now, iterate over each `Igt` instance in each file,
            for igt in xc:
                # Use a xigtpath expression to find the `tier` item that is a child of this node,
                # with state="normalized" as an attribute.
                norm_tier = xigtpath.find(igt, './tier[@state="normalized"]')

                # Next, since the `tag` attribute can be G+CR or M+AC etc., grab all lines
                # with a tag that starts with the desired tag letter.
                gloss_lines = [item for item in norm_tier if item.attributes['tag'].startswith("G")]
                meta_lines  = [item for item in norm_tier if item.attributes['tag'].startswith("M")]

                # Define a local function to update the wordlists for gloss and meta
                # lines.
                def update_count(l_l, words):
                    for l in l_l:
                        if l.value():
                            for w in l.value().split():
                                for sub_w in re.findall('[\w]+', w):  # <-- tokenize
                                    if sub_w.strip():
                                        words[sub_w.lower()] += 1 # <-- lowercase, and add

                # Update the counts.
                update_count(gloss_lines, gloss_words)
                update_count(meta_lines, meta_words)

    # Define a function to write out the wordlist objects to files.
    # here, we will reverse sort by frequency of the word, and
    # tab-delineate the columns.
    def write_items(words, path):
        if path:
            f = open(path, 'w', encoding='utf-8')
            items = sorted(words.items(), key=lambda x: (x[1], x[0]), reverse=True)
            for w, count in items:
                f.write('{}\t{}\n'.format(w, count))
            f.close()

    write_items(gloss_words, gloss)
    write_items(meta_words, meta)

# -------------------------------------------
# Main
# -------------------------------------------
if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('INFILES', nargs='+')
    p.add_argument('-g', '--gloss')
    p.add_argument('-m', '--meta')

    args = p.parse_args()

    filelist = []
    for infile in args.INFILES:
        filelist.extend(glob.glob(infile))

    wordlist(filelist, args.gloss, args.meta)
