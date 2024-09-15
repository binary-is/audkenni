from os import environ

CLIENT_ID = environ.get("AUDKENNI_CLIENT_ID", "")
SECRET = environ.get("AUDKENNI_SECRET", "")
BASE_URI = environ.get("AUDKENNI_BASE_URI", "https://example.audkenni.is:443")
DEV_MODE = environ.get("AUDKENNI_DEV_MODE", "") == "true"

# Optionally used when authenticating on behalf of another party.
RELATED_PARTY = environ.get("AUDKENNI_RELATED_PARTY", "")

# Unlikely to change but centrally defined.
POLLING_WAIT_SECONDS = 2
MAX_POLLING_SECONDS = 30
HTTP_TIMEOUT = 20

# Short-hands for common remote paths so that we don't have to concatenate the
# same strings over and over.
JSON_PATH = BASE_URI + "/sso/json/realms/root/realms/audkenni/"
OAUTH_PATH = BASE_URI + "/sso/oauth2/realms/root/realms/audkenni/"

# Auðkenni certificates. Some electronic IDs are issued by one of those, but
# other IDs by the other. Unlikely to change without this package also
# requiring an update, so we hard-code them here instead of configuring them as
# environment variables.
AUDKENNI_CERTIFICATES = [
    "https://skrar.audkenni.is/skilrikjakedjur/islandsrot/Fullgiltaudkenni2021.cer",
    "https://skrar.audkenni.is/skilrikjakedjur/islandsrot/older/Milliskilriki.cer",
]
if DEV_MODE:
    # Only relevant while developing.
    AUDKENNI_CERTIFICATES.append(
        "https://repo.audkenni.is/Skilriki/certs/FAP2021test.cer",  # Test
    )

# This must be provided in some calls to Auðkenni, even though it isn't used
# and serves no purpose. It must match the configured redirection URI on
# Auðkenni's side but there is **not** a need for a corresponding callback URI
# on our side. It is not configurable in `.env` or `settings` because it
# isn't really a setting, but rather a quirky, vestigial requirement.
FAKE_REDIRECT_URI = "http://localhost:3000/callback"
