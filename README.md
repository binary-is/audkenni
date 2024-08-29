 # About

 This is a basic and presumably most commonly needed implementation of electronic IDs at [https://www.audkenni.is/](Auðkenni).

 It currently only supports authentication on SIM cards through the REST API, version v200.

# Usage

It is configured using the environment variables found in `env-example`:

    export AUDKENNI_CLIENT_ID="exampleId"
    export AUDKENNI_SECRET="secret-string"
    export AUDKENNI_BASE_URI="https://example.audkenni.is:443"
    export AUDKENNI_DEV_MODE="true"  # Set to "false" or "" in production.

The [`python-dotenv`](https://pypi.org/project/python-dotenv/) package is very handy for reading the `.env` file automatically.

The client ID, secret and base URI must be retrieved from Auðkenni by purchasing a subscription to their services.

There is a basic example script called `example_use.py` which can be used like so:

    cp env-example .env
    # Edit '.env' with your favorite editor.
    source .env
    ./example_use.py

Check `example_use.py` for instructions on how to use it.

It is licensed under the [MIT license](https://mit-license.org/) as per the `LICENSE` file.
