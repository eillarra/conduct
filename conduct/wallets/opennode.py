from os import getenv

from conduct.types import Invoice, MilliSatoshi
from .base import Wallet, RestMixin


class OpenNodeWallet(Wallet, RestMixin):
    """https://developers.opennode.com/"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        self.endpoint = self._untrail(
            getenv("OPENNODE_API_ENDPOINT", "https://api.opennode.com/")
        )
        self.auth_admin = {"Authorization": getenv("OPENNODE_ADMIN_KEY")}
        self.auth_invoice = {"Authorization": getenv("OPENNODE_INVOICE_KEY")}

    def _check_response_errors(self, data: dict) -> None:
        pass

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        raise NotImplementedError

    def create_invoice(
        self, amount: int, description: str = "", expiry: int = 3600
    ) -> Invoice:
        data = self._post(
            "/v1/charges",
            data={"amount": f"{amount}", "description": description},  # , "private": True},
            headers=self.auth_invoice,
        )
        return Invoice(
            txid=data["id"],
            payment_request=data["lightning_invoice"]["payreq"],
            amount=amount,
            description=description,
        )

    def pay_invoice(self, *, payment_request: str):
        data = self._post(
            "/v2/withdrawals",
            data={"type": "ln", "address": payment_request},
            headers=self.auth_admin,
        )
        return data

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/v1/charge/{txid}?wait=false", headers=self.auth_invoice)
        return data

    def get_payment_status(self, *, txid: str):
        data = self._get(f"/v1/withdrawal/{txid}?wait=false", headers=self.auth_invoice)
        return data
