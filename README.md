# About

This is a basic and presumably most commonly needed implementation of electronic IDs at [Auðkenni](https://www.audkenni.is/).

It currently only supports authentication on SIM cards through the REST API, version v200.

# Usage

It is configured using the environment variables found in `env-example`:

    export AUDKENNI_CLIENT_ID="exampleId"
    export AUDKENNI_SECRET="secret-string"
    export AUDKENNI_BASE_URI="https://example.audkenni.is:443"
    export AUDKENNI_DEV_MODE="true"  # Set to "false" or "" in production.

The [`python-dotenv`](https://pypi.org/project/python-dotenv/) package is very handy for reading the `.env` file automatically.

The client ID, secret and base URI must be retrieved from Auðkenni by purchasing a subscription to their services. They will provide you with a testing client ID for development purposes, but you must contact them directly for that.

There is a basic example script called `example_use.py` which can be used like so:

    cp env-example .env
    # Edit '.env' with your favorite editor.
    source .env
    ./example_use.py <phone-number> "<message>"

# Security

**USE THIS SOFTWARE AT YOUR OWN RISK.**

While the instructions from Auðkenni were followed with the utmost diligence, the authors of this software **cannot** and therefore **do not** guarantee that it is secure.

However, the code was explicitly written to be as easily reviewable as possible, reflecting the step-by-step process as explained in Auðkenni's instructions. In particular, the main function `audkenni.see_some_id` (in the file `audkenni/__init__.py`) is composed of 6 functions, `step_1`, `step_2`, `step_3` etc., with each function reflecting the corresponding step in the instructions. So while we cannot guarantee that it is secure, we have made every effort to make sure that if there are any pitfalls in it, that they be noticed and fixed as quickly as possible. Feel free to help and contribute!

# License

It is licensed under the [MIT license](https://mit-license.org/) as per the `LICENSE` file.
