from os import getenv

from conduct import exceptions
from conduct.types import MilliSatoshi, Payment

from .base import Wallet, RestMixin


class OpenNodeWallet(Wallet, RestMixin):
    """https://developers.opennode.com/reference"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        self.endpoint = self._untrail(getenv("OPENNODE_API_ENDPOINT", "https://api.opennode.com/"))
        self.auth_admin = {"Authorization": getenv("OPENNODE_ADMIN_KEY")}
        self.auth_invoice = {"Authorization": getenv("OPENNODE_INVOICE_KEY")}

    def _check_response_errors(self, status_code: int, data: dict) -> None:
        if "success" in data and not data["success"]:
            try:
                raise {
                    "invalid amount": exceptions.InvalidInvoiceException,
                }[data["message"]](data["message"])
            except KeyError:
                raise exceptions.ConductException(data["message"])

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get("/v1/account/balance", headers=self.auth_admin)
        return MilliSatoshi.from_sat(data["data"]["balance"]["BTC"])

    def create_invoice(self, *, amount: int, description: str = "", expiry: int = 3600) -> Payment:
        data = self._post(
            "/v1/charges", data={"amount": str(amount), "description": description}, headers=self.auth_invoice,
        )

        return Payment(
            txid=self._sanitize_txid(data["data"]["id"]),
            payment_request=data["data"]["lightning_invoice"]["payreq"],
            amount=MilliSatoshi.from_sat(data["data"]["amount"]),
            description=data["data"]["description"],
            timestamp=data["data"]["created_at"],
            expiry=data["data"]["lightning_invoice"]["expires_at"] - data["data"]["created_at"],
        )

    def pay_invoice(self, *, payment_request: str) -> Payment:
        data = self._post("/v2/withdrawals", data={"type": "ln", "address": payment_request}, headers=self.auth_admin)

        return Payment(
            txid=self._sanitize_txid(data["data"]["id"]),
            payment_request=data["data"]["reference"],
            amount=MilliSatoshi.from_sat(data["data"]["amount"]),
            timestamp=data["data"]["processed_at"],
            fee=MilliSatoshi.from_sat(data["data"]["fee"]),
        )

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/v1/charge/{txid}?wait=false", headers=self.auth_invoice)
        return data

    def get_payment_status(self, *, txid: str):
        data = self._get(f"/v1/withdrawal/{txid}?wait=false", headers=self.auth_invoice)
        return data
