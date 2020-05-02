from abc import ABC, abstractmethod
from typing import Optional


class Wallet(ABC):
    """Abstract class."""

    @abstractmethod
    async def get_info(self):
        pass

    @abstractmethod
    async def get_balance(self):
        pass

    @abstractmethod
    async def create_invoice(self, *, amount: Optional[int], memo: Optional[str]):
        pass

    @abstractmethod
    async def pay_invoice(self, *, payment_request: str):
        pass

    @abstractmethod
    async def get_invoice_status(self, *, invoice_id: str):
        pass

    @abstractmethod
    async def get_payment_status(self, *, payment_id: str):
        pass
