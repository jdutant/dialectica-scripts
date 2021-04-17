#! usr/bin/python
# Script copyright Thomas Hodgson 2021
# MIT License

"""
Dialectica open access initiative self-citing bibliography file check, (c) Thomas Hodgson 2021
MIT License

The script takes paths as arguments. The assumption is that these are biblatex files.
It looks for biblatex cite commands, and compares these to the biblatex entries in the files.
The following will be printed, unless the --quiet option is set:

- the keys used in citation commands (if any)
- the missing keys that are not entries (if any)
- the entries in the file

If the option --source argument is given, the script tries to use bibtexparser to make an extended
biblatex file with missing entries added from the argument to --source.
The new file will have the value of the optional argument --suffix added to the name of the original
file.
The default value of --suffix is '_extended'.
If the optional --directory argument is given, the script will look for files in a directory with at
that path with the extension specified by the optional --extension argument. The default is 'bib'.

Requires python 3. Dependencies:

- argparse
- glob
- os
- re
- bibtexparser

"""

import argparse
import glob
import os
import re

# import bibtexparser: below, depending on whether a --source argument is specified

# Handle command line arguments
parser = argparse.ArgumentParser(
    description="Check bibliography files for self-citing keys"
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--verbose",
    action="store_true",
    help="Print information about what the script does",
    default=True,
)
group.add_argument(
    "--quiet",
    action="store_true",
    help="Do not print information about what the script does",
    default=False,
)
parser.add_argument(
    "bibliographies",
    help="The bibliography files to check",
    nargs="*",
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
parser.add_argument(
    "--directory",
    help="Look in this directory for biblatex files",
)
parser.add_argument(
    "--extension",
    help="The extension for bibliography files",
    default="bib",
)
args = parser.parse_args()

# if a --source option is provided, we need bibtexparser
if args.source:
    import bibtexparser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase

# If --quiet is set, args.verbose is false
if args.quiet:
    args.verbose = False

# Print script information message
if args.verbose:
    print(
        "Dialectica open access initiative self-citing bibliography file check",
        "(c) Thomas Hodgson 2021",
        sep="\n",
    )

# Make a list of biblatex files to run on
# Take the positional arguments
bibliographies = args.bibliographies
# Add what is in the specified directory
if args.directory:
    bibliographies += glob.glob(
        os.path.join(args.directory, "*.{}".format(args.extension))
    )

# Tell the user which directory was looked at, and what extension was used
if args.verbose:
    if args.directory:
        print(
            "I was asked to look at the directory '{}' for files with the extension '.{}'.".format(
                args.directory, args.extension
            )
        )
        # Check whether the directory exists, and tell the user if not
        if not os.path.isdir(args.directory):
            print("There is no directory '{}'.".format(args.directory))

    # Tell the user which files are being looked for

    if bibliographies:
        print(
            "I am looking for these bibliographies:",
            ", ".join(sorted(bibliographies)),
            sep="\n",
        )

for current_file in bibliographies:
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

        if args.verbose:
            # Print the information
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
                print("I didn't find any self-citing keys.")

            if entries:
                print(
                    "For information, these are all the entries I found:",
                    ", ".join(sorted(entries)),
                    sep="\n",
                )
            else:
                print("I didn't find any entries.")

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
            if args.verbose:
                # Print a message about what was written
                print(
                    "I looked at the source bibliography: '{}'.".format(args.source),
                    "I wrote an extended bibliography file: '{}'.".format(new_file),
                    sep="\n",
                )

    except FileNotFoundError:
        if args.verbose:
            print("I couldn't find {}.".format(current_file))
