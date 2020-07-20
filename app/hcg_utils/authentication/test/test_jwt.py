from unittest.mock import MagicMock
from .. import jwt


UNSIGNED_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpc3MiOiJIQ1gtSUFQIiwiY29tLmhjZ2Z1bmRzLmhjeC91c2VyIjp7Imxhc3RfbmFtZSI6IlVzZXIiLCJmaXJzdF9uYW1lIjoiVGVzdCIsInJvbGVzIjpbWyJsY3giLCJhY2Nlc3MiXSxbImxjeCIsInVwZGF0ZSJdXSwiaWRlbnRpZmllciI6ImxvZ2FuQGhjZ2Z1bmRzLmNvbSJ9LCJpYXQiOjE1ODAzMTM5NzUsImNvbS5oY2dmdW5kcy5oY3gvYWN0aW9uIjoiYWNjZXNzIiwiYXVkIjoibGN4IiwiZXhwIjo0MDcwOTA4ODAwLCJuYmYiOjE1ODAzMTM5NzUsInN1YiI6ImxvZ2FuQGhjZ2Z1bmRzLmNvbSJ9.'


SIGNED_TOKEN = 'eyJraWQiOiJRMFk0T1VaRVJEYzJRVVZET1RZNFJVVkNSVFpET1RSR1JUVTVOa1ExUmpVMk9FTkJRa1pCTmc9PSIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJIQ1gtSUFQIiwiY29tLmhjZ2Z1bmRzLmhjeFwvdXNlciI6eyJsYXN0X25hbWUiOiJPd2VuIiwiZmlyc3RfbmFtZSI6IkxvZ2FuIiwicm9sZXMiOltbImhlYWRlci1lY2hvIiwiYWNjZXNzIl1dLCJpZGVudGlmaWVyIjoibG9nYW5AaGNnZnVuZHMuY29tIn0sImlhdCI6MTU4MDMxNDE2NCwiY29tLmhjZ2Z1bmRzLmhjeFwvYWN0aW9uIjoiYWNjZXNzIiwiYXVkIjoiaGVhZGVyLWVjaG8iLCJleHAiOjE1ODAzMTQxNzksIm5iZiI6MTU4MDMxNDE2NCwic3ViIjoibG9nYW5AaGNnZnVuZHMuY29tIn0.HpxgC47abrKdRJoCxAhD1H-gCNIWDyYjnMEffcciA5uyA6GgZK3qz6o8z0OZ9OFILVQkRKEMr-adJdaKY2PdlpGlHIg2Vx1UGNSOtuCdmZAjpxhroAb3AD3li2tagNuBCNeLeyyICGRi-YeefDvWCLNOijI7Rq4NrSBAF8ZGvBmi7I26cC3O7IYz9jb08XIKelk9JRR58lLcZt-rtLk0gfw13gayAJMphRAGs8ka7EsWflak0N3C-2hlLVM54XopI-ijjJt_a5nhaNk_xunLl04TwuR7lP1akCBjoTdd14ydSj3H3V5oTciKI9IeGW-M2aCAcTuM-SFFVM_Xcty29g'


def test_decode_unsigned_token_with_verify():
    result = jwt.decode_token(UNSIGNED_TOKEN)
    assert result == {}


def test_decode_garbled_token():
    result = jwt.decode_token('a random string')
    assert result == {}


def test_decode_unsigned_token_no_verify():
    result = jwt.decode_token(UNSIGNED_TOKEN, verify=False)
    assert result != {}
    assert result['sub'] == 'logan@hcgfunds.com'


