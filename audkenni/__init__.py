from audkenni.steps import step_1
from audkenni.steps import step_2
from audkenni.steps import step_3
from audkenni.steps import step_4
from audkenni.steps import step_5
from audkenni.steps import step_6


def see_some_id(phone_number: str, prompt: str) -> dict:

    # These steps reflect the steps described in the documentation at:
    # https://audkenni.atlassian.net/wiki/spaces/DOC/pages/5289738241/SIM+Authentication+using+REST+API+api_v200

    # STEP 1/6
    #
    # Receive JSON payload already containing `authId` for subsequent requests,
    # to be filled out and re-used as a payload in step 2.
    #
    payload = step_1()

    # STEP 2/6
    #
    # Send a request with the prompt to the phone number.
    #
    # The payload from step 1 already contains the appropriate `authId`.
    #
    # We send the payload from step 1 instead of constructing it inside step 2,
    # because the order of options in it may differ between services, namely
    # between testing vs. production environments.
    #
    # It is step 2's responsibility to ensure that the payload's format is
    # respected in the form in which it arrived in step 1.
    #
    auth_id = step_2(payload, phone_number, prompt)

    # STEP 3/6
    #
    # Get a cookie which establishes our session.
    #
    # NOTE: The documentation claims that the `tokenId` gives us the login
    # session. It appears that we don't really need to use it as a session
    # token, though. We only seem to ever need the cookie.
    #
    cookie = step_3(auth_id)

    # STEP 4/6
    #
    # TODO: Missing explanatory comment.
    #
    code, code_verifier = step_4(cookie)

    # STEP 5/6
    #
    # TODO: Missing explanatory comment.
    #
    access_token, signature = step_5(cookie, code, code_verifier)

    # STEP 6/6
    #
    # TODO: Missing explanatory comment.
    #
    person = step_6(cookie, access_token, signature)

    return person
