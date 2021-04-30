Keys2bib.py
============

Extracts specified entries for a BibTex/BibLaTeX file

(c) Thomas Hodgson 2021, MIT License (see LICENSE file at this repository's root.)

## Pre-requisites

* Python 3, including some standard modules (`sys`, `argparse`).
* The [bibtexparser](https://bibtexparser.readthedocs.io/en/master/install.html#how-to-install) python package. This can be installed using
  the package installer for python: run `pip3 install bibtexparser` on 
  the command line.

## Usage

"bibtex" below refers to both BibTeX and BibLaTeX files.

The script takes a list of bibtex keys and a path to a bibtex file as --source.
The script prints a bibtex file of the entries from the source file that match the keys.
If the optional --output argument is given a path, then a bibtex file will be written there
instead of being printed.
The optional argument --keys can be used to provide a keyfile.
A keyfile is assumed to have one key per line. These keys are used to extract entries.
