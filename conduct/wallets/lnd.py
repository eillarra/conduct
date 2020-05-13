from os import getenv, path

from conduct import exceptions
from conduct.types import MilliSatoshi, Payment
from conduct.utils import macaroon_to_hex

from .base import Wallet, RestMixin


class LndBaseWallet(Wallet):
    def __init__(self):
        self.tls_cert = path.expanduser(getenv("LND_CERT"))


class LndWallet(LndBaseWallet):
    """https://api.lightning.community/#lnd-grpc-api-reference"""


class LndRestWallet(LndBaseWallet, RestMixin):
    """https://api.lightning.community/#lnd-rest-api-reference"""

    __slots__ = ("endpoint", "auth_admin", "auth_invoice")

    def __init__(self):
        super().__init__()

        admin_macaroon_hex = macaroon_to_hex(getenv("LND_ADMIN_MACAROON"))
        invoice_macaroon_hex = macaroon_to_hex(getenv("LND_INVOICE_MACAROON"))
        read_macaroon_hex = macaroon_to_hex(getenv("LND_READ_MACAROON"))

        self.endpoint = self._untrail(getenv("LND_REST_ENDPOINT"))
        self.auth_admin = {"Grpc-Metadata-macaroon": admin_macaroon_hex}
        self.auth_invoice = {"Grpc-Metadata-macaroon": invoice_macaroon_hex}
        self.auth_read = {"Grpc-Metadata-macaroon": read_macaroon_hex}

    def _check_response_errors(self, status_code: int, data: dict) -> None:
        pass

    def get_info(self):
        raise NotImplementedError

    def get_balance(self) -> MilliSatoshi:
        data = self._get("/v1/balance/blockchain", headers=self.auth_admin, verify=self.tls_cert)
        return MilliSatoshi.from_sat(data["total_balance"])

    def create_invoice(self, *, amount: int, description: str = "", expiry: int = 3600) -> Payment:
        invoice = self._post(
            "/v1/invoices",
            data={"value": amount, "memo": description, "expiry": expiry, "private": True,},
            headers=self.auth_invoice,
            verify=self.tls_cert,
        )
        data = self._get(f"/v1/payreq/{invoice['payment_request']}", headers=self.auth_read, verify=self.tls_cert,)

        return Payment(
            txid=self._sanitize_txid(data["payment_hash"]),
            payment_request=invoice["payment_request"],
            amount=MilliSatoshi.from_sat(int(data["num_satoshis"])),
            description=description,
            timestamp=int(data["timestamp"]),
            expiry=int(data["expiry"]),
        )

    def pay_invoice(self, *, payment_request: str) -> Payment:
        data = self._post(
            "/v1/channels/transactions",
            data={"payment_request": payment_request},
            headers=self.auth_admin,
            verify=self.tls_cert,
        )
        return data

    def get_invoice_status(self, *, txid: str):
        data = self._get(f"/v1/invoice/{txid}", headers=self.auth_invoice, verify=self.tls_cert,)
        return data

    def get_payment_status(self, *, txid: str):
        raise NotImplementedError
