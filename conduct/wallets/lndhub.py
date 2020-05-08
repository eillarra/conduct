from os import getenv
from typing import Tuple

from conduct.types import Invoice, MilliSatoshi
from .base import Wallet, RestMixin


class LndHub:
    """https://github.com/BlueWallet/LndHub/blob/master/doc/Send-requirements.md"""

    __slots__ = ("uri",)

    DEFAULT_ENDPOINT = "https://lndhub.herokuapp.com"

    def __init__(self, uri: str) -> None:
        self.uri = uri
        if (
            not uri.startswith("lndhub://")
            or not self.endpoint.startswith("https://")
            or None in self.credentials
        ):
            raise ValueError

    @property
    def endpoint(self) -> str:
        if "@" in self.uri:
            return self.uri.split("@")[1]
        return self.DEFAULT_ENDPOINT

    @property
    def credentials(self) -> Tuple[str, str]:
        username, password = (
            self.uri.replace("lndhub://", "").split("@")[0].split(":", 2)
        )
        return username, password


class LndHubWallet(Wallet, RestMixin):
    __slots__ = ("endpoint", "refresh_token", "auth")

    def __init__(self) -> None:
        lndhub = LndHub(getenv("LNDHUB_URI", ""))
        login, password = lndhub.credentials
        self.endpoint = self._untrail(lndhub.endpoint)
        self.authenticate(login=login, password=password)

    def _check_response_errors(self, data: dict) -> None:
        pass

    def authenticate(self, *, login: str, password: str) -> None:
        res = self._post("/auth?type=auth", data={"login": login, "password": password})
        self.refresh_token, access_token = res["refresh_token"], res["access_token"]
        self.auth = {"Authorization": f"Bearer {access_token}"}

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get("/balance", headers=self.auth)
        return MilliSatoshi.from_sat(data["BTC"]["AvailableBalance"])

    def create_invoice(
        self, *, amount: int, description: str = "", expiry: int = 3600
    ) -> Invoice:
        data = self._post(
            "/addinvoice",
            data={"amt": str(amount), "memo": description},
            headers=self.auth,
        )
        return Invoice(
            txid=data["add_index"],
            payment_request=data["pay_req"],
            amount=amount,
            description=description,
        )

    def pay_invoice(self, *, payment_request: str):
        data = self._post(
            "/payinvoice", data={"invoice": payment_request}, headers=self.auth
        )
        return data

    def get_invoice_status(self, *, txid: str):
        raise NotImplementedError

    def get_payment_status(self, *, txid: str):
        raise NotImplementedError
