import pytest
import uuid

from conduct.exceptions import ConductException
from conduct.types import Payment
from conduct.wallets import (
    LNbitsWallet,
    LNPayWallet,
    LntxbotWallet,
    OpenNodeWallet,
)


WALLET_CLASSES = [LNbitsWallet, LNPayWallet, LntxbotWallet, OpenNodeWallet]


def short_uuid() -> str:
    return f"conduct_{str(uuid.uuid4())[:8]}"


class TestTransactions:
    """Tests a chain of transactions between wallets."""

    @pytest.mark.parametrize("wallet_class", WALLET_CLASSES)
    @pytest.mark.skip
    def test_balance(self, wallet_class):
        assert wallet_class().get_balance().sat >= 0

    @pytest.mark.parametrize("wallet_class", WALLET_CLASSES)
    def test_create_invoice(self, wallet_class):
        invoice = wallet_class().create_invoice(amount=10, description=short_uuid())
        assert isinstance(invoice, Payment)

    @pytest.mark.parametrize("wallet_class", WALLET_CLASSES)
    def test_create_invalid_invoice(self, wallet_class):
        with pytest.raises(ConductException):
            wallet_class().create_invoice(amount=-10)
