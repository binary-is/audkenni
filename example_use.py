#!/usr/bin/env python3

# Install `python-dotenv` for this to work:
#
#     from dotenv import load_dotenv
#     load_dotenv()

from audkenni import see_some_id  # Needs `load_dotenv()` before running.
from audkenni.exceptions import AuthException
from audkenni.exceptions import AuthInProgressException
from audkenni.exceptions import UserAbortedException
from audkenni.exceptions import TimeoutException
from audkenni.exceptions import WrongNumberException
from sys import argv
from sys import stderr


def usage():
    print('Usage: ./example_use.py <phone-number> "<message>"')
    print()
    quit(1)


def parse_arguments(argv):
    phone_number = ""
    message = ""
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

        # Signature verification can optionally be skipped like so. It is not
        # recommended, but some IDs don't seem to support them.
        # person = see_some_id(phone_number, message, skip_signature_verification=True)
    except AuthException:
        print("Error: Authentication failed.")
        quit(16)
    except AuthInProgressException:
        print("Error: Authentication already in progress.")
        quit(32)
    except UserAbortedException:
        print("Error: The user aborted the operation.")
        quit(4)
    except TimeoutException:
        print("Error: Operation timed out.")
        quit(8)
    except WrongNumberException:
        print("Error: Phone number seems without a valid electronic ID.", file=stderr)
        quit(2)

    print("Name: %s" % person["name"])
    print("SSN: %s" % person["nationalRegisterId"])
    print("Signature: %s" % person["signature"])


if __name__ == "__main__":
    main(argv)
