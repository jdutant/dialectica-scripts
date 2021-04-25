# Script copyright Thomas Hodgson 2021
# MIT License

"""
Dialectica open access initiative bibliography extractor, (c) Thomas Hodgson 2021
MIT License

The script takes a list of bibtex keys and a path to a bibtex file as --source.
The script prints a bibtex file of the entries from the source file that match the keys.
If the optional --output argument is given a path, then a bibtex file will be written there
instead of being printed.
The optional argument --keys can be used to provide a keyfile.
A keyfile is assumed to have one key per line. These keys are used to extract entries.

Depends on:

- argparse
- sys
- bibtexparser

"""

import argparse
import sys
import bibtexparser
from bibtexparser.bwriter import BibTexWriter

parser = argparse.ArgumentParser(
    description="Extract a bibliography from a bibtex file based on keys"
)
parser.add_argument(
    "entries",
    help="The entries to extract",
    nargs="*",
)
parser.add_argument(
    "--source",
    "-s",
    help="A bibliography file to get entries from",
)
parser.add_argument(
    "--output",
    "-o",
    help="A path to write the output to",
)
parser.add_argument(
    "--keys",
    "-k",
    help="A keyfile to get keys from",
)
args = parser.parse_args()

# A source is required
if not args.source:
    parser.error("No source provided")

# Parse the source bibliography file using bibtexparser
with open(args.source, "r") as in_file:
    bib_database = bibtexparser.load(in_file)

# Use a set to avoid duplicates
keys = set(args.entries)

if args.keys:
    # Add entries for the keyfile
    with open(args.keys) as in_file:
        # The entries should be stripped of white space, and newlines
        # Update the set with the set of these
        keys |= set(line.strip() for line in in_file.readlines())

# Check for entries that are not in the source database; send a list of them to sdterr
missing_keys = [key for key in keys if key not in bib_database.entries_dict]
if missing_keys:
    sys.stderr.write("\n".join(missing_keys) + "\n")
    # Update missing keys; this is required for the filtering below
    keys -= set(missing_keys)

# Filter out all the entries not in keys
bib_database.entries = [bib_database.entries_dict[key] for key in keys]

if args.output:
    # Write the database to the path specified by --output
    writer = BibTexWriter()
    with open(args.output, "w") as out_file:
        out_file.write(writer.write(bib_database))
else:
    # Write a bibtex string to stdout
    sys.stdout.write(bibtexparser.dumps(bib_database))
