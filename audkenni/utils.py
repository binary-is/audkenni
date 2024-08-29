import base64
import requests
from audkenni.config import AUDKENNI_CERTIFICATES
from audkenni.config import HTTP_TIMEOUT
from cryptography import x509
from cryptography.hazmat.primitives.serialization.pkcs7 import (
    load_der_pkcs7_certificates,
)


def get_issuer_cert_from_url(issuer_cert_url):
    """
    Returns an issuer certificate from a provided URL.
    """
    # Get the issuer certificate from Auðkenni.
    response = requests.get(issuer_cert_url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()

    # Test-version is base-64 encoded, but production-version is in binary.
    if "-----BEGIN CERTIFICATE-----" in response.text:
        issuer_cert_data = base64.b64decode(
            response.text.replace("-----END CERTIFICATE-----", "")
            .replace("-----BEGIN CERTIFICATE-----", "")
            .replace("\n", "".replace("\r", ""))
        )
    else:
        issuer_cert_data = response.content

    issuer_cert = x509.load_der_x509_certificate(issuer_cert_data)
    return issuer_cert


def verify_issuance(cert, cert_url):
    """
    Verifies that the given certificate was issued by the provided issuer
    certificate.

    The native `.verify_directly_from_issued_by` works a bit strangely. It
    returns `None` on success and throws exceptions if something is wrong.

    This function encapsulates that process but returns a boolean.

    We need this because we are testing against more than one issuer cert.
    """

    issuer_cert = get_issuer_cert_from_url(cert_url)

    try:
        return cert.verify_directly_issued_by(issuer_cert) is None
    except Exception:
        # The following are descriptions of what different errors means. We
        # don't need to communicate them to the client, but perhaps this
        # information is useful during development.
        #
        # ValueError: "Issuer name does not match certificate issuer or the
        #              signature algorithm is not supported"
        #
        # TypeError: "The issuer does not have a supported public key type"
        #
        # x509.InvalidSignature: "The signature is invalid"
        return False

    # This should never happen because failure results in exception.
    return False


def verify_signature(person, signature):
    # Get certificate from signature.
    cert = load_der_pkcs7_certificates(base64.b64decode(signature))[0]

    # Check if we can find at least one valid certificate issuance.
    valid_signature_match = False
    for cert_url in AUDKENNI_CERTIFICATES:
        if verify_issuance(cert, cert_url):
            valid_signature_match = True
            break

    # Create a person object from the cert.
    cert_person = {at.oid._name: at.value for at in cert.subject}

    if (
        person["name"] == cert_person["commonName"]
        and person["nationalRegisterId"] == cert_person["serialNumber"]
        and valid_signature_match
    ):
        return True
    else:
        return False
