from decimal import Decimal
from typing import NamedTuple, Optional, Union


class MilliSatoshi(int):
    """A thousandth of a satoshi."""

    @classmethod
    def from_btc(cls, btc: Decimal) -> "MilliSatoshi":
        return cls(btc * 100_000_000_000)

    @classmethod
    def from_sat(cls, sat: Union[int, float]) -> "MilliSatoshi":
        return cls(sat * 1_000)

    @property
    def btc(self) -> Decimal:
        return Decimal(self) / 100_000_000_000

    @property
    def sat(self) -> Decimal:
        return Decimal(self) / 1_000


class Payment(NamedTuple):
    txid: str
    payment_request: str
    amount: MilliSatoshi
    description: Optional[str] = None
    timestamp: Optional[int] = None
    expiry: Optional[int] = None
    fee: Optional[MilliSatoshi] = None