def fetch_jwks_response():
    return [
        {
            "kty": "RSA",
            "n": "odnDosdisoyKvJMVdicL6zuSrelP-WroyIDWL6SLMFSDiwY5D8AkzlvlsylRyKl7SfTq2wPEX75x0uFTwBtz5lo4oyk77o_QF0lJbJFRa-clv0gqAS0gVnQD1i7BzZxdc72tADWvbooOCI3p8h6kUzeJySCOH-NF2m3CBDmet61w5CfnvKIZTfdGL4B97KbsSnqzPhpYAOAz3wpmloS25CVa9B3XmIHHLvmBdT7g0OWh3iwz3TXq58gqGsPzxPfLZTqZb7nO022GAirjFSoQ2puiQkTu6MVbuUqLo2S5zeMRzwa7nDlitz7KICgwo0UjrdiHv0-WADK4qLPF8eO2TQ",
        "e": "AQAB",
            "use": "sig",
            "alg": "RS256",
            "kid": "Q0Y4OUZERDc2QUVDOTY4RUVCRTZDOTRGRTU5NkQ1RjU2OENBQkZBNg==",
            "x5c": ["MIIDAzCCAeugAwIBAgIUflUu3t/1JCV9a85rbW+XSCwm80AwDQYJKoZIhvcNAQELBQAwITEfMB0GA1UEAwwWbG9naW4uaGN4LmhjZ2Z1bmRzLmNvbTAeFw0yMDAxMjYyMjIzNTRaFw0yMDAyMjYyMjIzNTRaMCExHzAdBgNVBAMMFmxvZ2luLmhjeC5oY2dmdW5kcy5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCh2cOix2KyjIq8kxV2JwvrO5Kt6U/5aujIgNYvpIswVIOLBjkPwCTOW+WzKVHIqXtJ9OrbA8RfvnHS4VPAG3PmWjijKTvuj9AXSUlskVFr5yW/SCoBLSBWdAPWLsHNnF1zva0ANa9uig4IjenyHqRTN4nJII4f40XabcIEOZ63rXDkJ+e8ohlN90YvgH3spuxKerM+GlgA4DPfCmaWhLbkJVr0HdeYgccu+YF1PuDQ5aHeLDPdNernyCoaw/PE98tlOplvuc7TbYYCKuMVKhDam6JCRO7oxVu5SoujZLnN4xHPBrucOWK3PsogKDCjRSOt2Ie/T5YAMrios8Xx47ZNAgMBAAGjMzAxMCEGA1UdEQQaMBiCFmxvZ2luLmhjeC5oY2dmdW5kcy5jb20wDAYDVR0TAQH/BAIwADANBgkqhkiG9w0BAQsFAAOCAQEAhSOZZiRpR8/BYm+62TvH3aoRucwRK0XoPHMI/95NQxJweeHxDDzNVdtwhURpfYs3nT6C2P4KJAJon3CwDgpr3k7QwhEjfUNHAPMz8OYrjSkeNz+Pwu4ypxnQk0MFQZNDzJVrTkC8ZglAihbG4cb8uEjr0LhJkt2NIm2kfIeah93ru3CFMsRf4NpGr3nglD9vCPh2fjKcdTGp6RGetKGIzbrnZxhQOoiReojf+fA+0dtXXpt/QW2NlJlWh7DQYSZNajyCq3BA3VG12NdkGW/ifCljXyG1i8aJdlHEJ0N1dkS8dtmZ317CpbQ/JLx4r70n41fbZWUEkLaTxNvXkqd3YA=="],
            "x5t": "Q0Y4OUZERDc2QUVDOTY4RUVCRTZDOTRGRTU5NkQ1RjU2OENBQkZBNg=="
        }
    ]


def test_decode_signed_token_with_verify_missing_jwks(mocker: MagicMock):
    # Clear the cache between executions
    jwt.CACHE.clear()

    fetch_jwks = mocker.patch("hcg_utils.authentication.jwt.fetch_jwks", return_value=[])

    result = jwt.decode_token(SIGNED_TOKEN)
    assert result == {}
    fetch_jwks.assert_called_once()


def test_decode_signed_token_with_verify(mocker: MagicMock):
    # Clear the cache between executions
    jwt.CACHE.clear()

    # Mock the audience, so we don't rely on flask.current_app
    mocker.patch("hcg_utils.authentication.jwt.get_target_audience", return_value='header-echo')

    fetch_jwks = mocker.patch("hcg_utils.authentication.jwt.fetch_jwks", return_value=fetch_jwks_response())

    # Signature will be expired, so suppress that check
    mocker.patch('jwt.api_jwt.PyJWT._validate_exp')

    result = jwt.decode_token(SIGNED_TOKEN)
    assert result != {}
    fetch_jwks.assert_called_once()


def test_decode_signed_token_no_verify():
    result = jwt.decode_token(SIGNED_TOKEN, verify=False)
    assert result != {}
    assert result['sub'] == 'logan@hcgfunds.com'
