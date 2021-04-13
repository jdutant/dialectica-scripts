#! usr/bin/python
# Script copyright Thomas Hodgson
# MIT License

"""
Dialectica open access initiative self-citing bibliography file check, (c) Thomas Hodgson 2021
MIT License

The script takes paths as arguments. The assumption is that these are biblatex files.
It looks for biblatex cite commands, and compares these to the biblatex entries in the files.
The following will be printed:

- the keys used in citation commands (if any)
- the missing keys that are not entries (if any)
- the entries in the file

If the option --source argument is given, the script tries to use bibtexparser to make an extended
biblatex file with missing entries added from the argument to --source. The new file will have value
of the optional argument --suffix added to the name of the original file.
The default value of --suffix is '_extended'.

Dependencies:

- argparse
- os
- re
- bibtexparser

"""

import argparse
import os
import re
import bibtexparser

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# Handle command line arguments
parser = argparse.ArgumentParser(
    description="Check bibliography files for self-citing keys"
)
parser.add_argument(
    "bibliographies",
    help="The bibliography files to check",
    nargs="+",
)
parser.add_argument(
    "--source",
    help="A bibliography file to get missing entries from",
)
parser.add_argument(
    "--suffix",
    help="Add this suffix to new bibliography files",
    default="_extended",
)
args = parser.parse_args()


for current_file in args.bibliographies:
    # open and read the current argument
    try:
        with open(current_file, "r") as in_file:
            bibliography = in_file.read()

        # Make sets of the citekeys found in the file, and of the entries,
        # and of the self cites missing from the entries
        # The self_keys regex matches an upper or lower case cite, citep, citeyear, citeauthor,
        # citeyearpar, and then anything between that and the first bracket
        # The self_keys regex doesn't handle lists of keys
        self_keys = set(
            re.findall(
                r"\\[C|c]ite[t|p|year|author|yearpar]?.*?\{\s*(.+?)\}", bibliography
            )
        )
        entries = set(re.findall(r"@.+?{(.+?)\,", bibliography))
        # The members of self_keys that are not in entries
        missing = self_keys - entries

        # Print the information
        print(
            "Dialectica open access initiative self-citing bibliography file check,",
            "(c) Thomas Hodgson 2021",
        )
        print("I'm checking: '{}'.".format(current_file))

        if self_keys:
            print(
                "I found these self-citing keys:",
                ", ".join(sorted(self_keys)),
                sep="\n",
            )

            if missing:
                print(
                    "These self-citing keys are missing from the file's entries:",
                    ", ".join(sorted(missing)),
                    sep="\n",
                )
            else:
                print("There are no missing self-citing keys.")

        else:
            print("I didn't find any keys self-citing other entries.")

        if entries:
            print(
                "For information, these are all the entries I found:",
                ", ".join(sorted(entries)),
                sep="\n",
            )
        else:
            print("I didn't find any entries")

        # Try to get the missing entries from the source bibliography
        if args.source and missing:
            # Use bibtexparser to get a dictionary from the file
            with open(args.source, "r") as in_file:
                source_database = bibtexparser.load(in_file)
            # Use bibtexparser to get a dictionary from the file
            with open(current_file, "r") as in_file:
                current_database = bibtexparser.load(in_file)
            # A list of the missing entries, represented as dictionaries
            missing_entries = [
                entry for entry in source_database.entries if entry["ID"] in missing
            ]
            # Create a new database, and add the entries from the current database
            # as well as the missing entries
            extended_database = BibDatabase()
            extended_database.entries = current_database.entries + missing_entries

            # Write to a file
            writer = BibTexWriter()
            # Make the name of a new file from the old and the suffix
            head, tail = os.path.split(current_file)
            root, ext = os.path.splitext(tail)
            new_file = os.path.join(head, root + args.suffix + ext)
            with open(new_file, "w") as out_file:
                out_file.write(writer.write(extended_database))
            print(
                "I looked at the source bibliography: '{}'.".format(args.source),
                "I wrote an extended bibliography file: '{}'.".format(new_file),
                sep="\n",
            )

    except FileNotFoundError:
        print("I couldn't find {}.".format(current_file))
