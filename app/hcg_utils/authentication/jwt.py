"""Module containing JWT logic."""
import json
import base64
import jwt
import logging

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.request import urlopen
from flask import current_app
from cachetools import cached

logger = logging.getLogger(__name__)


def get_target_audience():
    # Allow this to be mocked out easily
    return current_app.config.get('JWT_AUDIENCE')


def load_certificate(x5c: bytes) -> x509:
    """
    Load x509 certificate DER data.
    :param x5c:
    :return:
    """
    key_data = base64.decodebytes(x5c.encode("utf-8"))
    certificate = x509.load_der_x509_certificate(key_data, backend=default_backend())

    return certificate


def _decode_token_without_verify(token: str) -> dict:
    """
    Insecurely decode a token, for DEV only
    """
    try:
        return jwt.decode(token, verify=False)
    except (
            jwt.InvalidSignatureError,
            jwt.InvalidIssuedAtError,
            jwt.InvalidIssuerError,
            jwt.ExpiredSignatureError,
            jwt.InvalidAudienceError,
            jwt.DecodeError,
            TypeError
    ):
        logger.exception('Error decoding the token')
        return {}


def _decode_token_with_verify(token: str) -> dict:
    """
    Decode a jwt token.

    :param token: The token to decode.
    :type token: str
    :return: A dict containing the payload
    """
    unverified_header = {}
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError:
        logger.exception('Error decoding the unverified_header')
        return {}

    kid = unverified_header.get("kid")
    if kid is None:
        logger.error(f'Token did not include a "kid" header')
        return {}
    public_key = get_jwks(kid)
    if not public_key:
        logger.error('Could not load requested public key from the JWKS')
        return {}

    aud = get_target_audience()

    try:
        return jwt.decode(token, public_key, audience=aud, algorithms=['RS256'])
    except (
            jwt.InvalidSignatureError,
            jwt.InvalidIssuedAtError,
            jwt.InvalidIssuerError,
            jwt.ExpiredSignatureError,
            jwt.InvalidAudienceError,
            jwt.DecodeError,
            TypeError
    ):
        logger.exception('Error decoding the token')
        return {}


def decode_token(token: str, verify: bool=True) -> dict:
    """
    Decode a jwt token.

    :param token: The token to decode.
    :type token: str
    :param verify: Whether to verify the token
    :type verify: bool
    :return: A dict containing the payload
    """
    if verify is False:
        logger.warning('Insecurely decoding the token, should only be used in DEV')
        return _decode_token_without_verify(token)
    return _decode_token_with_verify(token)


def get_decode_key(token: str) -> str:
    """
    Retrieve the key to decode a JWT token.
    :param token: The JWT Token
    :type token: str
    :return: The key to decode the token.
    """
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header["kid"]
    key = get_jwks(kid)

    return key


def fetch_jwks() -> dict:
    """
    Fetch a JWKS from the well known location.

    It will return a version of the JWKS from the cache, if it exists.
    """
    key_json = urlopen(current_app.config['JWKS_ENDPOINT'])
    jwks = json.loads(key_json.read())
    return jwks["keys"]


CACHE = {}  # Needed to allow the cache to be "cleared" in unittests


@cached(CACHE)
def get_jwks(kid):
    """
    Check if a KID exists in the current cached JWKS.

    If not, it clears the cache and fetch it again.
    :param kid: The kid of the key.
    :return: The certificate.
    """
    jwks = fetch_jwks()
    for item in jwks:
        if item["kid"] == kid:
            certificate = load_certificate(item["x5c"][0])
            return certificate.public_key()

    return False
