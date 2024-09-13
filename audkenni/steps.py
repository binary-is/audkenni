import jwt
import pkce
import requests
from audkenni.config import CLIENT_ID
from audkenni.config import FAKE_REDIRECT_URI
from audkenni.config import HTTP_TIMEOUT
from audkenni.config import JSON_PATH
from audkenni.config import OAUTH_PATH
from audkenni.config import MAX_POLLING_SECONDS
from audkenni.config import POLLING_WAIT_SECONDS
from audkenni.config import SECRET
from audkenni.exceptions import AudkenniException
from audkenni.exceptions import AudkenniUserAbortedException
from audkenni.exceptions import AudkenniWrongNumberException
from audkenni.utils import verify_signature
from nanoid import generate
from time import sleep
from urllib.parse import parse_qs
from urllib.parse import urlparse

# Commonly used headers in JSON payloads.
json_headers = {
    "Content-Type": "application/json",
    "Accept-API-Version": "resource=2.0,protocol=1.0",
}


def step_1():
    response = requests.post(
        JSON_PATH + "authenticate?authIndexType=service&authIndexValue=api_v200",
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()

    # Payload that gets filled in later steps.
    payload = response.json()

    return payload


def step_2(payload, phone_number, prompt):

    # See step 2 in:
    # https://audkenni.atlassian.net/wiki/spaces/DOC/pages/5373853697/SIM+Authentication+using+REST+API+api_v201+NEW#Example-of-callback-answer-to-send-in-call

    # "Sláðu inn clientId"
    payload["callbacks"][0]["input"][0]["value"] = CLIENT_ID

    # "Sláðu inn Related Party"
    payload["callbacks"][1]["input"][0]["value"] = ""

    # "Sláðu inn símanúmer eða kennitölu"
    payload["callbacks"][2]["input"][0]["value"] = phone_number

    # "Sláðu inn skilaboð til notanda"
    payload["callbacks"][3]["input"][0]["value"] = prompt

    # "Nota vchoice (true eða false)"
    payload["callbacks"][4]["input"][0]["value"] = "false"

    # "Nota confirmMessage (true eða false)"
    payload["callbacks"][5]["input"][0]["value"] = "false"

    # "Sláðu inn Hash gildi"
    payload["callbacks"][6]["input"][0]["value"] = "false"

    # "Veldu auðkenningarleið"
    # NOTE: The index of "sim" isn't always the same between environments, so
    # we have to check its index.
    sim_index = payload["callbacks"][7]["output"][1]["value"].index("sim")
    payload["callbacks"][7]["input"][0]["value"] = sim_index

    response = requests.post(
        JSON_PATH + "authenticate?authIndexType=service&authIndexValue=api_v200",
        json=payload,
        headers=json_headers,
        timeout=HTTP_TIMEOUT,
    )
    if response.status_code == 200:
        auth_id = response.json()["authId"]
        return auth_id
    elif response.status_code == 401:
        raise AudkenniWrongNumberException(
            "Phone number does not seem to have a valid ID."
        )
    else:
        raise AudkenniException(
            "Unknown error occurred in communicating with remote server."
        )


def step_3(auth_id):
    payload = {
        "authId": auth_id,
        "callbacks": [
            {
                "type": "PollingWaitCallback",
                "output": [
                    {"name": "waitTime", "value": "5000"},
                    {
                        "name": "message",
                        "value": "templates.user.LoginTemplate.pollingwaitmessage",
                    },
                ],
            }
        ],
    }

    seconds_waited = 0
    while seconds_waited < MAX_POLLING_SECONDS:

        # Waiting in beginning of loop instead of the end, because it's
        # extremely unlikely for the process to complete within anything
        # reasonable we might put in `POLLING_WAIT_SECONDS`.
        sleep(POLLING_WAIT_SECONDS)
        seconds_waited += POLLING_WAIT_SECONDS

        response = requests.post(
            JSON_PATH + "authenticate",
            json=payload,
            headers=json_headers,
            timeout=HTTP_TIMEOUT,
        )

        if response.status_code == 200:
            data = response.json()
            if "tokenId" in data:
                # NOTE: The documentation claims that this `tokenId` is used as a
                # login session, but we seem to have no need for it.
                #
                # Instead, we only use its presence to indicate that we are ready
                # to receive more information in the next step (step 4).
                break
        elif response.status_code == 401:
            raise AudkenniUserAbortedException("The user aborted the operation.")
        else:
            raise AudkenniException(
                "Unknown error occurred in communicating with remote server."
            )

    cookie = response.headers["Set-cookie"]

    return cookie


def step_4(cookie):

    # 21-character random string.
    state = generate()

    code_verifier, code_challenge = pkce.generate_pkce_pair()

    payload = {
        "service": "api_v200",
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile signature",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "redirect_uri": FAKE_REDIRECT_URI,
    }

    response = requests.get(
        OAUTH_PATH + "authorize",
        params=payload,
        headers={
            "Cookie": cookie,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=HTTP_TIMEOUT,
        allow_redirects=False,
    )
    response.raise_for_status()

    # Get code from Location-header.
    location_header = response.headers.get("Location")
    query = parse_qs(urlparse(location_header).query)
    code = query.get("code").pop()

    return code, code_verifier


def step_5(cookie, code, code_verifier):

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": FAKE_REDIRECT_URI,
        "code_verifier": code_verifier,
        "code": code,
        "client_secret": SECRET,
    }

    response = requests.post(
        OAUTH_PATH + "access_token",
        params=payload,
        headers={
            "Cookie": cookie,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    if "access_token" not in data.keys():
        raise AudkenniException("Expected access token missing")

    if "id_token" not in data.keys():
        raise AudkenniException("Expected token ID missing")

    # Extract what we'll need.
    access_token = data["access_token"]
    id_token = data["id_token"]

    # Extract algorithm and key ID from ID token.
    unverified_header = jwt.get_unverified_header(id_token)
    algorithm = unverified_header.get("alg")
    key_id = unverified_header.get("kid")

    # Get public key data from Auðkenni.
    key_response = requests.get(OAUTH_PATH + "connect/jwk_uri", timeout=HTTP_TIMEOUT)
    key_response.raise_for_status()
    key_data = key_response.json()

    # Find the proper JWT key in Auðkenni's response.
    jwt_key = None
    for possible_jwt_key in key_data["keys"]:
        if possible_jwt_key["kid"] == key_id:
            jwt_key = possible_jwt_key

    # We expect the JWT key to be RSA.
    if jwt_key["kty"] != "RSA":
        raise AudkenniException("Unexpected JWT key type: %s" % jwt_key["kty"])

    # Get the public key from the JWT key.
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwt_key)

    # Verify the signature and decode the JWT payload from the ID token.
    jwt_payload = jwt.decode(
        data["id_token"],
        public_key,
        algorithms=algorithm,
        audience=CLIENT_ID,
        options={"verify_signature": True},
    )

    return access_token, jwt_payload["signature"]


def step_6(cookie, access_token, signature):
    response = requests.post(
        OAUTH_PATH + "userinfo",
        headers={
            "Cookie": cookie,
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}",
        },
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()

    data = response.json()
    person = {
        "name": data["name"],
        "nationalRegisterId": data["nationalRegisterId"],
        "signature": data["signature"],
    }

    if not verify_signature(person, signature):
        raise AudkenniException("Signature verification failed.")

    return person
