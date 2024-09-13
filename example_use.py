#!/usr/bin/env python3

# Install `python-dotenv` for this to work:
#
#     from dotenv import load_dotenv
#     load_dotenv()

from audkenni import see_some_id  # Needs `load_dotenv()` before running.
from audkenni.exceptions import AudkenniWrongNumberException
from sys import argv
from sys import stderr


def usage():
    print('Usage: ./example_use.py <phone-number> "<message>"')
    print()
    quit(1)


def parse_arguments(argv):
    try:
        phone_number = argv[1]
        message = argv[2]
    except IndexError:
        usage()

    return phone_number, message


def main(argv):
    phone_number, message = parse_arguments(argv)

    try:
        person = see_some_id(phone_number, message)
    except AudkenniWrongNumberException:
        print("Error: Phone number seems without a valid electronic ID.", file=stderr)
        quit(2)

    print("Name: %s" % person["name"])
    print("SSN: %s" % person["nationalRegisterId"])
    print("Signature: %s" % person["signature"])


if __name__ == "__main__":
    main(argv)
