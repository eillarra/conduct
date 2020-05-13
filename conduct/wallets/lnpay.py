from http import HTTPStatus
from os import getenv

from conduct import exceptions
from conduct.types import MilliSatoshi, Payment

from .base import Wallet, RestMixin


class LNPayWallet(Wallet, RestMixin):
    """https://docs.lnpay.co/"""

    __slots__ = ("endpoint", "auth", "admin_key", "invoice_key", "read_key")

    def __init__(self):
        self.endpoint = self._untrail(getenv("LNPAY_API_ENDPOINT", "https://lnpay.co/"))
        self.auth = {"X-Api-Key": getenv("LNPAY_API_KEY")}
        self.admin_key = getenv("LNPAY_ADMIN_KEY")
        self.invoice_key = getenv("LNPAY_INVOICE_KEY")
        self.read_key = getenv("LNPAY_READ_KEY")

    def _check_response_errors(self, status_code: int, data: dict) -> None:
        if status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR}:
            try:
                raise {
                    0: exceptions.InvalidInvoiceException,
                }[data["code"]](data["message"])
            except KeyError:
                raise exceptions.ConductException(data["message"])

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get(f"/v1/wallet/{self.read_key}", headers=self.auth)
        return MilliSatoshi.from_sat(data["balance"])

    def create_invoice(self, *, amount: int, description: str = "", expiry: int = 3600) -> Payment:
        data = self._post(
            f"/v1/wallet/{self.invoice_key}/invoice",
            data={"num_satoshis": str(amount), "memo": description, "expiry": expiry},
            headers=self.auth,
        )

        return Payment(
            txid=self._sanitize_txid(data["id"]),
            payment_request=data["payment_request"],
            amount=MilliSatoshi.from_sat(data["num_satoshis"]),
            description=data["memo"],
            timestamp=data["created_at"],
            expiry=data["expiry"],
        )

    def pay_invoice(self, *, payment_request: str) -> Payment:
        data = self._post(
            f"/v1/wallet/{self.admin_key}/withdraw", data={"payment_request": payment_request}, headers=self.auth,
        )

        return Payment(
            txid=self._sanitize_txid(data["lnTx"]["id"]),
            payment_request=data["lnTx"]["payment_request"],
            amount=MilliSatoshi.from_sat(data["lnTx"]["num_satoshis"]),
            description=data["lnTx"]["memo"],
            timestamp=data["lnTx"]["created_at"],
            expiry=data["lnTx"]["expiry"],
        )

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/v1/lntx/{txid}", headers=self.auth)
        return data

    def get_payment_status(self, *, txid: str):
        return self.get_invoice_status(txid=txid)
