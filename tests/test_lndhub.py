import pytest

from conduct.wallets.lndhub import LndHub


class TestLndHub:
    @pytest.mark.parametrize(
        "uri",
        [
            "https://invalid.com",
            "lndhub://username:password@http://invalid.com",
            "lndhub://username",
        ],
    )
    def test_invalid_url(self, uri):
        with pytest.raises(ValueError):
            LndHub(uri)

    @pytest.mark.parametrize(
        "uri, username, password, endpoint",
        [
            (
                "lndhub://username:password@https://endpoint.com",
                "username",
                "password",
                "https://endpoint.com",
            ),
            (
                "lndhub://username:password",
                "username",
                "password",
                LndHub.DEFAULT_ENDPOINT,
            ),
        ],
    )
    def test_valid_url(self, uri, username, password, endpoint):
        lndhub = LndHub(uri)
        user, passw = lndhub.credentials
        assert user == username
        assert passw == password
        assert lndhub.endpoint == endpoint
