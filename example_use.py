#!/usr/bin/env python3

# Install `python-dotenv` for this to work:
#
#     from dotenv import load_dotenv
#     load_dotenv()

from audkenni import see_some_id  # Needs `load_dotenv()` before running.

person = see_some_id("8885629", "Innskráning")

print("Name: %s" % person["name"])
print("SSN: %s" % person["nationalRegisterId"])
print("Signature: %s" % person["signature"])
