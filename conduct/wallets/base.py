import requests

from abc import ABC, abstractmethod
from http import HTTPStatus
from requests import Response

from conduct.types import Invoice, MilliSatoshi


class Wallet(ABC):
    """Abstract class."""

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_balance(self) -> MilliSatoshi:
        pass

    @abstractmethod
    def create_invoice(
        self, *, amount: int, description: str = "", expiry: int = 3600
    ) -> Invoice:
        pass

    @abstractmethod
    def pay_invoice(self, *, payment_request: str):
        pass

    @abstractmethod
    def get_invoice_status(self, *, txid: str):
        pass

    @abstractmethod
    def get_payment_status(self, *, txid: str):
        pass


class GrpcMixin:
    """Extra methods to deal with gRPC wallets."""


class RestMixin:
    """Extra methods to deal with REST wallets."""

    endpoint = ""

    def _get(self, path: str, *, params: dict = {}, headers: dict = {}):
        return self._process(
            requests.get(f"{self.endpoint}{path}", params=params, headers=headers)
        )

    def _post(self, path: str, *, data: dict = {}, headers: dict = {}):
        return self._process(
            requests.post(f"{self.endpoint}{path}", json=data, headers=headers)
        )

    def _process(self, res: Response):
        if res.status_code == HTTPStatus.NOT_FOUND:
            raise ValueError  # NotFoundException

        data = res.json()
        self._check_response_errors(data)

        return data

    def _raise_error(self, error_msg: str) -> str:
        raise NotImplementedError

    def _untrail(self, url: str) -> str:
        return url[:-1] if url.endswith("/") else url

    def _check_response_errors(self, data: dict) -> None:
        raise NotImplementedError
