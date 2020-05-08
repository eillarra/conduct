from os import getenv

from conduct.types import Invoice, MilliSatoshi
from .base import Wallet, RestMixin


class LNPayWallet(Wallet, RestMixin):
    """https://docs.lnpay.co/"""

    __slots__ = ("endpoint", "auth", "admin_key", "invoice_key", "read_key")

    def __init__(self):
        self.endpoint = self._untrail(
            getenv("LNPAY_API_ENDPOINT", "https://lnpay.co/v1/")
        )
        self.auth = {"X-Api-Key": getenv("LNPAY_API_KEY")}
        self.admin_key = getenv("LNPAY_ADMIN_KEY")
        self.invoice_key = getenv("LNPAY_INVOICE_KEY")
        self.read_key = getenv("LNPAY_READ_KEY")

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
            f"/wallet/{self.invoice_key}/invoice",
            data={"num_satoshis": str(amount), "memo": description, "expiry": expiry},
            headers=self.auth,
        )
        return Invoice(
            txid=data["id"],
            payment_request=data["payment_request"],
            amount=amount,
            description=description,
        )

    def pay_invoice(self, *, payment_request: str):
        data = self._post(
            f"/wallet/{self.admin_key}/withdraw",
            data={"payment_request": payment_request},
            headers=self.auth,
        )
        return data

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/lntx/{txid}", headers=self.auth)
        return data

    def get_payment_status(self, *, txid: str):
        return self.get_invoice_status(txid=txid)
