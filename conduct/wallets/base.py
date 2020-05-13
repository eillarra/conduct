try:
    import requests
except ImportError:  # pragma: nocover
    requests = None  # type: ignore

from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Union

from conduct import exceptions
from conduct.types import MilliSatoshi, Payment


class Wallet(ABC):
    """Abstract class."""

    TX_LIMIT = 4_294_967

    @abstractmethod
    def get_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> MilliSatoshi:
        raise NotImplementedError

    @abstractmethod
    def create_invoice(self, *, amount: int, description: str = "", expiry: int = 3600) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def pay_invoice(self, *, payment_request: str) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def get_invoice_status(self, *, txid: str):
        raise NotImplementedError

    @abstractmethod
    def get_payment_status(self, *, txid: str):
        raise NotImplementedError

    def _desanitize_txid(self, txid: str) -> str:
        return txid.replace("=slsh=", "/")

    def _sanitize_txid(self, txid: str) -> str:
        return txid.replace("/", "=slsh=")


class GrpcMixin:
    """Extra methods to deal with gRPC wallets."""


class RestMixin:
    """Extra methods to deal with REST wallets."""

    endpoint = ""

    def __process(self, res: requests.Response) -> dict:
        if res.status_code == HTTPStatus.NOT_FOUND:
            raise exceptions.NotFoundException

        try:
            data = res.json()
        except Exception:
            raise exceptions.ServerErrorException

        self._check_response_errors(res.status_code, data)

        return data

    def _check_response_errors(self, status_code: int, data: dict) -> None:
        raise NotImplementedError

    def _get(self, path: str, *, params: dict = {}, headers: dict = {}, verify: Union[bool, str] = True,) -> dict:
        assert requests is not None, "`requests` must be installed to use this wallet."

        try:
            return self.__process(
                requests.get(f"{self.endpoint}{path}", params=params, headers=headers, verify=verify,)
            )
        except requests.exceptions.RequestException:
            raise exceptions.ServerErrorException

    def _post(self, path: str, *, data: dict = {}, headers: dict = {}, verify: Union[bool, str] = True,) -> dict:
        assert requests is not None, "`requests` must be installed to use this wallet."

        try:
            return self.__process(requests.post(f"{self.endpoint}{path}", json=data, headers=headers, verify=verify))
        except requests.exceptions.RequestException:
            raise exceptions.ServerErrorException

    def _untrail(self, url: str) -> str:
        return url[:-1] if url.endswith("/") else url
