from os import getenv

from conduct import exceptions
from conduct.types import MilliSatoshi, Payment

from .base import Wallet, RestMixin


class LntxbotWallet(Wallet, RestMixin):
    """https://github.com/fiatjaf/lntxbot/blob/master/api.go"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        self.endpoint = self._untrail(getenv("LNTXBOT_API_ENDPOINT", "https://lntxbot.bigsun.xyz/"))
        self.auth_admin = {"Authorization": f"Basic {getenv('LNTXBOT_ADMIN_KEY')}"}
        self.auth_invoice = {"Authorization": f"Basic {getenv('LNTXBOT_INVOICE_KEY')}"}

    def _check_response_errors(self, status_code: int, data: dict) -> None:
        if "error" in data and data["error"]:
            try:
                raise {
                    1: exceptions.BadAuthException,
                    2: exceptions.InsufficientPermissionsException,
                    5: exceptions.ServerErrorException,
                    7: exceptions.ServerErrorException,
                    8: exceptions.BadRequestException,
                    10: exceptions.PaymentException,
                }[data["code"]](data["message"])
            except KeyError:
                raise exceptions.ConductException(data["message"])

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get("/balance", headers=self.auth_admin)
        return MilliSatoshi.from_sat(data["BTC"]["AvailableBalance"])

    def create_invoice(self, *, amount: int, description: str = "", expiry: int = 3600) -> Payment:
        data = self._post("/addinvoice", data={"amt": str(amount), "memo": description}, headers=self.auth_invoice)

        return Payment(
            txid=self._sanitize_txid(data["payment_hash"]),
            payment_request=data["payment_request"],
            amount=MilliSatoshi.from_sat(amount),
            description=description,
        )

    def pay_invoice(self, *, payment_request: str) -> Payment:
        data = self._post("/payinvoice", data={"invoice": payment_request}, headers=self.auth_admin)

        return Payment(
            txid=self._sanitize_txid(data["decoded"]["payment_hash"]),
            payment_request=payment_request,
            amount=MilliSatoshi.from_sat(float(-data["value"])),
            description=data["memo"],
            timestamp=int(data["decoded"]["timestamp"]),
            expiry=int(data["decoded"]["expiry"]),
            fee=MilliSatoshi(data["fee_msat"]),
        )

    def get_invoice_status(self, *, txid: str):
        data = self._post(f"/invoicestatus/{txid}?wait=false", headers=self.auth_invoice)
        return data

    def get_payment_status(self, *, txid: str):
        data = self._post(f"/paymentstatus/{txid}", headers=self.auth_invoice)
        return data
