#! usr/bin/python
# Script copyright Thomas Hodgson
# MIT License

"""
Dialectica open access initiative self-citing bibliography file check, (c) Thomas Hodgson 2021
MIT License

The script takes files as arguments. The assumption is that these are biblatex files.
It looks for biblatex cite commands, and compares these to the biblatex entries in the files.
The following will be printed:

- the keys used in citation commands (if any)
- the missing keys that are not entries (if any)
- the entries in the file

Dependencies:

- re
- sys

"""

import re
import sys


for current_file in sys.argv[1:]:
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

    except FileNotFoundError:
        print("I couldn't find {}.".format(current_file))
