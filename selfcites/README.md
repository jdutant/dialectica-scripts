Selfcites.py
============

Checks whether a BibTex/BibLaTeX file contains self-citations, 
adds them from a specified source if provided.

(c) Thomas Hodgson 2021, MIT License (see LICENSE file at this repository's root.)

## Pre-requisites

* Python 3, including some standard modules (`os`, `argparse`).
* if using the script to supplement missing citations from a specificied
  source, the [bibtexparser](https://bibtexparser.readthedocs.io/en/master/install.html#how-to-install) python package. This can be installed using
  the package installer for python: run `pip3 install bibtexparser` on 
  the command line.

## Usage

"BibTeX" below refers to both BibTeX and BibLaTeX files.

### Checking if a BibTeX file contains self-citing keys and if any is missing

Place the script `selfcites.py` in a suitable folder. On the command line:

```
python3 selfcites.py mybibliography.bib
```

The script will display the file's self-citing keys, if any, as a comma separated list. 

Of course if the script and/or the `.bib` file are in different folders than
the present working one, you should specify their paths, e.g.:

```
python3 ../resources/scripts/selfcites.py myarticle/mybibliography.bib
```

### Checking several BibTeX files

You can specify several files, or all BibTeX files at a given location:

```
python3 selfcites.py introduction.bib chapter1.bib
python3 selfcites.py book/*.bib
```

### Adding missing entries from a specified source file, if found

To look for and add any self-citing key's missing entries in a source bibliography file:

```
python3 selfcites.py mybibliography.bib --source masterbiblio.bib
```

The resulting bib file will be saved as `<yourbibfilename>_extended.bib`. You
can specify a custom suffix instead of the default `_extended` with the 
`--suffix` option:

```
python3 selfcites.py mybibliography.bib --source masterbiblio.bib --suffix "_finished"
```



