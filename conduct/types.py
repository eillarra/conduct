from decimal import Decimal
from typing import NamedTuple, Optional


class EpochTime(int):
    """UNIX Epoch time."""


class Invoice(NamedTuple):
    txid: str
    payment_request: str


class Payment(NamedTuple):
    txid: str
    payment_request: str
    timestamp: EpochTime
    amount: int
    fee: int
    description: Optional[str]


class MilliSatoshi(int):
    """A thousandth of a satoshi."""

    @classmethod
    def from_btc(cls, btc: Decimal) -> "MilliSatoshi":
        return cls(btc * 100_000_000_000)

    @classmethod
    def from_sat(cls, sat: int) -> "MilliSatoshi":
        return cls(sat * 1_000)

    @property
    def btc(self) -> Decimal:
        return Decimal(self) / 100_000_000_000

    @property
    def sat(self) -> int:
        return self // 1_000
