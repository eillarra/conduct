from os import getenv

from conduct.types import Invoice, MilliSatoshi
from .base import Wallet, RestMixin


class LNbitsWallet(Wallet, RestMixin):
    """https://github.com/lnbits/lnbits"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        self.endpoint = self._untrail(
            getenv("LNBITS_API_ENDPOINT", "https://lnbits.com/")
        )
        self.auth_admin = {"X-Api-Key": getenv("LNBITS_ADMIN_KEY")}
        self.auth_invoice = {"X-Api-Key": getenv("LNBITS_INVOICE_KEY")}

    def _check_response_errors(self, data: dict) -> None:
        pass

    def _create_invoice(
        self, amount: int, description: str = "", expiry: int = 3600
    ) -> dict:
        return self._post(
            f"/api/v1/payments",
            data={"out": False, "amount": amount, "memo": description},
            headers=self.auth_invoice,
        )

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        raise NotImplementedError

    def create_invoice(
        self, amount: int, description: str = "", expiry: int = 3600
    ):
        data = self._create_invoice(amount, description, expiry)
        return data

    def pay_invoice(self, *, payment_request: str):
        data = self._post(
            f"/api/v1/payments",
            data={"out": True, "bolt11": payment_request},
            headers=self.auth_admin,
        )
        return data

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/api/v1/payments/{txid}", headers=self.auth_invoice)
        return data

    def get_payment_status(self, *, txid: str):
        return self.get_invoice_status(txid=txid)
