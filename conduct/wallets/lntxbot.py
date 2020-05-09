from os import getenv

from conduct.types import Invoice, MilliSatoshi
from .base import Wallet, RestMixin


class LntxbotWallet(Wallet, RestMixin):
    """https://github.com/fiatjaf/lntxbot/blob/master/api.go"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        self.endpoint = self._untrail(
            getenv("LNTXBOT_API_ENDPOINT", "https://lntxbot.bigsun.xyz/")
        )
        self.auth_admin = {"Authorization": f"Basic {getenv('LNTXBOT_ADMIN_KEY')}"}
        self.auth_invoice = {"Authorization": f"Basic {getenv('LNTXBOT_INVOICE_KEY')}"}

    def _check_response_errors(self, data: dict) -> None:
        pass

    def _create_invoice(
        self, amount: int, description: str = "", expiry: int = 3600
    ) -> dict:
        return self._post(
            "/addinvoice",
            data={"amt": str(amount), "memo": description},
            headers=self.auth_invoice,
        )

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get("/balance", headers=self.auth_admin)
        return MilliSatoshi.from_sat(data["BTC"]["AvailableBalance"])

    def create_invoice(
        self, amount: int, description: str = "", expiry: int = 3600
    ):
        data = self._create_invoice(amount, description, expiry)
        return data

    def pay_invoice(self, *, payment_request: str):
        data = self._post(
            "/payinvoice", data={"invoice": payment_request}, headers=self.auth_admin,
        )
        return data

    def get_invoice_status(self, *, txid: str):
        data = self._post(
            f"/invoicestatus/{txid}?wait=false", headers=self.auth_invoice
        )
        return data

    def get_payment_status(self, *, txid: str):
        data = self._post(f"/paymentstatus/{txid}", headers=self.auth_invoice)
        return data
